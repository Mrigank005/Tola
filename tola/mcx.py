"""MCX client: Chrome-TLS session, polite pacing, retries and a raw-response cache.

MCX sits behind Akamai, which rejects plain HTTP clients; curl_cffi's Chrome fingerprint gets through.
Every response is written to data/raw/ before parsing, so a re-run only fetches what is missing
and every number in the snapshot can be traced back to the bytes MCX returned.
"""
import json
import time
from pathlib import Path

from curl_cffi import requests

ORIGIN = "https://www.mcxindia.com"
BHAV_PAGE = f"{ORIGIN}/market-data/bhavcopy"
SPOT_PAGE = f"{ORIGIN}/market-data/spot-market-price"
HEADERS = {"Accept": "application/json, text/javascript, */*; q=0.01", "X-Requested-With": "XMLHttpRequest"}
PAUSE = 1.5  # seconds between calls; MCX is a public site, not an API
RAW = Path(__file__).resolve().parent.parent / "data" / "raw"


class MCXError(RuntimeError):
    pass


class Client:
    def __init__(self, pause=PAUSE, log=print):
        self.pause, self.log, self.calls = pause, log, 0
        self._session = None

    def session(self):
        """Opened lazily, so a run served entirely from the cache never touches the network."""
        if self._session is None:
            self._session = requests.Session(impersonate="chrome")
            self._session.get(BHAV_PAGE, timeout=40)
        return self._session

    def get_json(self, url, params, referer):
        last = None
        for attempt in range(3):
            try:
                self.calls += 1
                r = self.session().get(url, params=params, headers={**HEADERS, "Referer": referer}, timeout=40)
                time.sleep(self.pause)
                if r.status_code == 200 and r.text.lstrip().startswith("{"):
                    j = r.json()
                    if j.get("IsSuccess") is False:
                        raise MCXError(f"IsSuccess=false: {j.get('Message')}")
                    return j
                last = f"HTTP {r.status_code}, body starts {r.text[:60]!r}"
            except MCXError:
                raise
            except Exception as e:  # network hiccup: back off and retry
                last = repr(e)
            self.log(f"  ! retry {attempt + 1}/3 {url.rsplit('/', 1)[-1]} {params}: {last}")
            time.sleep(5 * (attempt + 1))
        raise MCXError(f"gave up on {url} {params}: {last}")

    def cached(self, path, url, params, referer, refresh=False):
        """Return the cached JSON at data/raw/<path>, fetching it first if missing (or if refresh)."""
        f = RAW / path
        if f.exists() and not refresh:
            return json.loads(f.read_text(encoding="utf-8"))
        j = self.get_json(url, params, referer)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(j), encoding="utf-8")
        return j

    # --- endpoints -------------------------------------------------------------------------------

    def datewise(self, d, refresh=False):
        """All FUTCOM rows for one trading day. Holidays come back empty (or, per the PS, as another day)."""
        return self.cached(f"datewise/{d:%Y%m%d}.json", f"{BHAV_PAGE}/GetDateWiseBhavCopy",
                           {"InstrumentName": "FUTCOM", "fromDate": f"{d:%d/%m/%Y}"}, BHAV_PAGE, refresh)

    def contract(self, symbol, expiry, start, end, refresh=False):
        """Every daily row of one futures contract between start and end."""
        return self.cached(f"contract/{symbol}_{expiry:%Y%m%d}.json", f"{BHAV_PAGE}/GetCommoditywiseBhavCopy",
                           {"InstrumentName": "FUTCOM", "Symbol": symbol, "Expiry": f"{expiry:%d%b%Y}".upper(),
                            "fromDate": f"{start:%d/%m/%Y}", "toDate": f"{end:%d/%m/%Y}"}, BHAV_PAGE, refresh)

    def spot(self, product, location, start, end, name, refresh=False):
        """Every polled spot price for one product and location between start and end (all sessions)."""
        return self.cached(f"spot/{product}_{location}_{name}.json", f"{ORIGIN}/GetSpotMarketArchive",
                           {"Product": product, "Location": location, "fromDate": f"{start:%d/%m/%Y}",
                            "toDate": f"{end:%d/%m/%Y}", "Session": "0", "culture": "en"}, SPOT_PAGE, refresh)
