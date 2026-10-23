"""Risk-free rates for the implied-carry check: FBIL 3-month T-bill benchmark, with the RBI repo rate before it.

FBIL's public chart endpoint only serves the last 12 months, so every fetch is cached under data/raw/rates/ and the
build merges all cached files: history grows by itself from the first fetch onward.
"""
import json
from datetime import date

import pandas as pd
import yaml
from curl_cffi import requests

from .mcx import RAW

RATES_SPEC = RAW.parent / "specs" / "rates.yaml"
TBILL_SNAPSHOT = RAW.parent / "snapshot" / "tbill_3m.parquet"   # committed copy, so history survives a lost cache
FBIL = "https://www.fbil.org.in"
TBILL_URL = f"{FBIL}/wasdm/tbill/fetchcommongraph/12M"


def fetch_fbil(today: date, log=print):
    s = requests.Session(impersonate="chrome")
    s.get(FBIL, timeout=40)
    r = s.get(TBILL_URL, timeout=60)
    j = r.json() if r.status_code == 200 and r.text.lstrip().startswith("{") else None
    if not j:
        log(f"  ! FBIL T-bill: HTTP {r.status_code}")
        return 0
    f = RAW / "rates" / f"fbil_tbill_3m_{today:%Y%m%d}.json"
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(j), encoding="utf-8")
    n = sum(len(d["benchMarkTrend"]) for d in j["benchMarkTrendData"])
    log(f"  rates: FBIL 3M T-bill, {n} days")
    return n


def load_tbill():
    rows = []
    for f in sorted((RAW / "rates").glob("fbil_tbill_3m_*.json")):
        for d in json.loads(f.read_text(encoding="utf-8"))["benchMarkTrendData"]:
            if d["productName"] != "T-Bill Rate - 3 Months":
                continue
            rows += [{"date": date.fromisoformat(p["publishDate"]), "tbill_3m_pct": float(p["rate"])} for p in d["benchMarkTrend"]]
    df = pd.DataFrame(rows, columns=["date", "tbill_3m_pct"])
    if TBILL_SNAPSHOT.exists():
        df = pd.concat([pd.read_parquet(TBILL_SNAPSHOT), df])
    return df.drop_duplicates("date", keep="last").sort_values("date").reset_index(drop=True)


def repo_series():
    table = yaml.safe_load(RATES_SPEC.read_text(encoding="utf-8"))["repo_rate_pct"]
    return pd.Series({pd.Timestamp(str(k)).date(): float(v) for k, v in table.items()}).sort_index()


def rates_daily(dates):
    """One row per date: T-bill where FBIL covers it (carried forward over FBIL holidays), repo otherwise."""
    d = pd.DataFrame({"date": sorted(set(dates))})
    repo = repo_series()
    d["repo_pct"] = [repo[repo.index <= x].iloc[-1] if (repo.index <= x).any() else float("nan") for x in d.date]
    tb = load_tbill()
    if len(tb):
        d = pd.merge_asof(d.assign(_t=pd.to_datetime(d.date)), tb.assign(_t=pd.to_datetime(tb.date)).drop(columns="date"),
                          on="_t", direction="backward").drop(columns="_t")
        d.loc[pd.to_datetime(d.date) < pd.Timestamp(tb.date.min()), "tbill_3m_pct"] = float("nan")
    else:
        d["tbill_3m_pct"] = float("nan")
    d["rf_pct"] = d.tbill_3m_pct.fillna(d.repo_pct)
    d["rf_source"] = d.tbill_3m_pct.notna().map({True: "FBIL 3M T-bill", False: "RBI repo (proxy)"})
    return d
