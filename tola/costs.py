"""Order costs from data/specs/costs.yaml: statutory charges, broker preset, and tick-based slippage."""
from functools import lru_cache
from pathlib import Path

import yaml

COSTS_FILE = Path(__file__).resolve().parent.parent / "data" / "specs" / "costs.yaml"


@lru_cache(maxsize=1)
def load():
    return yaml.safe_load(COSTS_FILE.read_text(encoding="utf-8"))


def order_cost_inr(value_inr, side, units, broker="zerodha", slippage_ticks=None):
    """Rs cost of one executed order. value_inr: order value; side: 'buy' or 'sell';
    units: quantity in quote units (lots x lot_g / quote_g), for tick slippage."""
    c = load()
    st, br = c["statutory"], c["brokers"][broker]
    ticks = c["slippage_ticks_per_order"]["base"] if slippage_ticks is None else slippage_ticks
    brokerage = min(br["pct"] / 100 * value_inr, br["cap_inr"])
    txn = st["exchange_txn_pct"] / 100 * value_inr
    sebi = st["sebi_inr_per_crore"] * value_inr / 1e7
    gst = st["gst_pct_on_fees"] / 100 * (brokerage + txn + sebi)
    tax = st["ctt_sell_pct"] / 100 * value_inr if side == "sell" else st["stamp_buy_pct"] / 100 * value_inr
    slip = ticks * c["tick_inr_per_quote_unit"] * units
    return {"brokerage": brokerage, "exchange": txn, "sebi": sebi, "gst": gst, "tax": tax, "slippage": slip,
            "total": brokerage + txn + sebi + gst + tax + slip}
