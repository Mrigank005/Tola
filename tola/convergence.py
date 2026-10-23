"""M3 Same-reference convergence monitor.

Pairs of contracts with the same expiry, compared per gram at 999 on the same day:

  GOLDGUINEA / GOLDTEN    same settlement reference (Ahmedabad poll): any premium must vanish at settlement
  GOLDPETAL  / GOLDTEN    same rule, Mumbai poll: the premium should converge to the Mumbai-Ahmedabad spot gap
  GOLDPETAL  / GOLDGUINEA context back to 2020, before GOLDTEN existed
  GOLD       / GOLDM      control: both 995, both 3-day-average settlement; listed together on even months only

premium_bp = 1e4 x (small / big - 1), on the close (last half-hour VWAP) and on the day's VWAP. A day is eligible
when both legs traded at least Rs 1 crore and neither is in its tender window (G0's liquidity rule, with the
tender window taken from each contract's own spec version). A cycle counts when it has at least 10 eligible days.

Outputs:
  convergence_daily    one row per pair per shared trading day
  convergence_cycles   one row per pair per expiry: premium path by trading days to expiry, the last pre-tender
                       premium, the settlement gap (rebuilt DDRs, M1) and what a holder into settlement gives up
  convergence_summary  one row per pair: pooled mean of expired cycle means with a cycle-bootstrap CI, hit rate
  convergence_profile  one row per pair per days-to-expiry bucket, pooled over expired cycles
  convergence_live     one row per pair per live cycle: today's premium against history at the same stage
"""
import numpy as np
import pandas as pd

from .checks import Report

PAIRS = [
    ("GOLDGUINEA", "GOLDTEN", "same reference"),
    ("GOLDPETAL", "GOLDTEN", "Mumbai reference"),
    ("GOLDPETAL", "GOLDGUINEA", "context"),
    ("GOLD", "GOLDM", "control"),
]
VALUE_FLOOR_LAKH = 100
MIN_DAYS = 10
N_BOOT, SEED = 10_000, 20261013
# Live readings are ranked against cycles from the same contract regime. GOLDPETAL before the Apr 2025 contract
# (first under the current spec, with the Rs 100/g making charge) traded at a deep discount and is not comparable.
LIVE_HISTORY_FROM = {"GOLDPETAL/GOLDGUINEA": pd.Timestamp("2025-04-01").date()}
BUCKETS = [(60, 10_000, "60+"), (40, 60, "40-59"), (20, 40, "20-39"), (10, 20, "10-19"), (5, 10, "5-9"), (0, 5, "0-4")]


def bucket(tdte):
    for lo, hi, name in BUCKETS:
        if lo <= tdte < hi:
            return name
    return None


def cluster_ci(x, rng):
    """95% CI of the mean, resampling whole cycles (the G0 method)."""
    x = np.asarray(x, dtype=float)
    if len(x) < 2:
        return np.nan, np.nan
    means = x[rng.integers(0, len(x), size=(N_BOOT, len(x)))].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def daily(fut, basis):
    ref = basis.set_index(["symbol", "expiry", "date"]).reference_bp
    keep = ["date", "expiry", "last_trading_day", "tdte", "in_tender", "traded", "value_lakh", "close_g999", "vwap_g999"]
    out = []
    for small, big, kind in PAIRS:
        m = fut[fut.symbol == small][keep].merge(fut[fut.symbol == big][keep], on=["expiry", "date"], suffixes=("_s", "_b"))
        if m.empty:
            continue
        m.insert(0, "pair", f"{small}/{big}")
        m.insert(1, "kind", kind)
        m["small"], m["big"] = small, big
        m["tdte"] = m[["tdte_s", "tdte_b"]].min(axis=1)
        m["in_tender"] = m.in_tender_s | m.in_tender_b
        m["both_traded"] = m.traded_s & m.traded_b
        m["eligible"] = m.both_traded & (m.value_lakh_s >= VALUE_FLOOR_LAKH) & (m.value_lakh_b >= VALUE_FLOOR_LAKH) & ~m.in_tender
        m["premium_close_bp"] = np.where(m.both_traded, 1e4 * (m.close_g999_s / m.close_g999_b - 1), np.nan)
        m["premium_vwap_bp"] = np.where(m.both_traded, 1e4 * (m.vwap_g999_s / m.vwap_g999_b - 1), np.nan)
        rs = [ref.get((small, x, d), np.nan) for x, d in zip(m.expiry, m.date)]
        rb = [ref.get((big, x, d), np.nan) for x, d in zip(m.expiry, m.date)]
        m["reference_gap_bp"] = np.array(rs) - np.array(rb)
        m["bucket"] = [bucket(t) for t in m.tdte]
        out.append(m)
    d = pd.concat(out, ignore_index=True)
    cols = ["pair", "kind", "small", "big", "date", "expiry", "tdte", "bucket", "in_tender", "both_traded", "eligible",
            "value_lakh_s", "value_lakh_b", "close_g999_s", "close_g999_b", "vwap_g999_s", "vwap_g999_b",
            "premium_close_bp", "premium_vwap_bp", "reference_gap_bp"]
    return d[cols].sort_values(["pair", "expiry", "date"]).reset_index(drop=True)


def cycles(d, settlement, contracts, asof):
    ddr = settlement[settlement.ddr_reliable].set_index(["symbol", "expiry"]).ddr_g999
    ltd = contracts.set_index(["symbol", "expiry"]).last_trading_day
    rows = []
    for (pair, expiry), g in d.groupby(["pair", "expiry"]):
        small, big, kind = g.small.iloc[0], g.big.iloc[0], g.kind.iloc[0]
        e = g[g.eligible]
        r = {"pair": pair, "kind": kind, "small": small, "big": big, "expiry": expiry,
             "status": "expired" if expiry < asof else "live",
             "last_trading_day": min(ltd.get((small, expiry), expiry), ltd.get((big, expiry), expiry)),
             "eligible_days": len(e), "counts": len(e) >= MIN_DAYS,
             "mean_vwap_bp": e.premium_vwap_bp.mean() if len(e) else np.nan,
             "mean_close_bp": e.premium_close_bp.mean() if len(e) else np.nan}
        for _, _, name in BUCKETS:
            b = e[e.bucket == name].premium_vwap_bp
            r[f"vwap_{name}_bp"] = b.mean() if len(b) else np.nan
        if len(e):
            last = e.sort_values("date").iloc[-1]
            r.update(last_eligible_date=last.date, last_eligible_tdte=int(last.tdte),
                     last_premium_vwap_bp=last.premium_vwap_bp, last_premium_close_bp=last.premium_close_bp,
                     last_big_g999=last.vwap_g999_b)
        ds, db = ddr.get((small, expiry)), ddr.get((big, expiry))
        if ds is not None and db is not None:
            r["settlement_gap_bp"] = 1e4 * (ds / db - 1)
            if "last_premium_vwap_bp" in r:
                r["given_up_bp"] = r["last_premium_vwap_bp"] - r["settlement_gap_bp"]
                r["given_up_inr_g"] = r["given_up_bp"] / 1e4 * r["last_big_g999"]
        rows.append(r)
    return pd.DataFrame(rows).sort_values(["pair", "expiry"]).reset_index(drop=True)


def summary(cyc):
    rng = np.random.default_rng(SEED)
    rows = []
    # Pooled over expired cycles only (a live cycle's mean is still moving); live cycles are in convergence_live.
    for pair, g in cyc[cyc.counts & (cyc.status == "expired")].groupby("pair", sort=False):
        x = g.mean_vwap_bp.values
        lo, hi = cluster_ci(x, rng)
        c_lo, c_hi = cluster_ci(g.mean_close_bp.values, rng)
        exp = g
        rows.append({"pair": pair, "kind": g.kind.iloc[0], "cycles": len(g), "first_expiry": g.expiry.min(), "last_expiry": g.expiry.max(),
                     "pooled_vwap_bp": x.mean(), "ci_lo_bp": lo, "ci_hi_bp": hi, "hit_rate": float((x > 0).mean()),
                     "pooled_close_bp": g.mean_close_bp.mean(), "close_ci_lo_bp": c_lo, "close_ci_hi_bp": c_hi,
                     "settlement_gap_bp_median": exp.settlement_gap_bp.median(),
                     "settlement_gap_bp_maxabs": exp.settlement_gap_bp.abs().max(),
                     "given_up_bp_mean": exp.given_up_bp.mean(), "given_up_inr_g_mean": exp.given_up_inr_g.mean()})
    return pd.DataFrame(rows)


def profile(d, cyc):
    """Premium by days to expiry, pooled as the mean of cycle means over expired cycles that count."""
    keep = cyc[cyc.counts & (cyc.status == "expired")][["pair", "expiry"]]
    e = d[d.eligible].merge(keep, on=["pair", "expiry"])
    per = e.groupby(["pair", "bucket", "expiry"]).premium_vwap_bp.mean().reset_index()
    rng = np.random.default_rng(SEED)
    rows = []
    for (pair, b), g in per.groupby(["pair", "bucket"]):
        lo, hi = cluster_ci(g.premium_vwap_bp.values, rng)
        rows.append({"pair": pair, "bucket": b, "cycles": len(g), "mean_vwap_bp": g.premium_vwap_bp.mean(), "ci_lo_bp": lo, "ci_hi_bp": hi})
    order = {name: i for i, (_, _, name) in enumerate(BUCKETS)}
    p = pd.DataFrame(rows)
    return p.assign(_o=p.bucket.map(order)).sort_values(["pair", "_o"]).drop(columns="_o").reset_index(drop=True)


def live(d, cyc):
    """Latest reading of each live cycle against expired cycles of the same pair at the same stage."""
    hist = d[d.eligible].merge(cyc[cyc.counts & (cyc.status == "expired")][["pair", "expiry"]], on=["pair", "expiry"])
    rows = []
    for (pair, expiry), g in d.merge(cyc[cyc.status == "live"][["pair", "expiry"]], on=["pair", "expiry"]).groupby(["pair", "expiry"]):
        g = g[g.both_traded].sort_values("date")
        if g.empty:
            continue
        now = g.iloc[-1]
        h = hist[(hist.pair == pair) & (hist.bucket == now.bucket)]
        h = h[h.expiry >= LIVE_HISTORY_FROM.get(pair, h.expiry.min() if len(h) else expiry)]
        ref = h.groupby("expiry").premium_vwap_bp.mean()
        prev = g.iloc[-6] if len(g) >= 6 else None   # five trading days earlier
        rows.append({"pair": pair, "expiry": expiry, "date": now.date, "tdte": int(now.tdte), "bucket": now.bucket,
                     "eligible": bool(now.eligible), "in_tender": bool(now.in_tender),
                     "premium_vwap_bp": now.premium_vwap_bp, "premium_close_bp": now.premium_close_bp,
                     "change_5d_bp": now.premium_vwap_bp - prev.premium_vwap_bp if prev is not None else np.nan,
                     "history_cycles": len(ref), "history_mean_bp": ref.mean() if len(ref) else np.nan,
                     "history_pct_rank": float((ref < now.premium_vwap_bp).mean()) if len(ref) else np.nan,
                     "value_lakh_small": now.value_lakh_s, "value_lakh_big": now.value_lakh_b})
    return pd.DataFrame(rows)


def build(fut, basis, settlement, contracts, asof, report=None):
    report = report or Report()
    d = daily(fut, basis)
    cyc = cycles(d, settlement, contracts, asof)
    summ = summary(cyc)
    prof = profile(d, cyc)
    lv = live(d, cyc)

    same = cyc[(cyc.pair == "GOLDGUINEA/GOLDTEN") & cyc.settlement_gap_bp.notna()]
    off = same[same.settlement_gap_bp.abs() > 0.5]
    for r in off.head(5).itertuples():
        report.add("convergence.same_reference_settles_apart", "warn", f"{r.expiry}: {r.settlement_gap_bp:+.2f} bp",
                   "GOLDGUINEA and GOLDTEN should settle to the same price per gram")
    if off.empty and len(same):
        report.ok("convergence.same_reference_settles_apart",
                  f"GOLDGUINEA and GOLDTEN settle within 0.5 bp per gram in all {len(same)} expired cycles")
    report.add("convergence.cycles", "info", n=int(cyc.counts.sum()),
               note=f"Pair-cycles with {MIN_DAYS}+ eligible days ({(cyc.status == 'live').sum()} pair-cycles live)")
    return {"convergence_daily": d, "convergence_cycles": cyc, "convergence_summary": summ,
            "convergence_profile": prof, "convergence_live": lv}, report
