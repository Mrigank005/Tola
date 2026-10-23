"""M5 alert log (quiet by default) and contract calendar.

An alert fires on the day a condition *starts*, not on every day it stays true, so a calm market produces an
almost empty log. That emptiness is the point: M4 found the only tradeable signal is a swing in the premium,
and swings are rare outside episodes like Jan-Mar 2026.

  swing        same-reference pair (GOLDGUINEA or GOLDPETAL vs GOLDTEN, same expiry): the premium moves beyond
               SWING_K sd of its previous SWING_W eligible days (the M4 mean-reversion signal, W=40, k=1.5).
               Checked on the pair's most liquid live expiry each day.
  tender       a live contract is TENDER_NOTICE trading days from its tender window: exit-by date in the alert.
  control      GOLD vs GOLDM (same expiry, should be ~0) moves beyond CONTROL_BP.
  settlement   a same-reference pair settled more than SETTLE_BP apart per gram (e.g. GOLDPETAL on 30 Jan 2026).
"""
import numpy as np
import pandas as pd

SWING_W, SWING_K = 40, 1.5
TENDER_NOTICE = 5
CONTROL_BP = 10.0
SETTLE_BP = 20.0
LOG_FROM = pd.Timestamp("2025-04-01").date()
SAME_REF = ["GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN"]


def _onsets(flag):
    """True on days a condition switches on."""
    return flag & ~flag.shift(1, fill_value=False)


def swing_alerts(conv):
    out = []
    for pair in SAME_REF:
        d = conv[(conv.pair == pair) & conv.eligible].sort_values(["expiry", "date"]).copy()
        p = d.premium_close_bp
        g = d.groupby("expiry")
        mu = g.premium_close_bp.transform(lambda s: s.shift(1).rolling(SWING_W).mean())
        sd = g.premium_close_bp.transform(lambda s: s.shift(1).rolling(SWING_W).std())
        d["z"] = (p - mu) / sd
        d["mu"] = mu
        d["liq"] = d[["value_lakh_s", "value_lakh_b"]].min(axis=1)
        front = d.loc[d.groupby("date").liq.idxmax()].sort_values("date")      # most liquid expiry each day
        front = front[front.z.notna()]
        for side, flag in (("high", front.z > SWING_K), ("low", front.z < -SWING_K)):
            for r in front[_onsets(flag.reset_index(drop=True)).values].itertuples():
                small = pair.split("/")[0]
                out.append({"date": r.date, "type": "swing", "severity": "caution", "subject": pair, "expiry": r.expiry,
                            "title": f"{small} premium unusually {side}",
                            "detail": f"{r.premium_close_bp:+.0f} bp over GOLDTEN ({r.expiry:%b %Y}), vs {r.mu:+.0f} bp average of the last {SWING_W} days (z = {r.z:+.1f})",
                            "value_bp": r.premium_close_bp})
    return out


def control_alerts(conv):
    d = conv[(conv.pair == "GOLD/GOLDM") & conv.eligible].copy()
    d["liq"] = d[["value_lakh_s", "value_lakh_b"]].min(axis=1)
    front = d.loc[d.groupby("date").liq.idxmax()].sort_values("date").reset_index(drop=True)
    out = []
    for r in front[_onsets(front.premium_close_bp.abs() > CONTROL_BP)].itertuples():
        out.append({"date": r.date, "type": "control", "severity": "info", "subject": "GOLD/GOLDM", "expiry": r.expiry,
                    "title": "Control pair away from zero",
                    "detail": f"GOLD (1 kg) vs GOLDM (100 g), {r.expiry:%b %Y}: {r.premium_close_bp:+.0f} bp; it should sit near 0",
                    "value_bp": r.premium_close_bp})
    return out


def tender_alerts(contracts, trading_days, asof):
    """Notice day = TENDER_NOTICE trading days before the tender opens: counted on the observed MCX calendar when the
    tender date is inside it, on weekdays when it is in the future. Only notices that have arrived are logged."""
    cal = np.array(sorted(trading_days), dtype="datetime64[D]")
    out = []
    for r in contracts.itertuples():
        if r.tender_start is None or pd.isna(r.tender_start):
            continue
        ts = np.datetime64(r.tender_start)
        if ts <= cal[-1]:
            idx = int(np.searchsorted(cal, ts))
            if idx - TENDER_NOTICE < 0:
                continue
            day = cal[idx - TENDER_NOTICE].astype("datetime64[D]").item()
            exit_by = cal[idx - 1].astype("datetime64[D]").item()
        else:
            day = np.busday_offset(ts, -TENDER_NOTICE, roll="backward").astype("datetime64[D]").item()
            exit_by = np.busday_offset(ts, -1, roll="backward").astype("datetime64[D]").item()
        if day > asof:
            continue
        out.append({"date": day, "type": "tender", "severity": "info", "subject": r.symbol, "expiry": r.expiry,
                    "title": f"{r.symbol} {r.expiry:%b %Y}: tender window in {TENDER_NOTICE} trading days",
                    "detail": f"Tender opens {pd.Timestamp(r.tender_start):%d %b %Y}" + (f"; exit by {pd.Timestamp(exit_by):%d %b %Y} to avoid delivery" if exit_by else ""),
                    "value_bp": np.nan})
    return out


def settlement_alerts(cycles):
    out = []
    c = cycles[cycles.pair.isin(SAME_REF) & cycles.settlement_gap_bp.notna() & (cycles.settlement_gap_bp.abs() > SETTLE_BP)]
    for r in c.itertuples():
        small = r.pair.split("/")[0]
        out.append({"date": r.last_trading_day, "type": "settlement", "severity": "caution", "subject": r.pair, "expiry": r.expiry,
                    "title": f"{small} settled {r.settlement_gap_bp:+.0f} bp away from GOLDTEN",
                    "detail": "Same settlement rule, different poll: the spot polls were taken at different times on the settlement day",
                    "value_bp": r.settlement_gap_bp})
    return out


def build(conv, contracts, cycles, trading_days, asof):
    a = pd.DataFrame(swing_alerts(conv) + control_alerts(conv) + settlement_alerts(cycles)
                     + tender_alerts(contracts[contracts.expiry >= LOG_FROM], trading_days, asof))
    a = a[(a.date >= LOG_FROM) & (a.date <= asof)].sort_values(["date", "type"], ascending=[False, True]).reset_index(drop=True)
    days = [d for d in trading_days if LOG_FROM <= d <= asof]
    quiet = len(set(days) - set(a.date))
    return a, {"from": str(LOG_FROM), "to": str(asof), "trading_days": len(days), "alert_days": len(set(a.date)), "quiet_days": quiet,
               "by_type": a.type.value_counts().to_dict()}


def calendar(contracts, live_inputs):
    """Every live contract with its key dates, nearest first; turnover where it traded on the latest day."""
    c = contracts[contracts.status == "live"][["symbol", "expiry", "first_date", "tender_start", "last_trading_day", "tender_days"]].copy()
    c["exit_by"] = [np.busday_offset(np.datetime64(t), -1, roll="backward").astype("datetime64[D]").item() for t in c.tender_start]
    liq = live_inputs.set_index(["symbol", "expiry"])[["value_lakh", "thin"]]
    c = c.join(liq, on=["symbol", "expiry"])
    c["traded_latest_day"] = c.value_lakh.notna()
    c["thin"] = c.thin.astype("boolean").fillna(True).astype(bool)
    return c.rename(columns={"first_date": "first_traded"}).sort_values(["last_trading_day", "symbol"]).reset_index(drop=True)
