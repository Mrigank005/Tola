# Data

Everything Tola shows comes from the committed snapshot in `snapshot/`, so the app never depends on MCX being reachable.

## Refresh

```bash
pip install -r requirements.txt
python -m tola.refresh            # fetch new or still-live MCX data, validate, rebuild snapshot/
python -m tola.refresh --offline  # rebuild snapshot/ from the local raw cache, no network
python -m pytest -q               # parser, spec and snapshot checks
```

A refresh from an empty cache took 189 MCX calls (the G0 cache seeds the rest). A daily refresh is about 37 calls (around 2 minutes). If any validation **error** fires, nothing is written and the reasons go to `snapshot/VALIDATION_FAILED.md`.

## Layout

| Path | In git | What |
|---|---|---|
| `specs/rates.yaml` | yes | RBI repo-rate history with sources (risk-free proxy before FBIL coverage). |
| `specs/gold.yaml` | yes | Contract specs versioned by expiry month. Every value is copied from an MCX PDF. |
| `raw/specs/*.pdf` | yes | The 15 MCX spec PDFs behind `gold.yaml` (downloaded 23 Oct 2026). |
| `raw/contract/`, `raw/spot/`, `raw/datewise/` | no | Every MCX response, byte for byte. Rebuilt by the refresh; their hashes are in `snapshot/raw_index.json`. |
| `snapshot/*.parquet` | yes | The tables below. |
| `snapshot/manifest.json` | yes | Build time, data as-of dates, row counts, table and spec hashes, validation summary. |
| `snapshot/VALIDATION.md` | yes | Every check, what it found, with examples. |

## Tables

**`futures_daily`**: one row per contract per trading day.

| Column | Meaning |
|---|---|
| `date`, `symbol`, `expiry` | Trading day, contract symbol, published expiry date |
| `last_trading_day` | The contract's real last trading day. MCX sometimes brings an expiry forward when the spot market is shut on the published date (31 Mar 2025 → 28 Mar, 31 Mar 2026 → 30 Mar, 5 Oct 2022 → 4 Oct). For live contracts it equals `expiry`. |
| `open`, `high`, `low`, `close`, `prev_close` | As published, ₹ per quote unit (10 g for GOLD, GOLDM and GOLDTEN; 8 g GOLDGUINEA; 1 g GOLDPETAL). `close` is the weighted average of the last half hour (per the spec PDFs). On no-trade days `open`, `high` and `low` are NaN and `close` is MCX's carried-forward value. |
| `vwap` | Value × 10⁵ ÷ (volume × lot grams), in quote units. Accurate to ±₹500 of turnover, which matters only on one-lot GOLDPETAL days. |
| `volume_lots`, `value_lakh`, `oi_lots`, `traded` | Volume (lots), turnover (₹ lakh), open interest (lots), volume > 0 |
| `lot_g`, `quote_g`, `purity` | Contract basis from the spec file |
| `close_g999`, `open_g999`, `mid_g999`, `vwap_g999` | ₹ per gram at 999 purity. GOLD and GOLDM (995) are scaled by 999/995, which is how MCX itself converts. |
| `tdte`, `tdte_exact` | Trading days to `last_trading_day` (0 on that day). Counted on the MCX trading calendar seen in the data; past the last observed day it is a weekday estimate (`tdte_exact = false`). |
| `tender_days`, `in_tender` | Tender window length for that contract's spec version, and whether the day falls inside it |
| `spec_version`, `spec_verified` | e.g. `GOLDTEN@2025-11`. Null / false for contracts older than the first spec PDF we hold; for those, tender days are assumed from the first version. |
| `source` | Raw file the row came from |

**`spot_polls`**: every MCX polled spot price. `ts` is IST. `price` is per `unit_g` at the product's own purity; `price_g999` is per gram at 999. GOLDTEN, GOLDGUINEA and GOLDPETAL spots are published at 999, GOLD and GOLDM at 995. `stale` marks polls on days when MCX just republished the previous day's price because the spot market was shut: single holidays, Diwali week every year, and the 2020 and 2021 lockdowns (49 and 21 days).

**`settlement`**: the final settlement price (DDR) of every expired contract with spot coverage, rebuilt from polled spot using the spec's rule. The small contracts use the last poll on the last trading day. GOLD and GOLDM average the last polls of the last trading day and the two previous days with a *fresh* poll (MCX skips carried-forward days). `ddr_reliable` is false when the settlement-day spot was stale.

**Verified:** for expiries before Oct 2023, MCX published the DDR as the last-day close, and the rebuilt DDR equals it on **all 145** contracts with live spot (`close_is_ddr_era`, `ddr_matches_close`). From the Oct 2023 expiries the last-day close is a traded price, so `expiry_close_vs_ddr_bp` there is information, not a check.

**`contracts`**: one row per contract: first and last row, `last_trading_day`, `expiry_brought_forward`, rows, traded days, spec version, tender start date, `expired` or `live`.

**`basis_daily`** (M2): one row per traded contract-day. The futures price split into terms that add up exactly, all in bp against the same day's Ahmedabad 999 spot (`ref_spot_g999`):

| Column | Meaning |
|---|---|
| `basis_total_bp` | 1e4 · ln(close_g999 / ref_spot_g999) |
| `timing_bp` | The day's common level: spot is polled around 5–6 pm, the close is the last half hour to about 11:30 pm. Intercept of the benchmark curve. |
| `carry_bp` | The day's implied carry × time to the contract's effective settlement date (`tau_days`; a day earlier for 3-day-average contracts) |
| `reference_bp` | Own polled spot vs Ahmedabad 999 (GOLDPETAL's Mumbai spot; about 0 elsewhere) |
| `residual_bp` | What is left: the small-lot premium |
| `own_basis_bp` | Basis to the contract's own polled spot (= total − reference) |
| `fair_g999` | ref spot × exp((timing + carry + reference) / 1e4): the price with no residual |
| `making_charge_inr_g`, `making_charge_bp`, `tender_margin_pct` | Delivery terms, reported beside the residual and not subtracted (they are paid outside the futures price) |

**`curve_daily`** (M2): one row per trading day. `timing_bp`, `carry_pa` (annualised, continuous) and fit quality from the benchmark regression (GOLD and GOLDM, ₹1 Cr+ turnover, outside tender). `carry_source` is `fit`, `carried` (previous carry, at most 10 days) or `none`. `rf_pct` and `rf_source` give the FBIL 3-month T-bill, or the RBI repo rate before FBIL coverage, and `carry_minus_rf_pct` is the gap.

**`tbill_3m`**: the FBIL 3-month T-bill benchmark, accumulated across refreshes (FBIL's public endpoint serves only 12 months). The repo-rate table with sources is in `specs/rates.yaml`.

## Known limits

- The DDR is rebuilt from published polls, not read from an MCX settlement file. It is verified against MCX's published settlements up to Sep 2023; later DDRs use the same rule but have no published value to check against.
- Spec PDFs before Jan 2025 (GOLDGUINEA), Apr 2025 (GOLDPETAL), Nov 2025 (GOLDM) and Feb 2026 (GOLD) are not held. Lot size and quote unit for those years are confirmed by the data (VWAP inside the day's range); purity and tender rules are assumed.
- Trading days to expiry for live contracts ignore future MCX holidays.
