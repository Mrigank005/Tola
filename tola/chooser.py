"""M5 "Which contract?" chooser: the effective cost of holding gold through each live MCX gold contract.

The user is a buyer: "I want G grams of gold exposure for H trading days" (exit before tender), or "I want G grams
delivered" (hold to settlement). For every symbol, the nearest live expiry that fits is costed per gram:

  exit before tender                         take delivery
  - trading costs, entry + exit orders       - trading costs, entry order
  - premium change: the expected change in   - premium paid: today's residual (M2), lost in full at
    the premium over GOLDTEN (same expiry)     settlement because the contract settles to spot (M3)
    over H days, from history (+/- 1 sd
    shown as risk); 0 for the reference
    contracts GOLDTEN, GOLDM, GOLD
  - net carry: (implied carry - risk-free)    - net carry: (implied carry - risk-free) x days to
    x calendar days held                       settlement. A futures buyer keeps the cash and earns
                                               the risk-free rate on it, so only the excess is a cost.
                                             - making charge (spec), GST 3%, tender + delivery margin funding,
                                               vault/assay/transport (assumed)

Net carry is the price of holding gold through a futures contract instead of in hand. It is the same for every
symbol with the same holding period, so it never changes the ranking; it is shown because it changes the decision
against buying physical gold. For delivery, the result is also compared with buying the coin outright (cheapest observed
retail price, data/specs/costs.yaml).

All the inputs come from the snapshot, and export.py writes them to JSON so the web app can run the same formula.
"""
from dataclasses import dataclass

import numpy as np
import pandas as pd

from . import costs, specs

HORIZONS = (5, 10, 20, 40, 60)
CURRENT_ERA = pd.Timestamp("2025-04-01").date()   # first contracts under today's small-lot specs (M1-M4)
GST_PCT = 3.0
MIN_TURNOVER_LAKH = 100                            # Rs 1 crore on the latest day, else marked thin
MAX_SIZE_GAP = 0.10                                # whole lots must land within 10% of the grams asked for


@dataclass
class Request:
    grams: float = 100
    hold_days: int = 20            # trading days; for delivery, the earliest acceptable settlement
    take_delivery: bool = False
    broker: str = "zerodha"
    slippage_ticks: float | None = None


# --- inputs -------------------------------------------------------------------------------------

def premium_changes(conv):
    """How the small contracts' premium over GOLDTEN (same expiry, M3) changes over H eligible trading days, current
    contract era. This is measured directly from same-expiry prices, with no curve model. GOLDTEN, GOLDM and GOLD
    are the reference contracts (their residual is about 0, M2), so their premium change is taken as 0."""
    d = conv[conv.eligible & conv.pair.isin(["GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN"]) & (conv.expiry >= CURRENT_ERA)]
    d = d.sort_values(["pair", "expiry", "date"])
    rows = []
    for pair, g in d.groupby("pair"):
        for h in HORIZONS:
            ch = g.groupby("expiry").premium_vwap_bp.transform(lambda s: s.shift(-h) - s).dropna()
            rows.append({"symbol": pair.split("/")[0], "horizon": h, "mean_bp": ch.mean(), "sd_bp": ch.std(),
                         "p10_bp": ch.quantile(0.1), "p90_bp": ch.quantile(0.9), "n": int(len(ch))})
    return pd.DataFrame(rows)


def live_inputs(basis, contracts, curve):
    """One row per live contract on the latest trading day, with everything the formula needs."""
    asof = basis.date.max()
    live = contracts[contracts.status == "live"][["symbol", "expiry", "last_trading_day", "tender_start", "tender_days"]]
    x = basis[basis.date == asof].merge(live, on=["symbol", "expiry"], suffixes=("", "_c"))
    x["last_trading_day"] = x.last_trading_day_c
    x = x.drop(columns=[c for c in x.columns if c.endswith("_c")])
    b = pd.DataFrame({s: specs.basis(s) for s in specs.symbols()}).T
    x = x.join(b[["lot_g", "quote_g"]], on="symbol")
    # exit-by: the last trading day before the tender window opens (weekday count; future holidays not known)
    x["exit_by"] = [np.busday_offset(np.datetime64(t), -1, roll="backward").astype("datetime64[D]").item() for t in x.tender_start]
    x["days_to_exit_by"] = [int(np.busday_count(np.datetime64(asof), np.datetime64(e))) for e in x.exit_by]
    x["days_to_settle"] = [int(np.busday_count(np.datetime64(asof), np.datetime64(t))) for t in x.last_trading_day]
    cv = curve.set_index("date").loc[asof]
    x["carry_pa"] = cv.carry_pa
    x["rf_pct"] = cv.rf_pct
    x["thin"] = x.value_lakh < MIN_TURNOVER_LAKH
    cols = ["symbol", "expiry", "last_trading_day", "tender_start", "tender_days", "exit_by", "days_to_exit_by", "days_to_settle",
            "lot_g", "quote_g", "close_g999", "fair_g999", "residual_bp", "carry_pa", "rf_pct", "value_lakh", "thin",
            "making_charge_inr_g", "tender_margin_pct"]
    return x[cols].sort_values(["symbol", "expiry"]).reset_index(drop=True), asof


# --- the formula --------------------------------------------------------------------------------

def _change_stats(changes, symbol, h):
    """Expected residual change over h trading days, interpolated between the measured horizons."""
    c = changes[changes.symbol == symbol].set_index("horizon").sort_index()
    if c.empty:
        return 0.0, 0.0
    hs = c.index.values.astype(float)
    return float(np.interp(h, hs, c.mean_bp.values)), float(np.interp(h, hs, c.sd_bp.values))


ASOF = [None]   # set by quote(): the snapshot's latest trading day


def quote(req: Request, live: pd.DataFrame, changes: pd.DataFrame, asof):
    ASOF[0] = asof
    cfg = costs.load()
    dlv = cfg["delivery"]
    rows = []
    for sym, g in live.groupby("symbol"):
        need = "days_to_settle" if req.take_delivery else "days_to_exit_by"
        fits = g[g[need] >= req.hold_days].sort_values("expiry")
        row = {"symbol": sym, "lot_g": int(g.lot_g.iloc[0])}
        if fits.empty:
            rows.append({**row, "feasible": False, "reason": "no live expiry is far enough out for this holding period"})
            continue
        c = fits.iloc[0]
        lots = int(round(req.grams / c.lot_g))
        grams = lots * c.lot_g
        if lots < 1 or abs(grams - req.grams) / req.grams > MAX_SIZE_GAP:
            rows.append({**row, "expiry": c.expiry, "feasible": False,
                         "reason": f"trades in {int(c.lot_g)} g lots; {req.grams:g} g can't be matched within 10%"})
            continue

        S = float(c.fair_g999)                       # Rs/g reference used to value bp terms
        price = float(c.close_g999)
        notional = grams * price
        units = grams / c.quote_g
        entry = costs.order_cost_inr(notional, "buy", units, req.broker, req.slippage_ticks)["total"]
        days = int(c.days_to_settle if req.take_delivery else req.hold_days)
        end = c.last_trading_day if req.take_delivery else np.busday_offset(np.datetime64(ASOF[0]), days, roll="forward").astype("datetime64[D]").item()
        cal_days = (pd.Timestamp(end) - pd.Timestamp(ASOF[0])).days   # carry was fitted on calendar days / 365
        net_carry = float(c.carry_pa) - float(c.rf_pct) / 100
        lines = {"trading": entry, "net_carry": notional * net_carry * cal_days / 365}
        if req.take_delivery:
            lines["premium"] = notional * float(c.residual_bp) / 1e4
            mc = float(c.making_charge_inr_g) if pd.notna(c.making_charge_inr_g) else 0.0
            lines["making_charge"] = mc * grams
            lines["gst"] = GST_PCT / 100 * notional
            rate = float(c.rf_pct) / 100
            tm = (float(c.tender_margin_pct) if pd.notna(c.tender_margin_pct) else 8.34) / 100
            lines["margin_funding"] = notional * rate * (tm * int(c.tender_days) + dlv["delivery_margin_pct"] / 100 * dlv["delivery_margin_days"]) / 365
            lines["logistics"] = dlv["vault_assay_transport_inr_per_g"] * grams
            risk = 0.0
        else:
            exit_ = costs.order_cost_inr(notional, "sell", units, req.broker, req.slippage_ticks)["total"]
            lines["trading"] += exit_
            mean_bp, sd_bp = _change_stats(changes, sym, req.hold_days)
            lines["premium"] = -notional * mean_bp / 1e4         # a falling premium costs the holder
            risk = notional * sd_bp / 1e4
        total = sum(lines.values())
        rows.append({**row, "expiry": c.expiry, "feasible": True, "reason": "thin turnover today" if c.thin else "",
                     "lots": lots, "grams": grams, "price_g999": price, "notional_inr": notional,
                     "residual_bp": float(c.residual_bp), "carry_pa": float(c.carry_pa), "rf_pct": float(c.rf_pct),
                     "exit_by": None if req.take_delivery else c.exit_by, "tender_start": c.tender_start,
                     "settles": c.last_trading_day, "days_held": days, "calendar_days": cal_days,
                     **{f"{k}_inr": v for k, v in lines.items()}, "total_inr": total,
                     "total_inr_g": total / grams, "total_bp": 1e4 * total / notional,
                     "premium_risk_inr": risk, "premium_risk_inr_g": risk / grams})
    out = pd.DataFrame(rows)
    ok = out[out.feasible].sort_values("total_inr_g")
    out = pd.concat([ok.assign(rank=range(1, len(ok) + 1)), out[~out.feasible]], ignore_index=True)
    if req.take_delivery:
        prem = dlv["retail_coin_premium_pct"]
        out["retail_coin_alt_inr_g"] = [
            float(r.price_g999) * (prem.get(r.symbol, np.nan) / 100 + GST_PCT / 100) if r.feasible and r.symbol in prem else np.nan
            for r in out.itertuples()]
    return out
