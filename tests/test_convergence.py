"""Invariants of the M3 convergence monitor (data/snapshot/convergence_*)."""
from pathlib import Path

import pandas as pd
import pytest

SNAP = Path(__file__).resolve().parent.parent / "data" / "snapshot"
pytestmark = pytest.mark.skipif(not (SNAP / "convergence_daily.parquet").exists(), reason="no snapshot built")


def read(name):
    return pd.read_parquet(SNAP / f"{name}.parquet")


def test_daily_rows_are_unique_and_eligibility_is_consistent():
    d = read("convergence_daily")
    assert not d.duplicated(["pair", "expiry", "date"]).any()
    e = d[d.eligible]
    assert e.both_traded.all() and not e.in_tender.any()
    assert ((e.value_lakh_s >= 100) & (e.value_lakh_b >= 100)).all()


def test_same_reference_pair_reproduces_g0():
    s = read("convergence_summary").set_index("pair")
    g = s.loc["GOLDGUINEA/GOLDTEN"]
    assert g.cycles == 18 and g.pooled_vwap_bp == pytest.approx(78.7, abs=0.1) and g.hit_rate == 1.0
    assert s.loc["GOLDPETAL/GOLDTEN"].pooled_vwap_bp == pytest.approx(94.1, abs=0.3)


def test_guinea_and_ten_settle_to_the_same_price_per_gram():
    c = read("convergence_cycles")
    g = c[(c.pair == "GOLDGUINEA/GOLDTEN") & c.settlement_gap_bp.notna()]
    assert len(g) >= 18 and (g.settlement_gap_bp.abs() < 0.5).all()


def test_live_rows_cover_only_live_cycles():
    c = read("convergence_cycles")
    lv = read("convergence_live")
    live = set(map(tuple, c[c.status == "live"][["pair", "expiry"]].values))
    assert set(map(tuple, lv[["pair", "expiry"]].values)) <= live
    assert lv.history_pct_rank.dropna().between(0, 1).all()


def test_profile_buckets_are_complete_for_the_main_pairs():
    p = read("convergence_profile")
    for pair in ("GOLDGUINEA/GOLDTEN", "GOLDPETAL/GOLDTEN"):
        assert set(p[p.pair == pair].bucket) == {"60+", "40-59", "20-39", "10-19", "5-9", "0-4"}
