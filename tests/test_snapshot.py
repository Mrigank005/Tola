"""Invariants of the committed snapshot. These read data/snapshot/, so they test the data we ship."""
import json
from pathlib import Path

import pandas as pd
import pytest

SNAP = Path(__file__).resolve().parent.parent / "data" / "snapshot"
pytestmark = pytest.mark.skipif(not (SNAP / "manifest.json").exists(), reason="no snapshot built")


@pytest.fixture(scope="module")
def fut():
    return pd.read_parquet(SNAP / "futures_daily.parquet")


def test_manifest_matches_files():
    import hashlib
    m = json.loads((SNAP / "manifest.json").read_text())
    assert not m["validation"]["errors"]
    for name, t in m["tables"].items():
        assert hashlib.sha256((SNAP / f"{name}.parquet").read_bytes()).hexdigest() == t["sha256"], name


def test_one_row_per_contract_day_and_none_after_expiry(fut):
    assert not fut.duplicated(["symbol", "expiry", "date"]).any()
    assert (fut.date <= fut.expiry).all()


def test_untraded_days_carry_no_fill_prices(fut):
    u = fut[~fut.traded]
    assert u[["open", "high", "low", "vwap"]].isna().all().all()


def test_days_to_expiry_count_down(fut):
    for _, g in fut.groupby(["symbol", "expiry"]):
        assert g.sort_values("date").tdte.is_monotonic_decreasing
    assert (fut[fut.date == fut.expiry].tdte == 0).all()


def test_995_contracts_are_lifted_to_999(fut):
    g = fut[(fut.symbol == "GOLDM") & fut.traded].iloc[0]
    assert g.close_g999 == pytest.approx(g.close / 10 * 999 / 995)


def test_same_reference_contracts_settle_together():
    st = pd.read_parquet(SNAP / "settlement.parquet")
    w = st.pivot(index="expiry", columns="symbol", values="ddr_g999").dropna(subset=["GOLDTEN", "GOLDGUINEA"])
    assert len(w) >= 18
    assert (1e4 * (w.GOLDGUINEA / w.GOLDTEN - 1)).abs().max() < 0.5   # bp; G0 found <= 0.11


def test_reproduces_the_g0_premiums(fut):
    """The snapshot must reproduce G0 (PS Research/g0_gate/G0_RESULTS.md) under G0's pre-registered rules."""
    from datetime import date
    f = fut[(fut.expiry >= date(2025, 4, 1)) & (fut.expiry <= date(2026, 9, 30))]
    for small, expected in (("GOLDGUINEA", 78.7), ("GOLDPETAL", 94.1)):
        m = f[f.symbol == small].merge(f[f.symbol == "GOLDTEN"], on=["expiry", "date"], suffixes=("_s", "_b"))
        m = m[m.traded_s & m.traded_b & (m.value_lakh_s >= 100) & (m.value_lakh_b >= 100) & (m.tdte_s >= 5) & (m.tdte_b >= 5)]
        c = (1e4 * (m.vwap_g999_s / m.vwap_g999_b - 1)).groupby(m.expiry).agg(["mean", "size"])
        c = c[c["size"] >= 10]
        assert len(c) == 18 and c["mean"].mean() == pytest.approx(expected, abs=0.05), small


def test_rebuilt_ddr_matches_published_settlement_where_mcx_published_it():
    st = pd.read_parquet(SNAP / "settlement.parquet")
    t = st[st.close_is_ddr_era & st.ddr_reliable]
    assert len(t) >= 140 and t.ddr_matches_close.all()
