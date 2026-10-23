"""Tables behind M2_RESULTS.md, computed from the committed snapshot. Writes m2_tables.md next to this file.

Usage: python "PS Research/m2_basis/summarise_m2.py"
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).parent
SNAP = HERE.parent.parent / "data" / "snapshot"
b = pd.read_parquet(SNAP / "basis_daily.parquet")
c = pd.read_parquet(SNAP / "curve_daily.parquet")
fit = c[c.carry_source == "fit"].assign(year=lambda d: pd.to_datetime(d.date).dt.year,
                                        month=lambda d: pd.to_datetime(d.date).dt.to_period("M").astype(str))
liq = b[(b.value_lakh >= 100) & ~b.in_tender].dropna(subset=["residual_bp"]).assign(year=lambda d: pd.to_datetime(d.date).dt.year)
ORDER = ["GOLD", "GOLDM", "GOLDTEN", "GOLDGUINEA", "GOLDPETAL"]

out = ["# M2 tables", "", f"Generated from data/snapshot (futures through {b.date.max()}). Liquid = Rs 1 Cr+ turnover, outside the tender window.", ""]

out += ["## 1. Implied carry vs risk-free, by year (median, % a year)", ""]
y = fit.groupby("year").agg(carry=("carry_pa", lambda v: 100 * v.median()), rf=("rf_pct", "median"),
                            carry_minus_rf=("carry_minus_rf_pct", "median"), days=("date", "size"),
                            rf_source=("rf_source", lambda s: s.mode().iloc[0]))
out += [y.round(2).to_markdown(), ""]

out += ["## 2. Implied carry vs risk-free, by month since Jul 2025", ""]
m = fit[fit.month >= "2025-07"].groupby("month").agg(carry=("carry_pa", lambda v: 100 * v.median()), rf=("rf_pct", "median"),
                                                     fit_rmse_bp=("fit_rmse_bp", "median"), rf_source=("rf_source", "first"))
out += [m.round(2).to_markdown(), ""]

out += ["## 3. Timing term (spot poll ~5-6 pm vs futures close to ~11:30 pm), bp", ""]
t = fit.groupby("year").timing_bp.describe(percentiles=[.1, .25, .5, .75, .9])[["10%", "25%", "50%", "75%", "90%"]]
out += [t.round(1).to_markdown(), ""]

out += ["## 4. Residual by contract and year (median bp, liquid, pre-tender)", ""]
r = liq.pivot_table(index="year", columns="symbol", values="residual_bp", aggfunc="median")[ORDER]
out += [r.round(1).to_markdown(), ""]

out += ["## 5. Residual vs making charge, 2025-26 (median bp)", ""]
recent = liq[liq.year >= 2025]
mc = recent.groupby("symbol").agg(residual=("residual_bp", "median"), making_charge=("making_charge_bp", "median"),
                                  making_charge_inr_g=("making_charge_inr_g", "median"), days=("date", "size")).reindex(ORDER)
out += [mc.round(1).to_markdown(), ""]

out += ["## 6. Reference term: GOLDPETAL Mumbai spot vs Ahmedabad 999 (median bp)", ""]
ref = liq[liq.symbol == "GOLDPETAL"].groupby("year").reference_bp.median()
out += [ref.round(1).to_frame("GOLDPETAL reference_bp").to_markdown(), ""]

(HERE / "m2_tables.md").write_text("\n".join(out), encoding="utf-8")
print("\n".join(out))
