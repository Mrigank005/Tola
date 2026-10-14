"""G0 backfill: discover gold expiries month by month, then pull each contract's full daily history.

Every raw response is cached under raw/, so re-runs only fetch what is missing.
Usage: python fetch_g0.py [--test]
"""
import json
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path

from curl_cffi import requests

BASE = "https://www.mcxindia.com/market-data/bhavcopy"
HEADERS = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": BASE,
}
SYMBOLS = ("GOLDTEN", "GOLDGUINEA", "GOLDPETAL")
FIRST_MONTH = date(2020, 1, 1)
LAST_EXPIRY = date(2026, 9, 30)  # completed cycles only
PAUSE = 1.5

RAW = Path(__file__).parent / "raw"
(RAW / "datewise").mkdir(parents=True, exist_ok=True)
(RAW / "contract").mkdir(parents=True, exist_ok=True)

session = requests.Session(impersonate="chrome")
session.get(BASE, timeout=40)
calls = 0


def get_json(url, params):
    global calls
    for attempt in range(3):
        try:
            calls += 1
            r = session.get(url, params=params, headers=HEADERS, timeout=40)
            time.sleep(PAUSE)
            if r.status_code == 200 and r.text.lstrip().startswith("{"):
                return r.json()
            print(f"  ! HTTP {r.status_code} on {params}", flush=True)
        except Exception as e:  # network hiccup: back off and retry
            print(f"  ! {e!r} on {params}", flush=True)
        time.sleep(5 * (attempt + 1))
    return None


def datewise(d):
    f = RAW / "datewise" / f"{d:%Y%m%d}.json"
    if f.exists():
        return json.loads(f.read_text())
    j = get_json(f"{BASE}/GetDateWiseBhavCopy", {"InstrumentName": "FUTCOM", "fromDate": f"{d:%d/%m/%Y}"})
    if j is not None:
        f.write_text(json.dumps(j))
    return j


def contract(sym, expiry):
    f = RAW / "contract" / f"{sym}_{expiry:%Y%m%d}.json"
    if f.exists():
        return json.loads(f.read_text())
    frm = expiry - timedelta(days=364)
    j = get_json(f"{BASE}/GetCommoditywiseBhavCopy", {
        "InstrumentName": "FUTCOM", "Symbol": sym, "Expiry": f"{expiry:%d%b%Y}".upper(),
        "fromDate": f"{frm:%d/%m/%Y}", "toDate": f"{expiry:%d/%m/%Y}",
    })
    if j is not None:
        f.write_text(json.dumps(j))
    return j


def discover(months):
    """One trading day per month (the 10th, rolling forward past holidays) -> listed expiries."""
    expiries = {s: set() for s in SYMBOLS}
    for m in months:
        for offset in range(7):
            d = m.replace(day=10) + timedelta(days=offset)
            if d.weekday() >= 5:
                continue
            j = datewise(d)
            rows = (j or {}).get("Data") or []
            if rows:
                for w in rows:
                    s = w["Symbol"].strip()
                    if s in expiries:
                        expiries[s].add(datetime.strptime(w["ExpiryDate"], "%d%b%Y").date())
                break
        print(f"{m:%Y-%m} discovered, calls so far {calls}", flush=True)
    return expiries


def month_starts(start, end):
    m = start
    while m <= end:
        yield m
        m = (m.replace(day=28) + timedelta(days=4)).replace(day=1)


if __name__ == "__main__":
    test = "--test" in sys.argv
    months = list(month_starts(FIRST_MONTH, date(2026, 10, 1)))
    if test:
        months = [date(2020, 1, 1), date(2025, 6, 1)]
    exp = discover(months)
    todo = sorted((s, e) for s, es in exp.items() for e in es if e <= LAST_EXPIRY)
    if test:
        todo = [t for t in todo if t[1].year in (2020, 2025)][:3]
    print(f"{len(todo)} contracts to fetch", flush=True)
    for i, (s, e) in enumerate(todo, 1):
        j = contract(s, e)
        n = len((j or {}).get("Data") or [])
        print(f"[{i}/{len(todo)}] {s} {e} rows={n}", flush=True)
    (RAW / "expiries.json").write_text(json.dumps({s: sorted(map(str, es)) for s, es in exp.items()}, indent=1))
    print(f"done, {calls} network calls", flush=True)
