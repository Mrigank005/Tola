"""Build the committed snapshot (data/snapshot/) from the raw cache, validating as it goes.

Tables (all Parquet):
  futures_daily  one row per contract per trading day: raw fields, VWAP, prices per gram at 999 basis,
                 trading days to expiry, tender-window flag, spec version
  spot_polls     every polled spot price, per gram at 999 basis
  settlement     final settlement price (DDR) per expired contract, rebuilt from polled spot by the spec rule
  contracts      one row per contract: life, row counts, spec version, tender start, status

Errors stop the build before anything is written; warnings go to VALIDATION.md and manifest.json.
"""
import hashlib
import json
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

from . import parse, specs
from .checks import Report
from .mcx import RAW

ROOT = RAW.parent.parent
SNAP = ROOT / "data" / "snapshot"
VALUE_ROUNDING_INR = 500        # Value is published to 0.01 lakh, i.e. +/- Rs 500 of turnover
OUTLIER_PCT = 10.0              # vs contracts expiring within PEER_DAYS: catches unit errors, not steep curves
PEER_DAYS = 35
EARLY_EXPIRY_MAX = 3            # expired contracts ending this many trading days early: MCX moved the expiry
SPOT_TWIN_BP = 1.0              # GOLDTEN / GOLDGUINEA spot vs GOLDM x 999/995, same poll time
FROZEN_DAYS = 4                 # spot unchanged for this many polling days = market closed, MCX repeating the last value
CLOSE_IS_DDR_UNTIL = date(2023, 10, 1)   # before Oct 2023 expiries MCX published the DDR as the last-day Close


class BuildError(RuntimeError):
    pass


# --- futures -------------------------------------------------------------------------------------

def load_futures(report):
    rows = []
    for f in sorted((RAW / "contract").glob("*_*.json")):
        if f.stem.split("_")[0] in specs.symbols():
            rows += parse.futures_file(f, report)
    df = pd.DataFrame(rows)
    key = ["symbol", "expiry", "date"]
    dup = df[df.duplicated(key, keep=False)]
    if len(dup):
        conflicting = dup.drop(columns="source").drop_duplicates().duplicated(key, keep=False)
        if conflicting.any():
            report.add("futures.conflicting_duplicates", "error", dup[key].head(1).to_dict("records"),
                       "Same contract-day appears twice with different values")
        report.add("futures.duplicate_rows", "info", n=int(df.duplicated(key).sum()), note="Identical repeats dropped")
    df = df.drop_duplicates(key).sort_values(key).reset_index(drop=True)
    after = df[df.date > df.expiry]
    for r in after.head(5).itertuples():
        report.add("futures.row_after_expiry", "error", f"{r.symbol} {r.expiry} on {r.date}", "Trading row dated after expiry")
    return df[df.date <= df.expiry]


def add_last_trading_day(df, asof):
    """MCX sometimes brings an expiry forward (no spot poll on the published day, e.g. 31 Mar 2026 -> 30 Mar).
    For an expired contract the last row is its real last trading day; for a live one it is the published expiry."""
    last = df.groupby(["symbol", "expiry"]).date.transform("max")
    df["last_trading_day"] = np.where(df.expiry < asof, last, df.expiry)
    df["last_trading_day"] = pd.to_datetime(df.last_trading_day).dt.date
    return df


def enrich_futures(df, asof, report):
    b = pd.DataFrame({s: specs.basis(s) for s in specs.symbols()}).T
    df = df.join(b, on="symbol")
    df["traded"] = df.volume_lots > 0
    zero_px = (df[["open", "high", "low"]] <= 0).any(axis=1)
    bad = df[df.traded & zero_px]
    for r in bad.head(5).itertuples():
        report.add("futures.traded_without_prices", "error", f"{r.symbol} {r.expiry} {r.date}", "Volume > 0 but OHLC missing")
    report.add("futures.no_trade_days", "info", n=int((~df.traded).sum()),
               note="Volume 0: OHLC published as 0 and Close carried forward. Prices set to NaN, never used as fills")
    for c in ("open", "high", "low"):
        df.loc[~df.traded, c] = np.nan

    # VWAP per quote unit. Value carries +/- Rs 500 of rounding, which matters for one-lot GOLDPETAL days.
    grams = df.volume_lots * df.lot_g
    df["vwap"] = np.where(df.traded, df.value_lakh * 1e5 / grams * df.quote_g, np.nan)
    tol = VALUE_ROUNDING_INR / grams * df.quote_g + 1e-4 * df.close
    outside = df.traded & ((df.vwap < df.low - tol) | (df.vwap > df.high + tol))
    for sym, g in df[df.traded].groupby("symbol"):
        share = outside[g.index].mean()
        if share > 0.01:
            report.add("futures.vwap_outside_range", "error", f"{sym}: {share:.1%} of traded rows",
                       "Lot or quote grams in the spec file do not match the data")
        elif outside[g.index].any():
            for r in df.loc[g.index][outside[g.index]].head(3).itertuples():
                report.add("futures.vwap_outside_range", "warn", f"{r.symbol} {r.expiry} {r.date}: vwap {r.vwap:.0f} vs [{r.low:.0f}, {r.high:.0f}]",
                           "Isolated rows; lot size confirmed on the rest")
    if not outside.any():
        report.ok("futures.vwap_outside_range", "VWAP inside [Low, High] on every traded row: lot and quote grams confirmed")

    # On the last trading day the published Close is the settlement price (DDR), not a traded price.
    t = df[df.traded & ~((df.date == df.last_trading_day) & (df.expiry < asof))]
    ohlc_bad = t[(t.low > t[["open", "close"]].min(axis=1)) | (t.high < t[["open", "close"]].max(axis=1))]
    for r in ohlc_bad.head(5).itertuples():
        report.add("futures.ohlc_inconsistent", "warn", f"{r.symbol} {r.expiry} {r.date}: O {r.open} H {r.high} L {r.low} C {r.close}",
                   "Open or Close outside [Low, High] (Close is the last-half-hour VWAP)")
    if ohlc_bad.empty:
        report.ok("futures.ohlc_inconsistent", "Open and Close inside [Low, High] on every traded row")

    # Rs per gram at 999 basis: 995-quoted contracts (GOLD, GOLDM) scale by 999/995.
    k = (999 / df.purity) / df.quote_g
    for c in ("close", "open", "vwap"):
        df[f"{c}_g999"] = df[c] * k
    df["mid_g999"] = (df.high + df.low) / 2 * k

    # Compare each close with other symbols' contracts expiring within PEER_DAYS on the same day.
    t = df[df.traded][["date", "symbol", "expiry", "close_g999"]]
    m = t.merge(t, on="date", suffixes=("", "_p"))
    m = m[(m.symbol != m.symbol_p) & ((pd.to_datetime(m.expiry) - pd.to_datetime(m.expiry_p)).dt.days.abs() <= PEER_DAYS)]
    peer = m.groupby(["date", "symbol", "expiry"]).close_g999_p.median()
    dev = (100 * (t.set_index(["date", "symbol", "expiry"]).close_g999 / peer - 1)).dropna()
    out = dev[dev.abs() > OUTLIER_PCT]
    for (d, s_, x), v in out.head(5).items():
        report.add("futures.cross_contract_outlier", "warn", f"{s_} {x} {d}: {v:+.1f}%",
                   f"Close per gram more than {OUTLIER_PCT:.0f}% from other symbols expiring within {PEER_DAYS} days")
    if out.empty:
        report.ok("futures.cross_contract_outlier",
                  f"Every traded close within {OUTLIER_PCT:.0f}% of same-day peers expiring within {PEER_DAYS} days ({len(dev):,} rows compared)")
    return df


def calendar_and_tender(df, asof, report):
    """Trading days to expiry from the observed MCX calendar; weekday estimate past the last observed day."""
    cal = np.array(sorted(df.date.unique()), dtype="datetime64[D]")
    last = cal[-1]
    d = df.date.values.astype("datetime64[D]")
    e = pd.to_datetime(df.last_trading_day).values.astype("datetime64[D]")
    upto = np.minimum(e, last)
    known = np.searchsorted(cal, upto, side="right") - np.searchsorted(cal, d, side="right")
    extra = np.where(e > last, np.busday_count(last + 1, e + 1), 0)
    df["tdte"] = known + extra
    df["tdte_exact"] = e <= last

    ver = {(s, x): specs.version_for(s, x) for s, x in df[["symbol", "expiry"]].drop_duplicates().itertuples(index=False)}
    df["spec_version"] = [specs.version_id(s, ver[(s, x)]) for s, x in zip(df.symbol, df.expiry)]
    df["spec_verified"] = df.spec_version.notna()
    # Older contracts: tender days of the first version we hold, flagged as assumed via spec_verified.
    df["tender_days"] = [(ver[(s, x)] or specs.first_version(s))["tender"]["days"] for s, x in zip(df.symbol, df.expiry)]
    df["in_tender"] = df.tdte < df.tender_days
    n = df[~df.spec_verified][["symbol", "expiry"]].drop_duplicates()
    report.add("spec.version_not_held", "info", n=len(n),
               note="Contracts older than the first spec PDF we hold; basis is data-checked, tender days assumed from the first version")
    return df, cal


def contracts_table(df, cal, asof, report):
    g = df.groupby(["symbol", "expiry"])
    c = g.agg(first_date=("date", "min"), last_date=("date", "max"), last_trading_day=("last_trading_day", "first"),
              rows=("date", "size"), traded_days=("traded", "sum"),
              spec_version=("spec_version", "first"), tender_days=("tender_days", "first")).reset_index()
    c["status"] = np.where(c.expiry < asof, "expired", "live")
    c["expiry_brought_forward"] = (c.status == "expired") & (c.last_trading_day < c.expiry)
    cal_list = list(cal)
    tender_start = []
    for r in c.itertuples():
        ltd = np.datetime64(r.last_trading_day)
        if ltd <= cal[-1]:
            days = [x for x in cal_list if x <= ltd]
            tender_start.append(days[-r.tender_days].astype(date) if len(days) >= r.tender_days else None)
        else:
            tender_start.append(np.busday_offset(ltd, -(r.tender_days - 1), roll="backward").astype(date))
    c["tender_start"] = tender_start

    # Completeness: expired contracts should run to expiry, and have a row on every MCX trading day in between.
    for r in c[c.status == "expired"].itertuples():
        gap = int(np.searchsorted(cal, np.datetime64(r.expiry), side="right") - np.searchsorted(cal, np.datetime64(r.last_date), side="right"))
        if gap > EARLY_EXPIRY_MAX:
            report.add("futures.ends_before_expiry", "warn", f"{r.symbol} {r.expiry}: last row {r.last_date} ({gap} trading days early)",
                       "History stops well before expiry: likely an incomplete fetch")
        elif gap > 0:
            report.add("futures.expiry_brought_forward", "info", f"{r.symbol} {r.expiry} to {r.last_date}",
                       "MCX moved the last trading day earlier (no spot poll on the published expiry); last_trading_day used")
    missing = 0
    for (s, x), grp in g:
        span = cal[(cal >= np.datetime64(grp.date.min())) & (cal <= np.datetime64(grp.date.max()))]
        m = len(span) - len(grp)
        if m > 0:
            missing += m
            report.add("futures.missing_days", "warn", f"{s} {x}: {m} trading days missing", "Gaps inside a contract's life")
    if not missing:
        report.ok("futures.missing_days", "Every contract has a row on every MCX trading day of its life")
    return c


# --- spot and settlement -------------------------------------------------------------------------

def load_spot(report):
    rows = []
    for s in specs.symbols():
        sp = specs.spot(s)
        for f in sorted((RAW / "spot").glob(f"{sp['product']}_{sp['location']}_*.json")):
            rows += parse.spot_file(f, sp, report)
    df = pd.DataFrame(rows)
    key = ["product", "location", "ts"]
    conflicting = df.drop(columns="source").drop_duplicates().duplicated(key, keep=False)
    if conflicting.any():
        report.add("spot.conflicting_duplicates", "error", df[conflicting][key].head(1).to_dict("records"),
                   "Same poll appears twice with different prices")
    df = df.drop_duplicates(key).sort_values(key).reset_index(drop=True)
    pur = {specs.spot(s)["product"]: specs.spot(s)["purity"] for s in specs.symbols()}
    df["purity"] = df["product"].map(pur)
    df["price_g999"] = df.price / df.unit_g * 999 / df.purity

    # Carried-forward spot: when the physical market is shut (a spot holiday, Diwali week, the Covid lockdowns)
    # MCX republishes the previous day's last price. Such a day is stale; MCX's own 3-day DDR skips it
    # (verified: GOLDM Apr 2023 settles on 31 Mar, 3 Apr and 5 Apr, skipping the carried 4 Apr).
    daily = df.groupby(["product", "date"]).price.last().reset_index()
    daily["run"] = (daily.price != daily.groupby("product").price.shift()).cumsum()
    daily["run_len"] = daily.groupby("run").date.transform("size")
    daily["run_pos"] = daily.groupby("run").cumcount()
    stale_days = daily[daily.run_pos > 0]
    df["stale"] = df.set_index(["product", "date"]).index.isin(stale_days.set_index(["product", "date"]).index)
    report.add("spot.carried_forward_days", "info", n=len(stale_days),
               note="Product-days whose spot repeats the previous day's last price (spot market shut); polls marked stale")
    for (prod, run), g in stale_days[stale_days.run_len >= FROZEN_DAYS].groupby(["product", "run"]):
        report.add("spot.frozen", "info", f"{prod} {g.date.min()} to {g.date.max()} ({len(g) + 1} days at {g.price.iloc[0]:.0f})",
                   f"Spot unchanged for {FROZEN_DAYS}+ polling days (long market closure)")

    # GOLDTEN and GOLDGUINEA spots are GOLDM's Ahmedabad 995 spot x 999/995; check poll by poll.
    df["minute"] = df.ts.dt.floor("min")
    ref = df[df["product"] == "GOLDM"].set_index("minute").price_g999
    for p in ("GOLDTEN", "GOLDGUINEA"):
        s = df[df["product"] == p].set_index("minute").price_g999
        both = s.index.intersection(ref.index)
        bp = 1e4 * (s[both] / ref[both] - 1)
        bad = bp[bp.abs() > SPOT_TWIN_BP]
        if len(bad):
            report.add("spot.twin_mismatch", "warn", f"{p} {bad.index[0]}: {bad.iloc[0]:+.1f} bp (n={len(bad)} of {len(both)})",
                       f"Expected {p} spot = GOLDM spot x 999/995 at the same poll")
        else:
            report.ok(f"spot.twin_{p}", f"{p} spot = GOLDM x 999/995 on all {len(both)} shared polls (within {SPOT_TWIN_BP} bp)")
    return df.drop(columns="minute")


def settlement_table(fut, spot, contracts, cal, report):
    last_poll = spot.sort_values("ts").groupby(["product", "date"]).tail(1).set_index(["product", "date"])
    first_spot = spot.groupby("product").date.min()
    out = []
    for r in contracts[contracts.status == "expired"].itertuples():
        sp = specs.spot(r.symbol)
        prod = sp["product"]
        ltd = r.last_trading_day
        if prod not in first_spot or ltd < first_spot[prod]:
            continue
        v = specs.version_for(r.symbol, r.expiry)
        rule = (v or specs.first_version(r.symbol))["ddr"]["rule"]
        if (prod, ltd) not in last_poll.index:
            report.add("settlement.no_poll", "warn", f"{r.symbol} {r.expiry}", "No polled spot on the last trading day")
            continue
        if rule == "avg_last_poll_3d":
            # E0 plus the two previous trading days with a fresh poll (carried-forward days are skipped)
            prior = [x.astype(date) for x in cal[cal < np.datetime64(ltd)]][-15:]
            fresh = [d for d in prior if (prod, d) in last_poll.index and not last_poll.loc[(prod, d)].stale]
            days = fresh[-2:] + [ltd]
        else:
            days = [ltd]
        polls = [last_poll.loc[(prod, d)] for d in days]
        if len(polls) < (3 if rule == "avg_last_poll_3d" else 1):
            report.add("settlement.partial_polls", "warn", f"{r.symbol} {r.expiry}: {len(polls)} days", "Fewer fresh polls than the rule needs")
        assert sp["unit_g"] == specs.basis(r.symbol)["quote_g"], "spot unit must equal the quote unit"
        ddr = float(np.mean([p.price for p in polls]))
        reliable = not polls[-1].stale
        row = fut[(fut.symbol == r.symbol) & (fut.expiry == r.expiry) & (fut.date == ltd)]
        close = float(row.close.iloc[0]) if len(row) else np.nan
        out.append({
            "symbol": r.symbol, "expiry": r.expiry, "last_trading_day": ltd, "rule": rule, "rule_assumed": v is None,
            "poll_days": len(polls), "last_poll_ts": polls[-1].ts, "ddr": ddr, "ddr_reliable": reliable,
            "ddr_g999": ddr / sp["unit_g"] * 999 / sp["purity"],
            "expiry_close": close, "expiry_close_vs_ddr_bp": 1e4 * (close / ddr - 1) if close == close else np.nan,
        })
    st = pd.DataFrame(out)
    report.ok("settlement.rebuilt", f"DDR rebuilt for {len(st)} expired contracts from polled spot")
    # Until the Oct 2023 expiries MCX published the DDR as the last-day Close, so there the two must match:
    # an independent check of the rebuilt DDR. Later expiries publish a traded Close instead (kept as information).
    st["ddr_matches_close"] = st.expiry_close_vs_ddr_bp.abs() < 0.5
    st["close_is_ddr_era"] = st.expiry < CLOSE_IS_DDR_UNTIL
    for r in st[~st.ddr_reliable].itertuples():
        report.add("settlement.stale_spot", "info", f"{r.symbol} {r.expiry}", "DDR rebuilt from frozen spot; ddr_reliable = false")
    test = st[st.close_is_ddr_era & st.ddr_reliable]
    off = test[~test.ddr_matches_close]
    for r in off.head(5).itertuples():
        report.add("settlement.close_differs_from_ddr", "warn",
                   f"{r.symbol} {r.expiry}: close {r.expiry_close:.0f} vs rebuilt DDR {r.ddr:.0f} ({r.expiry_close_vs_ddr_bp:+.1f} bp)",
                   f"Pre-Oct 2023: rebuilt DDR differs from the published last-day close on {len(off)} of {len(test)} contracts")
    if off.empty:
        report.ok("settlement.close_differs_from_ddr",
                  f"Pre-Oct 2023: rebuilt DDR equals the published last-day close on all {len(test)} contracts with live spot")
    return st


# --- write -----------------------------------------------------------------------------------------

def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(asof=None, log=print):
    report = Report()
    asof = asof or date.today()
    fut = enrich_futures(add_last_trading_day(load_futures(report), asof), asof, report)
    fut, cal = calendar_and_tender(fut, asof, report)
    contracts = contracts_table(fut, cal, asof, report)
    spot = load_spot(report)
    settle = settlement_table(fut, spot, contracts, cal, report)

    SNAP.mkdir(parents=True, exist_ok=True)
    if report.errors():
        (SNAP / "VALIDATION_FAILED.md").write_text("# Validation failed\n\n" + report.markdown(), encoding="utf-8")
        raise BuildError(f"{len(report.errors())} check(s) failed; nothing written. See data/snapshot/VALIDATION_FAILED.md")
    (SNAP / "VALIDATION_FAILED.md").unlink(missing_ok=True)

    cols = ["date", "symbol", "expiry", "last_trading_day", "open", "high", "low", "close", "prev_close", "vwap", "volume_lots", "value_lakh",
            "oi_lots", "traded", "lot_g", "quote_g", "purity", "close_g999", "open_g999", "mid_g999", "vwap_g999",
            "tdte", "tdte_exact", "tender_days", "in_tender", "spec_version", "spec_verified", "source"]
    tables = {"futures_daily": fut[cols], "spot_polls": spot, "settlement": settle, "contracts": contracts}
    for name, t in tables.items():
        t.to_parquet(SNAP / f"{name}.parquet", index=False)

    raw_files = sorted(p for p in RAW.rglob("*") if p.is_file() and p.suffix in (".json", ".pdf") and not p.name.startswith("_"))
    raw_index = {str(p.relative_to(RAW)).replace("\\", "/"): sha256(p) for p in raw_files}
    manifest = {
        "built_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "data_asof": str(fut.date.max()),
        "spot_asof": str(spot.date.max()),
        "spec_file_sha256": sha256(specs.SPEC_FILE),
        "tables": {k: {"rows": int(len(v)), "sha256": sha256(SNAP / f"{k}.parquet")} for k, v in tables.items()},
        "coverage": {s: {"first": str(g.date.min()), "last": str(g.date.max()), "contracts": int(g.expiry.nunique())}
                     for s, g in fut.groupby("symbol")},
        "validation": report.summary(),
        "raw_files": len(raw_index),
        "raw_sha256": hashlib.sha256(json.dumps(raw_index, sort_keys=True).encode()).hexdigest(),
    }
    (SNAP / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    (SNAP / "raw_index.json").write_text(json.dumps(raw_index, indent=0, sort_keys=True), encoding="utf-8")
    (SNAP / "VALIDATION.md").write_text(
        f"# Snapshot validation\n\nBuilt {manifest['built_at']} · futures through {manifest['data_asof']} · "
        f"spot through {manifest['spot_asof']}\n\n" + report.markdown() + "\n", encoding="utf-8")
    log(f"snapshot written: " + ", ".join(f"{k} {v['rows']:,}" for k, v in manifest["tables"].items()))
    s = manifest["validation"]
    log(f"validation: {len(s['errors'])} errors, {len(s['warnings'])} warning types, {len(s['passed'])} checks passed")
    return manifest
