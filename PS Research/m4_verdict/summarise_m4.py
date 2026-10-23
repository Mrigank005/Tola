"""Tables behind M4_RESULTS.md, computed from the committed snapshot. Writes m4_tables.md next to this file.

Usage: python "PS Research/m4_verdict/summarise_m4.py"
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
SNAP = HERE.parent.parent / "data" / "snapshot"
read = lambda n: pd.read_parquet(SNAP / f"{n}.parquet")
s, t, ds, dc = read("wf_summary"), read("wf_trades"), read("delivery_summary"), read("delivery_cycles")
SAME = ["GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN"]

out = ["# M4 tables", "", f"Generated from data/snapshot (data through {t.exit_date.max()}). Position: 200 g per leg, "
       "signals at day t's close, fills at the next eligible day's VWAP, exit before tender. Base slippage 1 tick per order.", ""]

out += ["## 0. Why slippage is assumed: EDGE (Ardia, Guidotti & Kroencke 2024) on daily OHLC, per contract", ""]
import warnings
from bidask import edge
warnings.filterwarnings("ignore")
f = read("futures_daily")
f = f[f.traded & (f.value_lakh >= 100) & ~f.in_tender].sort_values(["symbol", "expiry", "date"])
er = []
for (sym, x), g in f.groupby(["symbol", "expiry"]):
    if len(g) >= 20:
        er.append({"symbol": sym, "year": pd.Timestamp(x).year, "edge_bp": 1e4 * edge(g.open.values, g.high.values, g.low.values, g.close.values),
                   "daily_vol_bp": 1e4 * np.log(g.close).diff().std(), "tick_bp": 1e4 / g.close.median()})
er = pd.DataFrame(er)
out += [er[er.year >= 2023].pivot_table(index="year", columns="symbol", values="edge_bp", aggfunc="median").round(1).to_markdown(), "",
        f"Correlation of EDGE with daily volatility across contracts: {er[['edge_bp', 'daily_vol_bp']].dropna().corr().iloc[0, 1]:.2f}. "
        f"Tick size: {er[er.year >= 2026].groupby('symbol').tick_bp.median().round(2).to_dict()} bp.", ""]

out += ["## 1. Scored strategies (DRIFT: no tuning; MR walk-forward: out-of-sample only)", ""]
cols = ["pair", "strategy", "trades", "cycles", "mean_gross_bp", "mean_cost_bp", "mean_net_bp", "ci_lo_bp", "ci_hi_bp", "hit_rate",
        "sharpe_per_trade", "deflated_sharpe_prob", "random_entry_p", "mean_net_bp_ex_crash", "ex_crash_ci_lo_bp", "ex_crash_ci_hi_bp",
        "trades_ex_crash", "breakeven_slippage_ticks", "spread_leg_share", "total_net_inr"]
out += [s[cols].round(2).to_markdown(index=False), ""]

out += ["## 2. MR walk-forward by period (out-of-sample, same-reference pairs)", ""]
w = t[t.out_of_sample & t.pair.isin(SAME)].copy()
w["period"] = np.select([pd.to_datetime(w.exit_date) < "2026-01-01", pd.to_datetime(w.entry_date) <= "2026-03-31"],
                        ["2025", "Jan-Mar 2026"], "Apr-Oct 2026")
out += [w.groupby(["pair", "period"]).agg(trades=("net_bp", "size"), cycles=("expiry", "nunique"), mean_net_bp=("net_bp", "mean"),
                                          median_net_bp=("net_bp", "median"), hit_rate=("net_bp", lambda v: (v > 0).mean()),
                                          net_inr=("net_inr", "sum")).round(1).to_markdown(), ""]

out += ["## 3. Every config, full sample (in-sample; the trial set behind the Deflated Sharpe)", ""]
ins = t[~t.out_of_sample]
out += [ins.pivot_table(index="config", columns="pair", values="net_bp", aggfunc=["size", "mean"]).round(1).to_markdown(), ""]

out += ["## 4. Slippage sensitivity: mean net bp per trade at 0 / 1 / 3 / 10 ticks per order", ""]
scored = pd.concat([ins[ins.rule == "DRIFT"], t[t.out_of_sample]])
rows = []
for (pair, cfg), g in scored.groupby(["pair", "config"]):
    r = {"pair": pair, "strategy": cfg}
    for k in (0, 1, 3, 10):
        r[f"{k} ticks"] = (1e4 * (g.gross_inr - g.cost_fixed_inr - k * g.slip_per_tick_inr) / g.notional_inr).mean()
    rows.append(r)
out += [pd.DataFrame(rows).round(1).to_markdown(index=False), ""]

out += ["## 5. Delivery leg: held through settlement (Rs per gram, mean over expired cycles)", ""]
out += [ds.round(2).to_markdown(index=False), ""]

out += ["## 6. Delivery leg per cycle, entered on the last pre-tender day", ""]
cols = ["pair", "expiry", "entry_premium_bp", "settlement_gap_bp", "futures_inr_g", "making_received_inr_g", "making_paid_inr_g",
        "margin_funding_inr_g", "entry_costs_inr_g", "headroom_inr_g", "breakeven_coin_premium_pct", "retail_net_inr_g"]
out += [dc[dc.entry == "last pre-tender day"][cols].round(1).to_markdown(index=False), ""]

out += ["## 7. Delivery headroom without the two assumed costs (bar resale discount, logistics)", ""]
g = dc.assign(headroom_ex_assumed=dc.headroom_inr_g + dc.bar_discount_inr_g + dc.logistics_inr_g)
g["breakeven_ex_assumed_pct"] = 100 * g.headroom_ex_assumed / g.spot_inr_g
out += [g.groupby(["pair", "entry"])[["headroom_inr_g", "headroom_ex_assumed", "breakeven_coin_premium_pct", "breakeven_ex_assumed_pct"]]
        .mean().round(2).to_markdown(), ""]

out += ["## 8. Current contract regime without Jan-Mar 2026: every config (in-sample, contracts expiring Apr 2025 on)", ""]
crash = (pd.to_datetime(ins.entry_date) <= "2026-03-31") & (pd.to_datetime(ins.exit_date) >= "2026-01-01")
cur = ins[~crash & (pd.to_datetime(ins.expiry) >= "2025-04-01")]
tab = cur.pivot_table(index="config", columns="pair", values="net_bp", aggfunc=["mean", "size"]).round(1)
out += [tab.to_markdown(), "",
        "Configs with a positive mean: " + ", ".join(f"{k}: {v} of 10" for k, v in
            cur.groupby("pair").apply(lambda g: int((g.groupby("config").net_bp.mean() > 0).sum())).items()), ""]

out += ["## 9. Walk-forward by contract era (out-of-sample)", ""]
w2 = t[t.out_of_sample].assign(era=lambda d: np.where(pd.to_datetime(d.expiry) >= "2025-04-01", "Apr 2025 on", "before Apr 2025"))
out += [w2.groupby(["pair", "era"]).net_bp.agg(["size", "mean", "median"]).round(1).to_markdown(), ""]

out += ["## 10. Pre-registered forward test: walk-forward trades entered after 22 Oct 2026", ""]
fw = t[t.out_of_sample & (pd.to_datetime(t.entry_date) > "2026-10-22")]
out += [(fw[["pair", "expiry", "config_used", "entry_date", "exit_date", "direction", "net_bp"]].to_markdown(index=False)
         if len(fw) else "No forward trades yet."), ""]

(HERE / "m4_tables.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
