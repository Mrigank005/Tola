"""M5: chooser formula, alert log and export."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from tola import alerts, chooser as ch

ROOT = Path(__file__).resolve().parent.parent
SNAP, EXPORT = ROOT / "data" / "snapshot", ROOT / "data" / "export"
pytestmark = pytest.mark.skipif(not (SNAP / "basis_daily.parquet").exists(), reason="no snapshot built")


@pytest.fixture(scope="module")
def inputs():
    read = lambda n: pd.read_parquet(SNAP / f"{n}.parquet")
    live, asof = ch.live_inputs(read("basis_daily"), read("contracts"), read("curve_daily"))
    return live, ch.premium_changes(read("convergence_daily")), asof


def test_lots_must_match_the_grams_asked_for(inputs):
    q = ch.quote(ch.Request(100, 20, False), *inputs)
    gold = q[q.symbol == "GOLD"].iloc[0]
    assert not gold.feasible and "1000 g lots" in gold.reason          # 100 g can't be done in 1 kg lots
    guinea = q[q.symbol == "GOLDGUINEA"].iloc[0]
    assert guinea.lots == 12 and guinea.grams == 96                     # nearest whole 8 g lots


def test_cost_lines_add_up_and_ranking_is_by_cost_per_gram(inputs):
    for req in (ch.Request(100, 20, False), ch.Request(100, 20, True)):
        q = ch.quote(req, *inputs)
        ok = q[q.feasible]
        lines = [c for c in ok.columns if c.endswith("_inr") and c not in ("total_inr", "notional_inr", "premium_risk_inr")]
        assert np.allclose(ok[lines].sum(axis=1), ok.total_inr)
        assert ok.total_inr_g.is_monotonic_increasing and list(ok["rank"]) == list(range(1, len(ok) + 1))


def test_delivery_adds_making_charge_and_gst(inputs):
    q = ch.quote(ch.Request(100, 20, True), *inputs).set_index("symbol")
    assert q.loc["GOLDPETAL", "making_charge_inr"] == pytest.approx(100 * q.loc["GOLDPETAL", "grams"])
    assert q.loc["GOLDM", "making_charge_inr"] == 0
    assert q.loc["GOLDTEN", "gst_inr"] == pytest.approx(0.03 * q.loc["GOLDTEN", "notional_inr"])


def test_exit_before_tender_respects_the_window(inputs):
    q = ch.quote(ch.Request(10, 20, False), *inputs)
    ok = q[q.feasible]
    assert (pd.to_datetime(ok.exit_by) < pd.to_datetime(ok.tender_start)).all()


def test_reference_contracts_carry_no_premium_change(inputs):
    q = ch.quote(ch.Request(100, 20, False), *inputs).set_index("symbol")
    assert q.loc["GOLDTEN", "premium_inr"] == 0 and q.loc["GOLDM", "premium_inr"] == 0


@pytest.mark.skipif(not (EXPORT / "golden.json").exists(), reason="no export")
def test_golden_cases_match_the_current_formula(inputs):
    g = json.loads((EXPORT / "golden.json").read_text(encoding="utf-8"))
    for case in g["cases"]:
        q = ch.quote(ch.Request(**case["request"]), *inputs)
        want = {r["symbol"]: r for r in case["quotes"] if r["feasible"]}
        got = q[q.feasible].set_index("symbol")
        assert set(want) == set(got.index)
        for sym, r in want.items():
            assert got.loc[sym, "total_inr_g"] == pytest.approx(r["total_inr_g"], abs=1e-4)


@pytest.mark.skipif(not (EXPORT / "alerts.json").exists(), reason="no export")
def test_alert_log_is_quiet_and_dated_correctly():
    a = json.loads((EXPORT / "alerts.json").read_text(encoding="utf-8"))
    s = a["summary"]
    assert s["quiet_days"] / s["trading_days"] > 0.6
    assert all(x["date"] <= a["asof"] for x in a["alerts"])


def test_alerts_fire_only_on_onset():
    flag = pd.Series([False, True, True, False, True])
    assert list(alerts._onsets(flag)) == [False, True, False, False, True]
