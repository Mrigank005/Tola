"""G0 follow-up: do GOLDTEN, GOLDGUINEA and GOLDPETAL settle to the same price per gram in every cycle?

For each shared expiry, pull MCX polled spot (the DDR basis) for each contract's own symbol and location
over the last few days of the cycle, take the last poll on expiry day, and compare per gram.
GOLDM's Ahmedabad spot (995 basis) is the purity reference: a 999-basis series should sit at x 999/995 over it.
Also samples 2024 GOLDPETAL / GOLDGUINEA expiries to check the GOLDPETAL break against the old spec.
Raw responses are cached under raw/spot/.
"""
import json
import time
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
from curl_cffi import requests

HERE = Path(__file__).parent
RAW = HERE / "raw" / "spot"
RAW.mkdir(parents=True, exist_ok=True)
OUT = HERE / "results"
SPOT = {  # symbol -> (location, grams the spot is quoted for)
    "GOLDTEN": ("AHMEDABAD", 10), "GOLDGUINEA": ("AHMEDABAD", 8),
    "GOLDPETAL": ("MUMBAI", 1), "GOLDM": ("AHMEDABAD", 10),
}
URL = "https://www.mcxindia.com/GetSpotMarketArchive"
HEADERS = {"Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest",
           "Referer": "https://www.mcxindia.com/market-data/spot-market-price"}

_session = None


def session():
    """Open the MCX session only when something actually has to be fetched, so cached runs stay offline."""
    global _session
    if _session is None:
        _session = requests.Session(impersonate="chrome")
        _session.get("https://www.mcxindia.com/market-data/spot-market-price", timeout=40)
    return _session


def spot_window(sym, end, days=6):
    f = RAW / f"{sym}_{end:%Y%m%d}.json"
    if f.exists():
        return json.loads(f.read_text())
    loc = SPOT[sym][0]
    params = {"Product": sym, "Location": loc, "fromDate": f"{end - timedelta(days=days):%d/%m/%Y}",
              "toDate": f"{end:%d/%m/%Y}", "Session": "0", "culture": "en"}
    for attempt in range(3):
        try:
            r = session().get(URL, params=params, headers=HEADERS, timeout=40)
            time.sleep(1.5)
            if r.text.lstrip().startswith("{"):
                j = r.json()
                f.write_text(json.dumps(j))
                return j
        except Exception as e:
            print("  !", sym, end, repr(e), flush=True)
        time.sleep(5 * (attempt + 1))
    return None


def last_poll(j, day):
    """Last poll on `day`; if none (expiry moved or no poll), the last poll on the latest earlier day."""
    rows = (j or {}).get("Data") or []
    best = None
    for w in rows:
        d = datetime.strptime(w["FormattedDate"], "%d %b %Y").date()
        if d > day:
            continue
        key = (d, w["FormattedTime"])
        if best is None or key > best[0]:
            best = (key, w["todaysSpotPrice"])
    return (f"{best[0][0]} {best[0][1]}", best[1]) if best else None


def main():
    g0 = json.loads((OUT / "g0_results.json").read_text())
    shared = [date.fromisoformat(e) for e in g0["shared_cycles"]]
    ctx = [date(2024, m, d) for m, d in [(6, 28), (9, 30), (10, 31), (11, 29), (12, 31)]] + \
          [date(2025, 1, 31), date(2025, 2, 28), date(2025, 3, 31)]
    rows = []
    for e in shared + ctx:
        syms = list(SPOT) if e in shared else ["GOLDGUINEA", "GOLDPETAL", "GOLDM"]
        rec = {"expiry": e, "in_g0": e in shared}
        for s in syms:
            lp = last_poll(spot_window(s, e), e)
            if lp:
                rec[f"{s}_time"], rec[f"{s}_per_g"] = lp[0], lp[1] / SPOT[s][1]
        rows.append(rec)
        print(e, {k: round(v, 2) if isinstance(v, float) else v for k, v in rec.items() if k.endswith("per_g")}, flush=True)
    df = pd.DataFrame(rows)
    ref999 = df["GOLDM_per_g"] * 999 / 995
    for s in ("GOLDTEN", "GOLDGUINEA", "GOLDPETAL"):
        if f"{s}_per_g" in df:
            df[f"{s}_vs_GOLDM999_bp"] = 1e4 * (df[f"{s}_per_g"] / ref999 - 1)
    df["GUINEA_vs_TEN_bp"] = 1e4 * (df["GOLDGUINEA_per_g"] / df.get("GOLDTEN_per_g") - 1)
    df["PETAL_vs_TEN_bp"] = 1e4 * (df["GOLDPETAL_per_g"] / df.get("GOLDTEN_per_g") - 1)
    df["PETAL_vs_GUINEA_bp"] = 1e4 * (df["GOLDPETAL_per_g"] / df["GOLDGUINEA_per_g"] - 1)
    df.round(2).to_csv(OUT / "settlement_check.csv", index=False)
    print(df.round(1).drop(columns=[c for c in df if c.endswith("_time")]).to_string(index=False))


if __name__ == "__main__":
    main()
