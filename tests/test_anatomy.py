"""Structural invariants of the M2 basis anatomy (data/snapshot/basis_daily, curve_daily)."""
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

SNAP = Path(__file__).resolve().parent.parent / "data" / "snapshot"
pytestmark = pytest.mark.skipif(not (SNAP / "basis_daily.parquet").exists(), reason="no snapshot built")


@pytest.fixture(scope="module")
def basis():
    return pd.read_parquet(SNAP / "basis_daily.parquet")


@pytest.fixture(scope="module")
def curve():
    return pd.read_parquet(SNAP / "curve_daily.parquet")


def test_waterfall_adds_up(basis):
    b = basis.dropna(subset=["residual_bp"])
    total = b.timing_bp + b.carry_bp + b.reference_bp + b.residual_bp
    assert np.allclose(total, b.basis_total_bp, atol=1e-6)
    assert np.allclose(b.ref_spot_g999 * np.exp((b.timing_bp + b.carry_bp + b.reference_bp) / 1e4), b.fair_g999)


def test_benchmark_contracts_sit_on_their_own_curve(basis):
    b = basis[basis.symbol.isin(["GOLD", "GOLDM"]) & (basis.value_lakh >= 100) & ~basis.in_tender].dropna(subset=["residual_bp"])
    by_year = b.groupby(pd.to_datetime(b.date).dt.year).residual_bp.median()
    assert by_year.abs().max() < 10, by_year


def test_reference_term_is_zero_for_ahmedabad_contracts(basis):
    for s in ("GOLD", "GOLDM", "GOLDTEN", "GOLDGUINEA"):
        assert basis[basis.symbol == s].reference_bp.abs().median() < 0.5, s


def test_every_fitted_day_has_a_risk_free_rate(curve):
    fit = curve[curve.carry_source == "fit"]
    assert fit.rf_pct.notna().all()
    assert (fit[pd.to_datetime(fit.date) >= "2025-10-16"].rf_source == "FBIL 3M T-bill").all()


def test_carry_is_plausible(curve):
    fit = curve[curve.carry_source == "fit"]
    assert fit.carry_pa.median() == pytest.approx(0.04, abs=0.03)
    assert ((fit.carry_pa > -0.2) & (fit.carry_pa < 0.6)).mean() > 0.99
