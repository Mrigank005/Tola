# Snapshot validation

Built 2026-10-23T03:48:36+05:30 · futures through 2026-10-22 · spot through 2026-10-22

| Check | Result | Count | Note | Examples |
|---|---|---|---|---|
| `futures.cross_contract_outlier` | **WARN** | 2 | Close per gram more than 10% from other symbols expiring within 35 days | GOLDGUINEA 2020-03-31 2020-03-31: -12.3%<br>GOLDTEN 2026-07-31 2026-02-01: +10.4% |
| `settlement.partial_polls` | **WARN** | 1 | Fewer fresh polls than the rule needs | GOLDM 2020-05-05: 1 days |
| `spot.twin_mismatch` | **WARN** | 2 | Expected GOLDGUINEA spot = GOLDM spot x 999/995 at the same poll | GOLDTEN 2026-08-28 18:38:00: -1.0 bp (n=2 of 835)<br>GOLDGUINEA 2024-07-11 17:34:00: +4.9 bp (n=2 of 3318) |
| `futures.expiry_brought_forward` | **INFO** | 6 | MCX moved the last trading day earlier (no spot poll on the published expiry); last_trading_day used | GOLD 2022-10-05 to 2022-10-04<br>GOLDGUINEA 2025-03-31 to 2025-03-28<br>GOLDGUINEA 2026-03-31 to 2026-03-30<br>GOLDPETAL 2025-03-31 to 2025-03-28<br>GOLDPETAL 2026-03-31 to 2026-03-30 |
| `futures.no_trade_days` | **INFO** | 7160 | Volume 0: OHLC published as 0 and Close carried forward. Prices set to NaN, never used as fills |  |
| `settlement.stale_spot` | **INFO** | 12 | DDR rebuilt from frozen spot; ddr_reliable = false | GOLD 2020-04-03<br>GOLDGUINEA 2020-03-31<br>GOLDGUINEA 2020-04-30<br>GOLDGUINEA 2020-05-29<br>GOLDGUINEA 2021-04-30 |
| `spec.version_not_held` | **INFO** | 228 | Contracts older than the first spec PDF we hold; basis is data-checked, tender days assumed from the first version |  |
| `spot.carried_forward_days` | **INFO** | 664 | Product-days whose spot repeats the previous day's last price (spot market shut); polls marked stale |  |
| `spot.frozen` | **INFO** | 23 | Spot unchanged for 4+ polling days (long market closure) | GOLD 2020-03-23 to 2020-06-02 (49 days at 40989)<br>GOLD 2020-11-14 to 2020-11-18 (5 days at 50738)<br>GOLD 2021-04-23 to 2021-05-21 (21 days at 47569)<br>GOLD 2022-10-24 to 2022-10-28 (6 days at 49818)<br>GOLD 2023-11-12 to 2023-11-17 (7 days at 60029) |
| `futures.missing_days` | pass | 0 | Every contract has a row on every MCX trading day of its life | |
| `futures.ohlc_inconsistent` | pass | 0 | Open and Close inside [Low, High] on every traded row | |
| `futures.vwap_outside_range` | pass | 0 | VWAP inside [Low, High] on every traded row: lot and quote grams confirmed | |
| `settlement.close_differs_from_ddr` | pass | 0 | Pre-Oct 2023: rebuilt DDR equals the published last-day close on all 145 contracts with live spot | |
| `settlement.rebuilt` | pass | 0 | DDR rebuilt for 302 expired contracts from polled spot | |
