"""M2 Basis Anatomy: for every traded contract-day, a waterfall from the futures price to an unexplained residual.

All terms are in basis points of log price, relative to the Ahmedabad 999 polled spot of the same day (S_ref,
GOLDM's spot x 999/995, which equals GOLDTEN's published spot). They add up exactly:

    basis_total = 1e4 ln(F / S_ref)        F: futures close, Rs per gram at 999 (unit step done in M1)
                = timing                   common level of the day: spot is polled ~5-6 pm, the futures close is the
                                           last half hour to ~11:30 pm, so overnight moves land here for every contract
                + carry                    r_t x tau: r_t is the day's implied carry, fitted on GOLD and GOLDM (big-lot
                                           benchmark curve); tau runs to the contract's effective settlement date
                + reference                1e4 ln(S_own / S_ref): Mumbai vs Ahmedabad spot (GOLDPETAL); 0 elsewhere
                + residual                 what no mechanical term explains: the small-lot premium

timing and carry come from one regression per day on the benchmark contracts: basis_total = timing + r_t * tau.
GOLD and GOLDM settle to a 3-day average of polls, which moves their effective settlement date about a day earlier;
that enters through tau, so "single poll vs 3-day average" is priced as carry, as it should be.

Delivery terms (making charge, delivery unit, tender margin) are paid outside the futures price: the buyer pays the
making charge on top of the DDR the futures converge to. They are reported next to the residual, not subtracted.
GOLDTEN is the test: it carries a Rs 30/g making charge (~20 bp) yet its residual is near zero.
"""
import numpy as np
import pandas as pd

from . import rates, specs
from .checks import Report

BENCH = ("GOLD", "GOLDM")
MIN_VALUE_LAKH = 100        # Rs 1 crore of turnover for a benchmark contract to enter the day's curve
CARRY_FFILL_DAYS = 10       # reuse the last fitted carry for at most this many trading days
FIT_RMSE_WARN_BP = 40.0
REF_ROLL_DAYS = 20          # Mumbai-Ahmedabad spot gap: rolling median when either poll is stale


def daily_spot(spot):
    """Last poll per product per day, with the previous good value carried over stale or missing days."""
    last = spot.sort_values("ts").groupby(["product", "date"]).tail(1)
    wide = last.pivot(index="date", columns="product", values="price_g999")
    stale = last.pivot(index="date", columns="product", values="stale").astype("boolean").fillna(True).astype(bool)
    return wide, stale


def effective_settlement(fut):
    """Date the contract's settlement price is struck: the last trading day, or for 3-day-average contracts the
    mean of their three poll days (weekday approximation)."""
    ltd = pd.to_datetime(fut.last_trading_day).values.astype("datetime64[D]")
    three = fut.symbol.isin([s for s in specs.symbols() if specs.first_version(s)["ddr"]["rule"] == "avg_last_poll_3d"])
    back1 = np.busday_offset(ltd, -1, roll="backward")
    back2 = np.busday_offset(ltd, -2, roll="backward")
    mean_back = ((ltd - back1).astype(int) + (ltd - back2).astype(int)) / 3.0
    return pd.Series(np.where(three, mean_back, 0.0), index=fut.index)


def fit_curves(f, report):
    """Per day: OLS of basis_total on tau over the liquid benchmark contracts -> (timing, carry)."""
    b = f[f.symbol.isin(BENCH) & f.traded & (f.value_lakh >= MIN_VALUE_LAKH) & ~f.in_tender & (f.tau > 0)]
    out = []
    for d, g in b.groupby("date"):
        if g.tau.round(4).nunique() >= 2:
            slope, icpt = np.polyfit(g.tau, g.basis_total_bp, 1)
            rmse = float(np.sqrt(np.mean((g.basis_total_bp - icpt - slope * g.tau) ** 2)))
            out.append({"date": d, "timing_bp": icpt, "carry_pa": slope / 1e4, "fit_contracts": len(g), "fit_rmse_bp": rmse, "carry_source": "fit"})
        else:
            out.append({"date": d, "timing_bp": np.nan, "carry_pa": np.nan, "fit_contracts": len(g), "fit_rmse_bp": np.nan, "carry_source": "none"})
    c = pd.DataFrame(out).set_index("date").reindex(sorted(f.date.unique()))
    c["fit_contracts"] = c.fit_contracts.fillna(0).astype(int)
    c["carry_source"] = c.carry_source.fillna("none")

    # Days without a usable fit: carry forward r for a few days, re-level the timing term on whatever benchmark traded.
    filled = c.carry_pa.ffill(limit=CARRY_FFILL_DAYS)
    gap = c.carry_pa.isna() & filled.notna()
    c.loc[gap, "carry_source"] = "carried"
    c["carry_pa"] = filled
    for d in c.index[gap]:
        g = b[b.date == d]
        if len(g):
            c.loc[d, "timing_bp"] = float(np.median(g.basis_total_bp - 1e4 * c.loc[d, "carry_pa"] * g.tau))
    c.loc[c.timing_bp.isna(), "carry_source"] = "none"

    n_fit, n_car, n_none = (c.carry_source == "fit").sum(), (c.carry_source == "carried").sum(), (c.carry_source == "none").sum()
    report.add("anatomy.curve_days", "info", n=int(n_fit),
               note=f"Days with a fitted benchmark curve; {n_car} more reuse the previous carry; {n_none} have no curve")
    wide = c[c.fit_rmse_bp > FIT_RMSE_WARN_BP]
    for d, r in wide.head(5).iterrows():
        report.add("anatomy.loose_fit", "warn", f"{d}: rmse {r.fit_rmse_bp:.0f} bp over {r.fit_contracts} contracts",
                   f"Benchmark contracts sit more than {FIT_RMSE_WARN_BP:.0f} bp off a straight carry line ({len(wide)} days)")
    if wide.empty:
        report.ok("anatomy.loose_fit", f"Benchmark curve fits within {FIT_RMSE_WARN_BP:.0f} bp rmse on every fitted day")
    return c


def build(fut, spot, report=None):
    report = report or Report()
    S, stale = daily_spot(spot)
    f = fut[fut.traded].copy()
    f["ref_spot_g999"] = f.date.map(S["GOLDM"].ffill())
    f["ref_spot_stale"] = f.date.map(stale["GOLDM"]).astype("boolean").fillna(True).astype(bool)

    own_prod = {s: specs.spot(s)["product"] for s in specs.symbols()}
    gap_bp = {}
    for s, prod in own_prod.items():
        raw = 1e4 * np.log(S[prod] / S["GOLDM"])
        fresh = raw.where(~stale[prod] & ~stale["GOLDM"])
        gap_bp[s] = fresh.fillna(fresh.rolling(REF_ROLL_DAYS, min_periods=3).median()).fillna(0.0)
    f["reference_bp"] = [gap_bp[s].get(d, 0.0) for s, d in zip(f.symbol, f.date)]
    f["own_spot_g999"] = f.ref_spot_g999 * np.exp(f.reference_bp / 1e4)

    f["settle_shift_days"] = effective_settlement(f)
    f["tau_days"] = (pd.to_datetime(f.last_trading_day) - pd.to_datetime(f.date)).dt.days - f.settle_shift_days
    f["tau"] = f.tau_days.clip(lower=0) / 365.0
    f["basis_total_bp"] = 1e4 * np.log(f.close_g999 / f.ref_spot_g999)
    f["own_basis_bp"] = f.basis_total_bp - f.reference_bp

    curve = fit_curves(f, report)
    f = f.join(curve[["timing_bp", "carry_pa", "carry_source"]], on="date")
    f["carry_bp"] = 1e4 * f.carry_pa * f.tau
    f["residual_bp"] = f.basis_total_bp - f.timing_bp - f.carry_bp - f.reference_bp
    f["fair_g999"] = f.ref_spot_g999 * np.exp((f.timing_bp + f.carry_bp + f.reference_bp) / 1e4)

    # Delivery terms, reported beside the residual (not subtracted)
    ver = {(s, x): specs.version_for(s, x) for s, x in f[["symbol", "expiry"]].drop_duplicates().itertuples(index=False)}
    mc = [(ver[(s, x)] or {}).get("making_charge_inr_per_g") for s, x in zip(f.symbol, f.expiry)]
    f["making_charge_inr_g"] = pd.array(mc, dtype="Float64")
    f["making_charge_bp"] = 1e4 * np.log1p(f.making_charge_inr_g.astype(float) / f.own_spot_g999)
    f["tender_margin_pct"] = [(ver[(s, x)] or {}).get("tender", {}).get("margin_pct") for s, x in zip(f.symbol, f.expiry)]

    ident = (f.timing_bp + f.carry_bp + f.reference_bp + f.residual_bp - f.basis_total_bp).abs().max()
    if not (ident < 1e-6 or np.isnan(ident)):
        report.add("anatomy.waterfall_identity", "error", f"max gap {ident}", "Components do not add up to the total basis")
    else:
        report.ok("anatomy.waterfall_identity", "timing + carry + reference + residual = total basis on every row")

    rf = rates.rates_daily(curve.index)
    curve = curve.join(rf.set_index("date"))
    curve["carry_minus_rf_pct"] = 100 * curve.carry_pa - curve.rf_pct
    curve["ref_spot_g999"] = S["GOLDM"].ffill().reindex(curve.index)

    cols = ["date", "symbol", "expiry", "last_trading_day", "tdte", "in_tender", "tau_days", "value_lakh",
            "close_g999", "ref_spot_g999", "ref_spot_stale", "own_spot_g999", "fair_g999",
            "basis_total_bp", "own_basis_bp", "timing_bp", "carry_bp", "reference_bp", "residual_bp", "carry_source",
            "making_charge_inr_g", "making_charge_bp", "tender_margin_pct", "spec_version", "spec_verified"]
    basis = f[cols].reset_index(drop=True)
    curve = curve.reset_index().rename(columns={"index": "date"})
    return basis, curve, report
