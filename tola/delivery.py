"""M4 delivery leg: the only position that collects the whole premium is one held through settlement.

Per expired same-reference cycle (GOLDGUINEA/GOLDTEN, GOLDPETAL/GOLDTEN), gram-matched, all in Rs per gram:
  short the small contract, long GOLDTEN, entered either early (cycle mean premium 60+ trading days out) or on the
  last day before tender; both legs go to settlement.

  futures      (entry premium - settlement gap) x S          both legs settle to their DDR, gold moves cancel
  making       + small contract's making charge (received)   the short delivers and is paid it by the buyer
               - GOLDTEN's making charge (paid)              the long takes the 10 g bars and pays it
  bars         - resale discount on the 10 g bars received
  logistics    - vault, assay and transport
  margin       - 8.34% tender margin over the tender days and 25% delivery margin to pay-in, both legs, at the risk-free rate
  entry costs  - statutory + brokerage + slippage on the two entry orders
  = headroom before buying the coins to deliver.

breakeven_coin_premium_pct = headroom / S: the most a deliverer can pay over spot for the coins and still break even.
The retail benchmark (Augmont, 13 Oct 2026) is in data/specs/costs.yaml. GST (3% on delivered gold) is collected and
paid at both ends; it nets out only for a GST-registered participant, which is assumed here.
"""
import numpy as np
import pandas as pd

from . import costs, specs
from .backtest import POSITION_G

PAIRS = ("GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN")
ENTRIES = {"early (60+ days)": "vwap_60+_bp", "last pre-tender day": "last_premium_vwap_bp"}


def entry_cost_per_g(small, big, s_price, b_price):
    c = costs.load()
    qs, qb = specs.basis(small)["quote_g"], specs.basis(big)["quote_g"]
    g = POSITION_G
    sell = costs.order_cost_inr(g * s_price, "sell", g / qs)["total"]
    buy = costs.order_cost_inr(g * b_price, "buy", g / qb)["total"]
    return (sell + buy) / g


def build(cycles, curve):
    d = costs.load()["delivery"]
    rf = curve.set_index("date").rf_pct.sort_index()
    rows = []
    sel = cycles[cycles.pair.isin(PAIRS) & (cycles.status == "expired") & cycles.counts]
    for r in sel.to_dict("records"):
        small, big = r["pair"].split("/")
        if not np.isfinite(r["settlement_gap_bp"]):
            continue
        S = r["last_big_g999"]
        vs, vb = specs.version_for(small, r["expiry"]), specs.version_for(big, r["expiry"])
        mc_s = (vs or {}).get("making_charge_inr_per_g") or 0.0
        mc_b = (vb or {}).get("making_charge_inr_per_g") or 0.0
        tender_days = (vs or specs.first_version(small))["tender"]["days"]
        tender_margin = (vs or specs.first_version(small))["tender"]["margin_pct"] / 100
        rate = rf[rf.index <= r["last_trading_day"]].iloc[-1] / 100
        funding = 2 * S * rate * (tender_margin * tender_days + d["delivery_margin_pct"] / 100 * d["delivery_margin_days"]) / 365
        for label, col in ENTRIES.items():
            prem = r[col]
            if not np.isfinite(prem):
                continue
            futures = (prem - r["settlement_gap_bp"]) / 1e4 * S
            entry = entry_cost_per_g(small, big, S * (1 + prem / 1e4), S)
            headroom = (futures + mc_s - mc_b - d["bar_resale_discount_pct"] / 100 * S
                        - d["vault_assay_transport_inr_per_g"] - funding - entry)
            retail = d["retail_coin_premium_pct"].get(small)
            rows.append({
                "pair": r["pair"], "expiry": r["expiry"], "entry": label, "entry_premium_bp": prem,
                "settlement_gap_bp": r["settlement_gap_bp"], "spot_inr_g": S,
                "futures_inr_g": futures, "making_received_inr_g": mc_s, "making_paid_inr_g": mc_b,
                "bar_discount_inr_g": d["bar_resale_discount_pct"] / 100 * S, "logistics_inr_g": d["vault_assay_transport_inr_per_g"],
                "margin_funding_inr_g": funding, "entry_costs_inr_g": entry,
                "headroom_inr_g": headroom, "breakeven_coin_premium_pct": 100 * headroom / S,
                "retail_coin_premium_pct": retail,
                "retail_net_inr_g": headroom - retail / 100 * S if retail is not None else np.nan,
            })
    cyc = pd.DataFrame(rows)
    summ = (cyc.groupby(["pair", "entry"])
            .agg(cycles=("expiry", "size"), entry_premium_bp=("entry_premium_bp", "mean"),
                 futures_inr_g=("futures_inr_g", "mean"), making_net_inr_g=("making_received_inr_g", "mean"),
                 headroom_inr_g=("headroom_inr_g", "mean"),
                 breakeven_coin_premium_pct=("breakeven_coin_premium_pct", "mean"),
                 breakeven_min_pct=("breakeven_coin_premium_pct", "min"), breakeven_max_pct=("breakeven_coin_premium_pct", "max"),
                 retail_coin_premium_pct=("retail_coin_premium_pct", "first"), retail_net_inr_g=("retail_net_inr_g", "mean"),
                 retail_profitable_share=("retail_net_inr_g", lambda v: float((v > 0).mean())))
            .reset_index())
    summ["making_net_inr_g"] = summ.making_net_inr_g - cyc.groupby(["pair", "entry"]).making_paid_inr_g.mean().values
    return {"delivery_cycles": cyc, "delivery_summary": summ}
