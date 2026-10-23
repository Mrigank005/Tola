"""One-command data refresh: fetch what is missing or still live from MCX, then rebuild the snapshot.

    python -m tola.refresh              # fetch, then build data/snapshot/
    python -m tola.refresh --offline    # rebuild from the raw cache only (no network)

What gets fetched:
  - discovery: one daily bhavcopy per month since 2020 (cached), plus the latest trading day, to list contracts
  - contracts: every gold futures contract's full daily history; live ones and ones cached before expiry are re-fetched
  - spot: each contract's polled spot, one call per product per calendar year; the current year is re-fetched
  - rates: FBIL's 3-month T-bill benchmark (last 12 months; cached copies accumulate history)
A first run from an empty cache is about 250 calls (~10 minutes at MCX-friendly pacing); a daily refresh is ~40.
"""
import argparse
import json
import shutil
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

from . import build, parse, rates, specs
from .checks import Report
from .mcx import RAW, Client, MCXError

FIRST_MONTH = date(2020, 1, 1)
WINDOW_DAYS = 450                  # GOLD contracts trade ~12 months; 450 days covers every gold contract's life
STATE = RAW / "_fetched.json"      # cache key -> date fetched, to tell complete files from ones fetched while live
G0_RAW = RAW.parent.parent / "PS Research" / "g0_gate" / "raw"


def month_starts(start, end):
    m = start.replace(day=1)
    while m <= end:
        yield m
        m = (m.replace(day=28) + timedelta(days=4)).replace(day=1)


class Refresher:
    def __init__(self, today, log=print):
        self.today, self.log = today, log
        self.client = Client(log=log)
        self.report = Report()
        self.state = json.loads(STATE.read_text()) if STATE.exists() else {}

    def mark(self, key):
        self.state[key] = str(self.today)

    def fetched_on(self, key):
        v = self.state.get(key)
        if v:
            return date.fromisoformat(v)
        f = RAW / key
        return datetime.fromtimestamp(f.stat().st_mtime).date() if f.exists() else None

    def import_g0(self):
        """Seed the cache from the G0 backfill (same endpoints, same file names) so it is never re-downloaded."""
        n = 0
        for sub in ("contract", "datewise"):
            (RAW / sub).mkdir(parents=True, exist_ok=True)
            for f in (G0_RAW / sub).glob("*.json"):
                dst = RAW / sub / f.name
                if not dst.exists():
                    shutil.copy2(f, dst)
                    n += 1
        if n:
            self.log(f"seeded {n} cached responses from the G0 backfill")

    # --- discovery ------------------------------------------------------------------------------

    def trading_day_rows(self, d, refresh):
        try:
            j = self.client.datewise(d, refresh=refresh)
        except MCXError as e:
            self.log(f"  ! {d}: {e}")
            return []
        return [w for w in parse.datewise_rows(j, d, self.report) if w["Symbol"].strip() in specs.symbols()]

    def discover(self):
        found = {}

        def take(rows):
            for w in rows:
                found.setdefault((w["Symbol"].strip(), datetime.strptime(w["ExpiryDate"], "%d%b%Y").date()), True)

        for m in month_starts(FIRST_MONTH, self.today):
            for off in range(10):  # the 10th, rolling forward past weekends and holidays
                d = m.replace(day=10) + timedelta(days=off)
                if d.weekday() < 5 and d <= self.today:
                    rows = self.trading_day_rows(d, refresh=(self.today - d).days < 7)
                    if rows:
                        take(rows)
                        break
        # the latest trading day, so contracts listed since the 10th are included
        for back in range(10):
            d = self.today - timedelta(days=back)
            if d.weekday() < 5:
                rows = self.trading_day_rows(d, refresh=True)
                if rows:
                    take(rows)
                    self.latest = d
                    break
        self.log(f"discovered {len(found)} gold contracts (latest trading day {getattr(self, 'latest', '?')})")
        return sorted(found)

    # --- fetch ----------------------------------------------------------------------------------

    def contract_needs_fetch(self, sym, exp):
        key = f"contract/{sym}_{exp:%Y%m%d}.json"
        f = RAW / key
        if not f.exists() or exp >= self.today:
            return True
        got = self.fetched_on(key)
        if got is not None and got <= exp:          # cached while the contract was still trading
            return True
        rows = json.loads(f.read_text()).get("Data") or []
        if rows:                                   # a G0 file fetched with a 364-day window may be cut at the start
            first = min(datetime.strptime(w["Date"], "%m/%d/%Y").date() for w in rows)
            if (first - (exp - timedelta(days=364))).days <= 3:
                return True
        return False

    def fetch_contracts(self, todo):
        need = [(s, e) for s, e in todo if self.contract_needs_fetch(s, e)]
        self.log(f"contracts: {len(todo)} known, {len(need)} to fetch")
        for i, (s, e) in enumerate(need, 1):
            try:
                j = self.client.contract(s, e, e - timedelta(days=WINDOW_DAYS), min(e, self.today), refresh=True)
                self.mark(f"contract/{s}_{e:%Y%m%d}.json")
                self.log(f"  [{i}/{len(need)}] {s} {e:%d %b %Y}: {len(j.get('Data') or [])} rows")
            except MCXError as ex:
                self.log(f"  [{i}/{len(need)}] {s} {e}: FAILED {ex}")

    def fetch_spot(self):
        calls = 0
        for s in specs.symbols():
            sp = specs.spot(s)
            for y in range(FIRST_MONTH.year, self.today.year + 1):
                key = f"spot/{sp['product']}_{sp['location']}_{y}.json"
                got = self.fetched_on(key)
                if (RAW / key).exists() and got is not None and got > date(y, 12, 31):
                    continue
                try:
                    j = self.client.spot(sp["product"], sp["location"], date(y, 1, 1), min(date(y, 12, 31), self.today),
                                         name=str(y), refresh=True)
                    self.mark(key)
                    calls += 1
                    self.log(f"  spot {sp['product']} {sp['location']} {y}: {len(j.get('Data') or [])} polls")
                except MCXError as ex:
                    self.log(f"  spot {sp['product']} {y}: FAILED {ex}")
        self.log(f"spot: {calls} windows fetched")

    def save_state(self):
        STATE.write_text(json.dumps(self.state, indent=0, sort_keys=True))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Refresh MCX gold data and rebuild the snapshot.")
    ap.add_argument("--offline", action="store_true", help="build from the raw cache only, no network")
    ap.add_argument("--today", type=date.fromisoformat, default=date.today(), help=argparse.SUPPRESS)
    args = ap.parse_args(argv)

    def log(msg):
        print(msg, flush=True)

    if not args.offline:
        r = Refresher(args.today, log)
        r.import_g0()
        try:
            r.fetch_contracts(r.discover())
            r.fetch_spot()
            rates.fetch_fbil(args.today, log)
        finally:
            r.save_state()
            log(f"network calls: {r.client.calls}")
    try:
        build.build(asof=args.today, log=log)
    except build.BuildError as e:
        log(f"BUILD FAILED: {e}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
