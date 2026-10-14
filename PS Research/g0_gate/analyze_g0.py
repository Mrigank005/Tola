"""G0 analysis. Implements G0_PREREGISTRATION.md exactly; any change to thresholds belongs there first.

Reads raw/contract/*.json written by fetch_g0.py, writes results/*.csv, results/g0_results.json and G0_RESULTS.md.
"""
import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
RAW, OUT = HERE / "raw" / "contract", HERE / "results"
OUT.mkdir(exist_ok=True)

LOT_G = {"GOLDTEN": 10, "GOLDGUINEA": 8, "GOLDPETAL": 1}
QUOTE_G = {"GOLDTEN": 10, "GOLDGUINEA": 8, "GOLDPETAL": 1}
MARKS = ("close", "open", "mid", "vwap")
PAIRS = (("GOLDGUINEA", "GOLDTEN"), ("GOLDPETAL", "GOLDTEN"))

# Pre-registered parameters
TENDER_EXCL = 5          # last N trading days of each contract excluded
VALUE_FLOOR_LAKH = 100   # Rs 1 crore per leg per day
MIN_DAYS = 10            # eligible days for a cycle to survive
MIN_CYCLES = 8
GO_MIN_BP = 15.0
GO_HIT = 0.75
N_BOOT, SEED = 10_000, 20261013


def load():
    rows = []
    for f in sorted(RAW.glob("*.json")):
        sym, exp = f.stem.split("_")
        data = json.loads(f.read_text()).get("Data") or []
        for w in data:
            rows.append({
                "sym": sym, "expiry": datetime.strptime(exp, "%Y%m%d").date(),
                "date": datetime.strptime(w["Date"], "%m/%d/%Y").date(),
                "open": w["Open"], "high": w["High"], "low": w["Low"], "close": w["Close"],
                "volume": w["Volume"], "value": w["Value"],
            })
    df = pd.DataFrame(rows).drop_duplicates(["sym", "expiry", "date"]).sort_values(["sym", "expiry", "date"])
    # trading days to expiry, counted on the contract's own rows (MCX publishes a row every trading day)
    df["tdte"] = df.groupby(["sym", "expiry"]).cumcount(ascending=False)
    q = df["sym"].map(QUOTE_G)
    df["close_g"] = df["close"] / q
    df["open_g"] = df["open"] / q
    df["mid_g"] = (df["high"] + df["low"]) / 2 / q
    df["vwap_g"] = np.where(df["volume"] > 0, df["value"] * 1e5 / (df["volume"] * df["sym"].map(LOT_G)), np.nan)
    df["traded"] = (df["volume"] > 0) & (df["open"] > 0) & (df["high"] > 0) & (df["low"] > 0)
    return df


def pair_days(df, small, big, tender_excl=TENDER_EXCL, floor=VALUE_FLOOR_LAKH):
    a = df[df.sym == small]
    b = df[df.sym == big]
    m = a.merge(b, on=["expiry", "date"], suffixes=("_s", "_b"))
    ok = (m.traded_s & m.traded_b & (m.value_s >= floor) & (m.value_b >= floor)
          & (m.tdte_s >= tender_excl) & (m.tdte_b >= tender_excl))
    m = m[ok].copy()
    for k in MARKS:
        m[f"prem_{k}"] = 1e4 * (m[f"{k}_g_s"] / m[f"{k}_g_b"] - 1)
    return m


def cycle_table(m):
    g = m.groupby("expiry")
    t = g[[f"prem_{k}" for k in MARKS]].mean()
    t["days"] = g.size()
    return t[t.days >= MIN_DAYS]


def boot_ci(x, rng):
    x = np.asarray(x)
    idx = rng.integers(0, len(x), size=(N_BOOT, len(x)))
    means = x[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def summarise(cyc):
    rng = np.random.default_rng(SEED)
    out = {"cycles": int(len(cyc)), "marks": {}}
    for k in MARKS:
        x = cyc[f"prem_{k}"].values
        if len(x) == 0:
            out["marks"][k] = None
            continue
        lo, hi = boot_ci(x, rng) if len(x) > 1 else (np.nan, np.nan)
        out["marks"][k] = {"pooled": float(x.mean()), "ci_lo": lo, "ci_hi": hi, "hit": float((x > 0).mean())}
    return out


def decide(s):
    mk = s["marks"]
    if s["cycles"] < MIN_CYCLES:
        return "PARTIAL", f"only {s['cycles']} surviving cycles (< {MIN_CYCLES})"
    go = all(mk[k] and mk[k]["pooled"] >= GO_MIN_BP and mk[k]["ci_lo"] > 0 and mk[k]["hit"] >= GO_HIT for k in MARKS)
    if go:
        return "GO", "all four marks: pooled >= 15 bp, CI above 0, hit rate >= 75%"
    if mk["vwap"]["ci_lo"] > 0 and mk["close"]["ci_lo"] > 0:
        return "PARTIAL", "VWAP and Close CIs above 0, but not every GO condition met"
    return "NO-GO", "VWAP or Close CI includes 0 or lies below it"


def decay(m):
    bins = [5, 10, 20, 40, 60, 1000]
    lab = ["5-9", "10-19", "20-39", "40-59", "60+"]
    m = m.assign(bucket=pd.cut(m.tdte_b, bins=bins, right=False, labels=lab))
    per_cycle = m.groupby(["bucket", "expiry"], observed=True)[["prem_vwap", "prem_close"]].mean()
    return per_cycle.groupby("bucket", observed=True).agg(["mean", "count"]).round(1)


def main():
    df = load()
    df.to_csv(OUT / "gold_small_contracts_daily.csv", index=False)
    exps = {s: set(df[df.sym == s].expiry) for s in LOT_G}
    shared = sorted(exps["GOLDTEN"] & exps["GOLDGUINEA"] & exps["GOLDPETAL"])
    res = {"shared_cycles": [str(e) for e in shared], "pairs": {}, "sensitivity": {}}
    md = []
    for small, big in PAIRS:
        name = f"{small}-{big}"
        m = pair_days(df[df.expiry.isin(shared)], small, big)
        cyc = cycle_table(m)
        cyc.round(2).to_csv(OUT / f"cycles_{name}.csv")
        s = summarise(cyc)
        verdict, why = decide(s)
        s.update(verdict=verdict, reason=why, eligible_days=int(len(m)),
                 decay=decay(m).reset_index().astype(str).values.tolist())
        res["pairs"][name] = s
        # sensitivity (never decisive)
        sens = {}
        for label, kw, filt in [
            ("floor_0.25cr", {"floor": 25}, None),
            ("floor_5cr", {"floor": 500}, None),
            ("tender_3day", {"tender_excl": 3}, None),
            ("ex_crash_cycles", {}, lambda c: c[~c.index.map(lambda e: e.year == 2026 and e.month <= 3)]),
        ]:
            cs = cycle_table(pair_days(df[df.expiry.isin(shared)], small, big, **kw))
            if filt:
                cs = filt(cs)
            ss = summarise(cs)
            sens[label] = {"cycles": ss["cycles"], **{k: (round(v["pooled"], 1) if v else None) for k, v in ss["marks"].items()},
                           "vwap_ci": [round(ss["marks"]["vwap"]["ci_lo"], 1), round(ss["marks"]["vwap"]["ci_hi"], 1)] if ss["marks"]["vwap"] else None}
        res["sensitivity"][name] = sens
    # context: GOLDGUINEA vs GOLDPETAL since 2020 (not part of the decision)
    ctx = pair_days(df, "GOLDPETAL", "GOLDGUINEA")
    ctx_c = cycle_table(ctx)
    ctx_c.round(2).to_csv(OUT / "context_cycles_GOLDPETAL-GOLDGUINEA.csv")
    res["context_petal_vs_guinea"] = {"cycles": int(len(ctx_c)),
                                       "by_year_vwap": ctx_c.groupby(ctx_c.index.map(lambda e: e.year))["prem_vwap"].mean().round(1).to_dict()}
    pairs_v = [p["verdict"] for p in res["pairs"].values()]
    res["overall"] = "GO" if "GO" in pairs_v else ("PARTIAL" if "PARTIAL" in pairs_v else "NO-GO")
    (OUT / "g0_results.json").write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps(res, indent=1, default=str))


if __name__ == "__main__":
    main()
