"""Write the JSON the web app reads (data/export/). Everything is derived from the committed snapshot.

  chooser.json   live contracts, premium-change history, cost schedule, delivery inputs, coin prices: everything the
                 chooser formula needs, so the app computes quotes in the browser for any input
  golden.json    reference quotes from tola.chooser for a set of requests; the app's JS port must reproduce them
  alerts.json    the quiet alert log and its summary
  calendar.json  live contracts' key dates
  meta.json      as-of dates and build info

Usage: python -m tola.export   (also run at the end of python -m tola.refresh)
"""
import json
from datetime import date, datetime
from pathlib import Path

import numpy as np
import pandas as pd

from . import alerts, chooser, costs, specs

ROOT = Path(__file__).resolve().parent.parent
SNAP = ROOT / "data" / "snapshot"
OUT = ROOT / "data" / "export"
GOLDEN_REQUESTS = [
    chooser.Request(100, 20, False), chooser.Request(10, 60, False), chooser.Request(1, 5, False), chooser.Request(1000, 40, False),
    chooser.Request(8, 20, True), chooser.Request(100, 20, True), chooser.Request(1, 10, True),
]


def _clean(v):
    if isinstance(v, (pd.Timestamp, datetime, date)):
        return str(v)[:10]
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating, float)):
        return None if not np.isfinite(v) else float(v)   # full precision: the app's port must match tola.chooser
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if v is pd.NA or v is pd.NaT:
        return None
    return v


def records(df):
    return [{k: _clean(v) for k, v in r.items()} for r in df.to_dict("records")]


def write(name, obj):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.json").write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=_clean), encoding="utf-8")


def _settlement_check(st):
    """Before Oct 2023 MCX published the DDR as the last-day close: how many rebuilt DDRs can be checked, and match."""
    t = st[st.close_is_ddr_era & st.ddr_reliable]
    return {"checked": int(len(t)), "matched": int(t.ddr_matches_close.sum())}


def evidence(read, basis, curve, conv, cycles, asof):
    """Figures for the Overview, Basis, Convergence, Verdict and Method pages, all from the snapshot."""
    summ, prof, live = read("convergence_summary"), read("convergence_profile"), read("convergence_live")
    wf, dlv = read("wf_summary"), read("delivery_summary")
    same = ["GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN"]
    exp = cycles[cycles.pair.isin(same + ["GOLD/GOLDM"]) & cycles.counts & (cycles.status == "expired")]
    e = conv[conv.eligible & conv.pair.isin(same) & (conv.expiry >= chooser.CURRENT_ERA)]
    monthly = (e.assign(month=pd.to_datetime(e.date).dt.to_period("M").astype(str))
               .groupby(["pair", "month"]).premium_vwap_bp.median().reset_index())
    # Today's waterfall: the most liquid live expiry per symbol
    today = basis[basis.date == asof].sort_values("value_lakh", ascending=False).drop_duplicates("symbol")
    carry = curve[curve.carry_source == "fit"][["date", "carry_pa", "rf_pct", "timing_bp"]]
    carry = carry.assign(month=pd.to_datetime(carry.date).dt.to_period("M").astype(str)).groupby("month").median(numeric_only=True).reset_index()
    resid = basis[(basis.value_lakh >= 100) & ~basis.in_tender].dropna(subset=["residual_bp"])
    resid = resid.assign(year=pd.to_datetime(resid.date).dt.year).groupby(["year", "symbol"]).residual_bp.median().reset_index()
    manifest = json.loads((SNAP / "manifest.json").read_text(encoding="utf-8"))
    return {
        "asof": str(asof),
        "summary": records(summ), "profile": records(prof), "live": records(live),
        "cycles": records(exp[["pair", "expiry", "mean_vwap_bp", "eligible_days", "settlement_gap_bp", "given_up_bp", "given_up_inr_g",
                               "last_premium_vwap_bp"]]),
        "monthly": records(monthly),
        "waterfall_today": records(today[["symbol", "expiry", "close_g999", "ref_spot_g999", "fair_g999", "basis_total_bp", "timing_bp",
                                          "carry_bp", "reference_bp", "residual_bp", "making_charge_inr_g", "making_charge_bp", "value_lakh"]]),
        "carry_monthly": records(carry),
        "residual_by_year": records(resid),
        "walk_forward": records(wf), "delivery": records(dlv),
        "validation": manifest["validation"], "coverage": manifest["coverage"],
        "settlement_check": _settlement_check(read("settlement")),
        "spec_versions": sum(len(v["versions"]) for v in specs.load().values()),
        "tables": {k: v["rows"] for k, v in manifest["tables"].items()},
    }


def run(log=print):
    read = lambda n: pd.read_parquet(SNAP / f"{n}.parquet")
    basis, contracts, curve, conv, cycles, fut = (read(n) for n in ("basis_daily", "contracts", "curve_daily", "convergence_daily",
                                                                    "convergence_cycles", "futures_daily"))
    live, asof = chooser.live_inputs(basis, contracts, curve)
    changes = chooser.premium_changes(conv)
    cfg = costs.load()

    write("chooser", {
        "asof": str(asof),
        "contracts": records(live),
        "premium_changes": records(changes),
        "costs": {"statutory": cfg["statutory"], "brokers": cfg["brokers"], "tick_inr_per_quote_unit": cfg["tick_inr_per_quote_unit"],
                  "slippage_ticks_base": cfg["slippage_ticks_per_order"]["base"]},
        "delivery": {k: v for k, v in cfg["delivery"].items() if k != "coin_price_observations"},
        "coin_price_observations": [{k: _clean(v) for k, v in o.items()} for o in cfg["delivery"]["coin_price_observations"]],
        "constants": {"gst_pct": chooser.GST_PCT, "max_size_gap": chooser.MAX_SIZE_GAP, "min_turnover_lakh": chooser.MIN_TURNOVER_LAKH,
                      "horizons": list(chooser.HORIZONS)},
        "symbols": {s: {**specs.basis(s), "spot": specs.spot(s)} for s in specs.symbols()},
    })
    golden = []
    for req in GOLDEN_REQUESTS:
        q = chooser.quote(req, live, changes, asof)
        golden.append({"request": req.__dict__, "quotes": records(q)})
    write("golden", {"asof": str(asof), "cases": golden})

    trading_days = sorted(fut.date.unique())
    log_df, summary = alerts.build(conv, contracts, cycles, trading_days, asof)
    write("alerts", {"asof": str(asof), "summary": summary, "rules": {
        "swing": f"premium beyond {alerts.SWING_K} sd of its last {alerts.SWING_W} eligible days (most liquid expiry)",
        "tender": f"{alerts.TENDER_NOTICE} trading days before a live contract's tender window",
        "control": f"GOLD vs GOLDM beyond {alerts.CONTROL_BP:g} bp", "settlement": f"same-reference pair settled more than {alerts.SETTLE_BP:g} bp apart"},
        "alerts": records(log_df)})
    write("calendar", {"asof": str(asof), "contracts": records(alerts.calendar(contracts, live))})
    write("evidence", evidence(read, basis, curve, conv, cycles, asof))
    manifest = json.loads((SNAP / "manifest.json").read_text(encoding="utf-8"))
    write("meta", {"asof": str(asof), "data_asof": manifest["data_asof"], "spot_asof": manifest["spot_asof"],
                   "built_at": manifest["built_at"], "exported_at": datetime.now().astimezone().isoformat(timespec="seconds")})
    log(f"export: {len(live)} live contracts, {len(log_df)} alerts ({summary['quiet_days']} of {summary['trading_days']} trading days quiet) -> data/export/")


if __name__ == "__main__":
    run()
