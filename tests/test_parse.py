import json

import pytest

from tola import parse
from tola.checks import Report

ROW = {"InstrumentName": "FUTCOM", "Symbol": "GOLDTEN      ", "ExpiryDate": "30OCT2026", "Date": "10/09/2026",
       "DateDisplay": "09 Oct 2026", "Open": 1, "High": 2, "Low": 1, "Close": 2, "PreviousClose": 1, "Volume": 3,
       "Value": 0.5, "OpenInterest": 4}


def write(tmp_path, name, rows):
    f = tmp_path / name
    f.write_text(json.dumps({"Data": rows}))
    return f


def test_futures_dates_are_month_first(tmp_path):
    rows = parse.futures_file(write(tmp_path, "GOLDTEN_20261030.json", [ROW]), Report())
    assert str(rows[0]["date"]) == "2026-10-09"
    assert rows[0]["symbol"] == "GOLDTEN"


@pytest.mark.parametrize("change,check", [
    ({"DateDisplay": "10 Sep 2026"}, "futures.date_fields_disagree"),
    ({"Symbol": "GOLDGUINEA"}, "futures.wrong_contract"),
    ({"ExpiryDate": "27NOV2026"}, "futures.wrong_contract"),
    ({"InstrumentName": "OPTFUT"}, "futures.instrument_not_futcom"),
])
def test_futures_guards_reject_bad_rows(tmp_path, change, check):
    r = Report()
    rows = parse.futures_file(write(tmp_path, "GOLDTEN_20261030.json", [{**ROW, **change}]), r)
    assert rows == [] and r.errors()[check]["count"] == 1


SPOT = {"symbol": "GOLDGUINEA", "unit": "8 GRMS", "location": "AHMEDABAD", "todaysSpotPrice": 57481.0,
        "date": "/Date(1719579872990)/", "FormattedDate": "28 Jun 2024", "FormattedTime": "18:34"}
SPEC = {"product": "GOLDGUINEA", "location": "AHMEDABAD", "unit_g": 8, "purity": 999}


def test_spot_epoch_is_read_as_ist(tmp_path):
    rows = parse.spot_file(write(tmp_path, "GOLDGUINEA_AHMEDABAD_2024.json", [SPOT]), SPEC, Report())
    assert rows[0]["ts"].strftime("%Y-%m-%d %H:%M") == "2024-06-28 18:34"


@pytest.mark.parametrize("change,check", [
    ({"unit": "10 GRMS"}, "spot.unit_mismatch"),
    ({"location": "MUMBAI"}, "spot.wrong_series"),
    ({"FormattedTime": "12:34"}, "spot.timestamp_disagree"),
])
def test_spot_guards(tmp_path, change, check):
    r = Report()
    assert parse.spot_file(write(tmp_path, "x.json", [{**SPOT, **change}]), SPEC, r) == []
    assert check in r.errors()


def test_datewise_ignores_a_substituted_day():
    from datetime import date
    r = Report()
    assert parse.datewise_rows({"Data": [ROW]}, date(2026, 10, 10), r) == []
    assert "datewise.other_day_returned" in r.summary()["warnings"]
