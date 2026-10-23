"""M4 walk-forward verdict on the same-expiry premium (pre-tender trading rules).

Trades are gram-matched spreads on one pair and one expiry: POSITION_G grams per leg (GOLDGUINEA 25 lots or
GOLDPETAL 200 lots against GOLDTEN 20 lots). direction +1 = short the premium (sell small, buy big).

Timing: a signal is decided on day t's close premium and filled at the next eligible day's VWAP (t+1). Every position
is closed by the last day before either leg's tender window; nothing is held into delivery here (see delivery.py).

Rules (the honest trial count is every config of every rule, per pair):
  DRIFT          short the premium at the first eligible day 60+ trading days out, exit before tender (no tuning)
  MR(W, k)       z = (premium - mean of the previous W eligible days) / their sd, within the cycle;
                 enter short when z > k, long when z < -k; exit when z crosses 0 or before tender.
                 W in {20, 40, 60}, k in {1.0, 1.5, 2.0}: 9 configs
Walk-forward: each calendar month uses the MR config with the best mean net bp over trades that had already closed
before the month began (at least MIN_TRAIN_TRADES); otherwise the middle config. Only those out-of-sample trades
are scored as "MR walk-forward".

Costs per order: statutory + broker preset + slippage in ticks (costs.py). P&L is split exactly into a spread leg
(the premium change on the entry notional) and a gold leg (the premium times the gold move).
"""
from itertools import product

import numpy as np
import pandas as pd
from scipy.stats import kurtosis, norm, skew

from . import costs, specs
from .checks import Report

PAIRS = ("GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN", "GOLDPETAL/GOLDGUINEA")
POSITION_G = 200
DRIFT_ENTRY_TDTE = 60
WINDOWS, THRESHOLDS = (20, 40, 60), (1.0, 1.5, 2.0)
DEFAULT_CFG = (40, 1.5)
MIN_TRAIN_TRADES = 5
N_BOOT, N_NULL, SEED = 10_000, 2_000, 20261023
CRASH = (pd.Timestamp("2026-01-01").date(), pd.Timestamp("2026-03-31").date())


def configs():
    return [("DRIFT", None, None)] + [("MR", w, k) for w, k in product(WINDOWS, THRESHOLDS)]


def cfg_name(rule, w, k):
    return "DRIFT" if rule == "DRIFT" else f"MR(W={w},k={k})"


# --- trade simulation ----------------------------------------------------------------------------

def series(conv, pair):
    """Eligible days of each cycle of a pair, in date order (the only days we decide or fill on)."""
    d = conv[(conv.pair == pair) & conv.eligible].sort_values(["expiry", "date"])
    return {x: g.reset_index(drop=True) for x, g in d.groupby("expiry")}


def signals_mr(g, w, k):
    p = g.premium_close_bp
    mu = p.shift(1).rolling(w).mean()
    sd = p.shift(1).rolling(w).std()
    return (p - mu) / sd


def simulate(g, rule, w=None, k=None):
    """Positions on one cycle's eligible days. Returns a list of (entry_row, exit_row, direction) fill indices."""
    n = len(g)
    trades, pos, entry, d = [], 0, None, 0
    if rule == "DRIFT":
        idx = np.flatnonzero(g.tdte.values >= DRIFT_ENTRY_TDTE)
        start = int(idx[0]) if len(idx) else 0
        if start + 1 < n - 1:
            trades.append((start + 1, n - 1, +1))
        return trades
    z = signals_mr(g, w, k).values
    for i in range(n - 1):                      # decide at close i, fill at i + 1
        force = i + 1 == n - 1                  # next eligible day is the last before tender
        if pos == 0:
            if force or np.isnan(z[i]):
                continue
            if z[i] > k:
                pos, d, entry = 1, +1, i + 1
            elif z[i] < -k:
                pos, d, entry = 1, -1, i + 1
        else:
            if force or (d == +1 and z[i] <= 0) or (d == -1 and z[i] >= 0):
                trades.append((entry, i + 1, d))
                pos = 0
    return trades


def price_trade(g, e, x, d, small, big, ticks=None):
    a, b = g.iloc[e], g.iloc[x]
    G = POSITION_G
    fs_e, fb_e, fs_x, fb_x = a.vwap_g999_s, a.vwap_g999_b, b.vwap_g999_s, b.vwap_g999_b
    gross = d * G * ((fb_x - fb_e) - (fs_x - fs_e))
    p_e, p_x = 1e4 * (fs_e / fb_e - 1), 1e4 * (fs_x / fb_x - 1)
    spread_leg = d * G * fb_e * (p_e - p_x) / 1e4
    qs, qb = specs.basis(small)["quote_g"], specs.basis(big)["quote_g"]
    sell_small_first = d == +1
    orders = [  # (value, side, units)
        (G * fs_e, "sell" if sell_small_first else "buy", G / qs), (G * fb_e, "buy" if sell_small_first else "sell", G / qb),
        (G * fs_x, "buy" if sell_small_first else "sell", G / qs), (G * fb_x, "sell" if sell_small_first else "buy", G / qb),
    ]
    fixed = sum(costs.order_cost_inr(v, sd, u, slippage_ticks=0)["total"] for v, sd, u in orders)
    slip_per_tick = sum(costs.order_cost_inr(v, sd, u, slippage_ticks=1)["slippage"] for v, sd, u in orders)
    t = costs.load()["slippage_ticks_per_order"]["base"] if ticks is None else ticks
    cost = fixed + t * slip_per_tick
    notional = G * fb_e
    return {"entry_date": a.date, "exit_date": b.date, "direction": d, "hold_days": x - e,
            "entry_tdte": int(a.tdte), "exit_tdte": int(b.tdte), "premium_entry_bp": p_e, "premium_exit_bp": p_x,
            "notional_inr": notional, "gross_inr": gross, "spread_leg_inr": spread_leg, "gold_leg_inr": gross - spread_leg,
            "cost_fixed_inr": fixed, "slip_per_tick_inr": slip_per_tick, "cost_inr": cost, "net_inr": gross - cost,
            "gross_bp": 1e4 * gross / notional, "cost_bp": 1e4 * cost / notional, "net_bp": 1e4 * (gross - cost) / notional}


def all_trades(conv):
    rows = []
    for pair in PAIRS:
        small, big = pair.split("/")
        for expiry, g in series(conv, pair).items():
            for rule, w, k in configs():
                for e, x, d in simulate(g, rule, w, k):
                    rows.append({"pair": pair, "expiry": expiry, "config": cfg_name(rule, w, k), "rule": rule,
                                 **price_trade(g, e, x, d, small, big)})
    return pd.DataFrame(rows)


def walk_forward(trades):
    """Pick an MR config each month from trades closed before that month; keep only those out-of-sample trades."""
    out = []
    for pair, t in trades[trades.rule == "MR"].groupby("pair"):
        t = t.assign(month=pd.to_datetime(t.entry_date).dt.to_period("M"))
        for m in sorted(t.month.unique()):
            start = m.to_timestamp().date()
            past = t[t.exit_date < start]
            perf = past.groupby("config").net_bp.agg(["mean", "size"])
            perf = perf[perf["size"] >= MIN_TRAIN_TRADES]
            choice = perf["mean"].idxmax() if len(perf) else cfg_name("MR", *DEFAULT_CFG)
            sel = t[(t.month == m) & (t.config == choice)]
            out.append(sel.assign(chosen_from=len(past)))
    wf = pd.concat(out, ignore_index=True).drop(columns="month")
    return wf.assign(config_used=wf.config, config="MR walk-forward")


# --- statistics ----------------------------------------------------------------------------------

def boot_ci(t, rng):
    """95% CI of the mean net bp per trade, resampling whole cycles."""
    groups = [g.net_bp.values for _, g in t.groupby("expiry")]
    if len(groups) < 2:
        return np.nan, np.nan
    means = []
    for _ in range(N_BOOT // 5):
        pick = rng.integers(0, len(groups), len(groups))
        v = np.concatenate([groups[i] for i in pick])
        means.append(v.mean())
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def random_entry_p(t, conv, rng):
    """Share of random-timing replicas (same cycles, hold lengths and directions) whose mean net bp >= the rule's."""
    ser = {(p, x): (g.vwap_g999_s.values, g.vwap_g999_b.values) for p in t.pair.unique() for x, g in series(conv, p).items()}
    total, count = np.zeros(N_NULL), 0
    for r in t.itertuples():
        fs, fb = ser[(r.pair, r.expiry)]
        hold = max(1, int(r.hold_days))
        hi = len(fb) - 1 - hold
        if hi < 1:
            continue
        e = rng.integers(1, hi + 1, size=N_NULL)
        x = e + hold
        gross = r.direction * ((fb[x] - fb[e]) - (fs[x] - fs[e])) / fb[e]
        total += 1e4 * gross - r.cost_bp
        count += 1
    if not count:
        return np.nan
    return float(((total / count) >= t.net_bp.mean()).mean())


def deflated_sharpe(sr, n_obs, sr_trials, sk, ku):
    """Bailey & Lopez de Prado (2014): probability the true Sharpe exceeds the best of N noise trials."""
    n = len(sr_trials)
    if n_obs < 3 or n < 2 or not np.isfinite(sr):
        return np.nan
    v = np.var(sr_trials, ddof=1)
    g = 0.5772156649
    sr0 = np.sqrt(v) * ((1 - g) * norm.ppf(1 - 1 / n) + g * norm.ppf(1 - 1 / (n * np.e)))
    den = np.sqrt(max(1e-12, 1 - sk * sr + (ku - 1) / 4 * sr ** 2))
    return float(norm.cdf((sr - sr0) * np.sqrt(n_obs - 1) / den))


def summarise(trades, wf, conv):
    rng = np.random.default_rng(SEED)
    rows = []
    sr_by = trades.groupby(["pair", "config"]).net_bp.agg(lambda v: v.mean() / v.std(ddof=1) if len(v) > 2 else np.nan)
    scored = pd.concat([trades[trades.rule == "DRIFT"], wf], ignore_index=True)
    for (pair, cfg), t in scored.groupby(["pair", "config"]):
        if t.empty:
            continue
        lo, hi = boot_ci(t, rng)
        ex = t[~((t.entry_date <= CRASH[1]) & (t.exit_date >= CRASH[0]))]
        ex_lo, ex_hi = boot_ci(ex, rng) if len(ex) else (np.nan, np.nan)
        sr = t.net_bp.mean() / t.net_bp.std(ddof=1) if len(t) > 2 else np.nan
        gross_minus_fixed = (t.gross_inr - t.cost_fixed_inr).sum()
        rows.append({
            "pair": pair, "strategy": cfg, "trades": len(t), "cycles": t.expiry.nunique(),
            "first_entry": t.entry_date.min(), "last_exit": t.exit_date.max(),
            "mean_gross_bp": t.gross_bp.mean(), "mean_cost_bp": t.cost_bp.mean(), "mean_net_bp": t.net_bp.mean(),
            "ci_lo_bp": lo, "ci_hi_bp": hi, "hit_rate": float((t.net_bp > 0).mean()),
            "total_net_inr": t.net_inr.sum(), "spread_leg_share": t.spread_leg_inr.sum() / t.gross_inr.sum() if t.gross_inr.sum() else np.nan,
            "sharpe_per_trade": sr,
            "deflated_sharpe_prob": deflated_sharpe(sr, len(t), sr_by.loc[pair].dropna().values,
                                                    skew(t.net_bp), kurtosis(t.net_bp, fisher=False)) if len(t) > 2 else np.nan,
            # DRIFT's timing is fixed by rule and spans almost the whole cycle, so random replicas tie with it: not applicable
            "random_entry_p": np.nan if cfg == "DRIFT" else random_entry_p(t, conv, rng),
            "mean_net_bp_ex_crash": ex.net_bp.mean() if len(ex) else np.nan, "trades_ex_crash": len(ex),
            "ex_crash_ci_lo_bp": ex_lo, "ex_crash_ci_hi_bp": ex_hi,
            "breakeven_slippage_ticks": gross_minus_fixed / t.slip_per_tick_inr.sum() if t.slip_per_tick_inr.sum() else np.nan,
            "trials_per_pair": len(configs()),
        })
    return pd.DataFrame(rows)


def build(conv, report=None):
    report = report or Report()
    trades = all_trades(conv)
    wf = walk_forward(trades)
    summ = summarise(trades, wf, conv)
    report.add("backtest.trades", "info", n=len(trades),
               note=f"Simulated trades across {len(configs())} configs x {len(PAIRS)} pairs; {len(wf)} walk-forward out-of-sample")
    return {"wf_trades": pd.concat([trades.assign(out_of_sample=False), wf.assign(out_of_sample=True)], ignore_index=True),
            "wf_summary": summ}, report
