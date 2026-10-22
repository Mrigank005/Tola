"""Turn cached MCX JSON into typed rows. Row-level guards report into a checks.Report.

Field quirks (verified on real responses, see PS Research/06_data_sources.md):
  - futures `Date` is MM/DD/YYYY while requests use DD/MM/YYYY; `DateDisplay` is "22 Oct 2026". Both must agree.
  - `Symbol` is space-padded; `ExpiryDate` is DDMMMYYYY.
  - `Value` is turnover in Rs lakh, `Volume` is lots.
  - spot `date` is "/Date(<ms since epoch, UTC>)/"; FormattedDate / FormattedTime are IST.
"""
import json
import re
from datetime import date, datetime, timedelta, timezone

IST = timezone(timedelta(hours=5, minutes=30))
NUM = ("Open", "High", "Low", "Close", "PreviousClose", "Value")


def _d(s, fmt):
    return datetime.strptime(s.strip(), fmt).date()


def futures_file(path, report):
    """Rows of one GetCommoditywiseBhavCopy response, cached as <SYMBOL>_<YYYYMMDD>.json."""
    sym, exp = path.stem.split("_")
    expiry = _d(exp, "%Y%m%d")
    rows = []
    for w in json.loads(path.read_text(encoding="utf-8")).get("Data") or []:
        where = f"{path.name} {w.get('DateDisplay')}"
        if w.get("InstrumentName") != "FUTCOM":
            report.add("futures.instrument_not_futcom", "error", where, "Response mixed options into a futures request")
            continue
        if w["Symbol"].strip() != sym or _d(w["ExpiryDate"], "%d%b%Y") != expiry:
            report.add("futures.wrong_contract", "error", f"{where}: {w['Symbol'].strip()} {w['ExpiryDate']}",
                       "Row belongs to a different contract than the one requested")
            continue
        d = _d(w["Date"], "%m/%d/%Y")
        if d != _d(w["DateDisplay"], "%d %b %Y"):
            report.add("futures.date_fields_disagree", "error", f"{where}: Date={w['Date']}",
                       "MM/DD `Date` and `DateDisplay` give different days")
            continue
        rows.append({
            "date": d, "symbol": sym, "expiry": expiry,
            "open": float(w["Open"]), "high": float(w["High"]), "low": float(w["Low"]), "close": float(w["Close"]),
            "prev_close": float(w["PreviousClose"]), "volume_lots": int(w["Volume"]), "value_lakh": float(w["Value"]),
            "oi_lots": int(w["OpenInterest"]), "source": f"contract/{path.name}",
        })
    return rows


_MS = re.compile(r"/Date\((-?\d+)\)/")


def spot_file(path, spec_spot, report):
    """Rows of one GetSpotMarketArchive response. spec_spot is the symbol's `spot` block from the spec file."""
    rows = []
    for w in json.loads(path.read_text(encoding="utf-8")).get("Data") or []:
        where = f"{path.name} {w.get('FormattedDate')} {w.get('FormattedTime')}"
        if w["symbol"].strip() != spec_spot["product"] or w["location"].strip() != spec_spot["location"]:
            report.add("spot.wrong_series", "error", f"{where}: {w['symbol']} {w['location']}",
                       "Poll belongs to a different product or location than requested")
            continue
        unit = int(re.match(r"\s*(\d+)", w["unit"]).group(1))
        if unit != spec_spot["unit_g"]:
            report.add("spot.unit_mismatch", "error", f"{where}: unit {w['unit']!r}", "Quoted unit differs from the spec file")
            continue
        ts = datetime.fromtimestamp(int(_MS.match(w["date"]).group(1)) / 1000, IST)
        shown = datetime.strptime(f"{w['FormattedDate']} {w['FormattedTime']}", "%d %b %Y %H:%M").replace(tzinfo=IST)
        if abs((ts - shown).total_seconds()) >= 60:
            report.add("spot.timestamp_disagree", "error", f"{where}: epoch says {ts:%d %b %Y %H:%M}",
                       "Epoch timestamp and formatted IST time differ")
            continue
        rows.append({"ts": ts.replace(tzinfo=None), "date": ts.date(), "product": spec_spot["product"],
                     "location": spec_spot["location"], "unit_g": unit, "price": float(w["todaysSpotPrice"]),
                     "source": f"spot/{path.name}"})
    return rows


def datewise_rows(j, requested: date, report):
    """Gold FUTCOM rows of one GetDateWiseBhavCopy response, or [] if MCX answered with another day (holiday)."""
    rows = (j or {}).get("Data") or []
    if not rows:
        return []
    got = {_d(w["Date"], "%m/%d/%Y") for w in rows}
    if got != {requested}:
        report.add("datewise.other_day_returned", "warn", f"asked {requested}, got {sorted(got)}",
                   "MCX returned a different trading day (holiday behaviour); rows ignored")
        return []
    return [w for w in rows if w["Symbol"].strip().startswith("GOLD") and w.get("InstrumentName") == "FUTCOM"]
