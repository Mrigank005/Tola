# 01 · GitHub Repositories

Stars, last push, language and licence come from the GitHub REST API, pulled on **13 Oct 2026**. "Reusable for us" judges what we can lift into a PS03 build in the remaining Round 2 window (13–31 Oct 2026).

Licence key: GPL/AGPL code can be *used as a reference* but copying it into our repo obliges us to release under the same licence. MIT/Apache-2.0 can be copied with attribution. "None" means no licence file, so legally all rights reserved: read it, don't copy it.

---

## A. Direct competitors: other Hack in Hills '26 PS03 teams

> **Superseded on 23 Oct 2026 by [08_competitor_tracker.md](08_competitor_tracker.md)** (42 repos; gold-rv renamed to `nexora-gold-rv-`). This table is kept as the 13 Oct baseline.

This is the most important section. At least **11 public repos** target the same problem statement. All were created between 1 and 8 Oct 2026, so Round 2 is crowded with near-identical builds.

| Repo | Created → last push | Stack | Data | What they do | What they don't do |
|---|---|---|---|---|---|
| [CodeByDivyansh-tech/gold-rv](https://github.com/CodeByDivyansh-tech/gold-rv) · live: gold-rv.vercel.app | 01 Oct → 07 Oct | Python pipeline → static HTML/JS site, pytest | **Real**: 11,954 EOD rows (Oct 2023–Sep 2026) + 55k-row history 2003–2026 shared by the "Parity" team | Normalization, carry (median implied 8.03%), rolling z, five-gate alerts, walk-forward with frozen params, attribution identity test, lifecycle calendar, honest "no persistent edge proven" verdict (t = 1.89), interactive 3D pitch deck | Slippage is **assumed** (5 bp/order), not measured, and their own break-even is 3.8 bp, so the verdict hinges on an assumption. Flags an unexplained ~250 bp GOLDPETAL basis regime shift (Dec 2024–Mar 2025) but doesn't explain it. No polled-spot (settlement-reference) data. |
| [manaslalwani190/auraspread](https://github.com/manaslalwani190/auraspread) | 03 Oct → 11 Oct | Python + Plotly static web ("The Assay Office") | Cached bhavcopy JSON **plus a synthetic GBM fallback** | "87.4% of the apparent gap is mechanical carry", MAD z-scores, walk-forward 60/40, break-even ₹22.10/10g vs ₹48 friction, look-ahead tests | Synthetic fallback weakens credibility. Treats the residual as noise rather than structure. |
| [Mayank-iitj/GoldLens](https://github.com/Mayank-iitj/GoldLens) | 04 Oct | Python, DuckDB, Streamlit + WebGL landing page | Ingest CLI, "simulation mode" | Carry-adjusted RV, OU half-life, Deflated Sharpe, "NO-GO" verdict | Heavy on presentation adjectives. Unclear how much is computed on real data. |
| [PALLAK-DEVI/commodity-derivatives-intelligence](https://github.com/PALLAK-DEVI/commodity-derivatives-intelligence) (team "Bits and Bytes") | 06 Oct → 08 Oct | Static JS, Plotly, KaTeX | Not stated | Carry modelled with an **assumed** repo 6.5% + storage 0.25% − lease 0.10%; integer-lot ILP solver; alpha/beta regression | Carry is assumed, not implied from the curve. No measured costs. |
| [jayanti614/goldparity](https://github.com/jayanti614/goldparity) (team "Tech Tribe") | 07 Oct → 08 Oct | Python backend | **Manual file upload** of the real MCX CSV (found that the CSV's trade date is "18 Sep 2026", and that options rows share symbols with futures) | Implied carry from each contract's own front vs next month; roll-down to a common expiry; 20-day z; 5-day hold backtest with bootstrap CI | No automated fetch. Says MCX needs session/cookie handling. |
| [rahulkumar1311/AurumIQ](https://github.com/rahulkumar1311/AurumIQ) · live: aurum-iq.vercel.app | 04 Oct | FastAPI + React/Recharts + SQLite | Real sample CSV + "WAF diagnostic" downloader | 50/25/25 dev/val/test split, OU half-life, liquidity score, audit trail tables | Second copy [aritradutta7858-netizen/AurumIQ](https://github.com/aritradutta7858-netizen/AurumIQ) (Kotlin) shows Sharpe 1.84 and 71% win rate on data marked `DataSource.DEMO`, i.e. synthetic. |
| [mahamunisarvesh738/MCX_GOLDINTEL](https://github.com/mahamunisarvesh738/MCX_GOLDINTEL) | 02 Oct → 10 Oct | PERN (Postgres/Express/React/Node), Electron | Seeder with "6,600+ contract cycles" | Six pillars mirroring the PS directions; includes GOLD (1 kg); "retail convenience premium" mentioned | JS quant engine; no evidence of measured costs. |
| [satyamkr11/gold-contract-radar](https://github.com/satyamkr11/gold-contract-radar) | 02 Oct | Python + Streamlit | Bhavcopy | Clean normalization maths, explicit Indian cost model (turnover 0.0021%, CTT 0.01%, stamp 0.002%, SEBI, GST), "insufficient data" guard | No carry adjustment described. |
| [krishsingh-ai/cdi-terminal](https://github.com/krishsingh-ai/cdi-terminal) · live: cdi-terminal.vercel.app | 03 Oct → 06 Oct | React + TS + Vite + Framer Motion | `mockData.ts` | UI shell: glassmorphism, auth modal, ticker | Frontend only, mock data. |
| govindbairagi3186/GOLDINTEL, /ARTHIQ | — | — | — | Appeared in search results | **Now 404** (deleted or made private). |

**What this means for us:** normalize → carry-adjust → z-score → walk-forward → costs → "no edge" verdict is now **table stakes**. Several teams (gold-rv especially) do it well on real data. Repeating it, even better, will not stand out. See `00_index.md` and the scope section of `research_summary.html` for the angles nobody covers.

---

## B. MCX / Indian market data access

| Repo | ★ | Last push | Lang | Licence | Notes | Reusable for us |
|---|---|---|---|---|---|---|
| [RuchiTanmay/mcxlib](https://github.com/RuchiTanmay/mcxlib) (PyPI `mcxlib` 0.4, 1 May 2026) | 11 | 2026-05-01 | Python | Apache-2.0 (PyPI page says MIT) | Wraps ~15 MCX endpoints: market watch, bhavcopy, historical, option chain, PCR, category-wise OI and turnover (Excel), iCOMDEX, PRO/CLI. | **Partially broken.** It uses `POST /backpage.aspx/GetDateWiseBhavCopy`, which now returns a 404 page; MCX moved to `GET /market-data/bhavcopy/GetDateWiseBhavCopy`. The Excel-based functions (`get_category_wise_oi`, `get_trading_statistics`) are worth trying for participant-category OI. Copy its header patterns, not its URLs. |
| [jugaad-py/jugaad-data](https://github.com/jugaad-py/jugaad-data) | 585 | 2026-10-06 | Python | custom (`LICENSE.YOLO.md`) | Mature NSE + RBI downloader with caching. No MCX. | Reference for **cache-first downloader design** and RBI rate pulls. |
| [marketcalls/openchart](https://github.com/marketcalls/openchart) | 77 | 2026-01-16 | Python | NOASSERTION | NSE/NFO intraday and EOD from the NSE charting backend. | Low (no MCX). |
| [vikassharma545/Historical-Market-data-From-Zerodha](https://github.com/vikassharma545/Historical-Market-data-From-Zerodha) (`pyzdata`) | 32 | 2026-10-01 | Python | MIT | OHLCV + OI candles incl. **MCX** via Zerodha's web session, no paid API. | Possible **intraday** source to validate EOD fills. Depends on a Zerodha login; terms-of-service risk. Stretch only. |
| [Khushalsawant/Download-Bhavcopy-from-MCX_India](https://github.com/Khushalsawant/Download-Bhavcopy-from-MCX_India) | 1 | 2019-07-16 | Python | None | Old single script. | None (stale). |
| [Sudarshan-FinanceTech/mcx-daily-commodity-data](https://github.com/Sudarshan-FinanceTech/mcx-daily-commodity-data) | 0 | 2026-09-29 | Python | None | Latest bhavcopy → FUTCOM rows → Excel history. | Idea only. |
| [lexiforest/curl_cffi](https://github.com/lexiforest/curl_cffi) | 6,704 | 2026-10-09 | Python | MIT | Python HTTP client that **impersonates Chrome's TLS fingerprint**. | **Critical.** In our test, plain `curl`/`requests` got an **Akamai 403** from mcxindia.com, while `curl_cffi` with `impersonate="chrome"` returned 200 on the page, bhavcopy, commodity-wise range and polled-spot endpoints. This is our ingestion layer. |
| [0xSaurabhx/IBJA-API](https://github.com/0xSaurabhx/IBJA-API) | 6 | 2026-09-18 | JS | None | Scrapes live IBJA 999/995 rates. | Reference for IBJA scraping (spot cross-check). |

---

## C. Futures term structure, rolling, calendar spreads, backtesting

| Repo | ★ | Last push | Lang | Licence | What it is | Reusable for us |
|---|---|---|---|---|---|---|
| [pst-group/pysystemtrade](https://github.com/pst-group/pysystemtrade) (Rob Carver; moved from robcarver17 in Jan 2026) | 3,552 | 2026-10-08 | Python | GPL-3.0 | Production systematic futures framework: **roll calendars, carry rule from current vs carry contract**, multiple-prices tables. | **Design reference** for contract-keyed storage ("multiple prices": price / forward / carry contract per date) and roll calendars. GPL, so don't copy code. |
| [mindymallory/RollFutures](https://github.com/mindymallory/RollFutures) | 1 | 2025-12-29 | HTML/R | None | Builds continuous nearby series (volume, DTE and OI roll rules). | Concept only. The PS explicitly warns *against* continuous series, which we avoid. |
| [GreaseMonkeyIT/futures-term-structure](https://github.com/GreaseMonkeyIT/futures-term-structure) | 0 | 2026-09-14 | Notebook | None | Energy carry signal `ln(M1/M2)×12`, tested after costs. | Formula check. |
| [blaquebaux/barrel](https://github.com/blaquebaux/barrel) | 0 | 2026-10-06 | Python | MIT | Roll-carry and contango-bleed study with an honest null framing. | Good example of how to **present a null result**. |
| [AnnieMahajan454/brent-spread-backtester](https://github.com/AnnieMahajan454/brent-spread-backtester) | 0 | 2026-09-30 | TS/Python | MIT | Walk-forward calendar and butterfly spreads, FastAPI + React, explains "why backtests mislead". | Our exact stack shape. MIT, so UI patterns can be borrowed. |
| [quantrocket-codeload/calspread](https://github.com/quantrocket-codeload/calspread) | 16 | 2026-10-09 | Notebook | Apache-2.0 | Bollinger mean reversion on CL calendar spreads; native vs synthetic spreads. | Shows why **synthetic spread fills differ from exchange spread fills**, which matters for our cost realism. |
| [sarthakdass/statarb](https://github.com/sarthakdass/statarb) | 0 | 2026-09-22 | Python | None | Walk-forward pairs: cointegration, Kalman hedge ratio, OU half-life, CI pipeline. | Reference for OU half-life and Kalman code structure. |
| [nautechsystems/nautilus_trader](https://github.com/nautechsystems/nautilus_trader) | 29,898 | 2026-10-13 | Rust/Python | LGPL-3.0 | Event-driven, production-grade backtest and live engine. | Overkill for EOD. Our custom ~300-line loop is safer to explain to judges. |
| [QuantConnect/Lean](https://github.com/QuantConnect/Lean) | 21,975 | 2026-10-12 | C# | Apache-2.0 | Full engine with futures chains. | No MCX data, so low value. |
| [mementum/backtrader](https://github.com/mementum/backtrader) | 23,460 | 2024-08-19 | Python | GPL-3.0 | Classic Python backtester, inactive since 2024. | Low. |
| [polakowo/vectorbt](https://github.com/polakowo/vectorbt) | 9,350 | 2026-10-09 | Python | NOASSERTION (Commons Clause) | Vectorised backtesting and parameter sweeps. | Fast grid sweeps for the DSR trial count. Watch licence restrictions. |
| [ranaroussi/quantstats](https://github.com/ranaroussi/quantstats) | 7,701 | 2026-09-27 | Python | Apache-2.0 | Tear sheets: Sharpe, drawdown, rolling beta. | **Use** for performance stats. |

---

## D. Statistical rigour and microstructure

| Repo | ★ | Last push | Licence | Reusable for us |
|---|---|---|---|---|
| [esvhd/pypbo](https://github.com/esvhd/pypbo) | 143 | 2026-07-06 | AGPL-3.0 | Reference implementation of PBO (CSCV) and DSR. AGPL, so re-implement the ~40 lines of DSR ourselves. Several small MIT re-implementations also exist (e.g. `tulinette/backtest-overfitting-lab`, `WatchTree-19/overfit`). |
| [eguidotti/bidask](https://github.com/eguidotti/bidask) | 136 | 2025-10-13 | MIT | **High value.** Implements the Ardia–Guidotti–Kroencke (2024) "EDGE" estimator of bid-ask spread from **daily OHLC**, which is exactly what the bhavcopy gives us. R package, also on PyPI as `bidask`. Lets us **measure** slippage per contract per day instead of assuming 5 bp the way gold-rv does. |
| [bashtage/arch](https://github.com/bashtage/arch) | 1,594 | 2026-10-12 | NCSA-style | GARCH/HAR volatility, bootstrap (stationary/block bootstrap for CIs), unit-root tests. **Use** for block-bootstrap confidence intervals. |

---

## E. Pricing libraries and terminals

| Repo | ★ | Last push | Licence | Notes |
|---|---|---|---|---|
| [lballabio/QuantLib-SWIG](https://github.com/lballabio/QuantLib-SWIG) | 403 (core QuantLib is far larger) | 2026-10-12 | BSD-style | Black-76 for options on futures, curve bootstrapping. Only needed if we add MCX gold **options**, which is out of scope. |
| [xqguo/CommodQuant](https://github.com/xqguo/CommodQuant) | 12 | 2025-06-30 | MIT | F# commodity pricing toolkit. Reference only. |
| [OpenBB-finance/OpenBB](https://github.com/OpenBB-finance/OpenBB) (API now redirects to `openbq-org/OpenBB`) | 74,172 | 2026-10-12 | NOASSERTION (AGPL core) | `obb.derivatives.futures.curve()` covers CBOE/yfinance/Deribit, **not MCX**. Useful only for COMEX gold context. |
| [Hitheshkaranth/OpenTerminalUI](https://github.com/Hitheshkaranth/OpenTerminalUI) | 286 | 2026-10-06 | MIT | React 18 + Vite + Tailwind + lightweight-charts v5, FastAPI backend, screening, alerts. **Closest open-source "terminal" UI to borrow layout patterns from.** |

---

## F. News, sentiment and forecasting models

| Repo | ★ | Last push | Licence | Relevance |
|---|---|---|---|---|
| [ProsusAI/finBERT](https://github.com/ProsusAI/finBERT) | 2,252 | 2026-10-12 | Apache-2.0 | Financial sentiment classifier. Literature (02_research_papers) shows it complements LLM sentiment. Low priority for a relative-value product, because news moves *all* gold contracts together. |
| [Josshua-DSA/ARCAS](https://github.com/Josshua-DSA/ARCAS) | 0 | 2026-10-12 | None | News → calibrated bullish/bearish impact for gold, silver, USD, using hybrid LLM extraction. Idea reference. |
| [pranav797/news-sentiment-pipeline](https://github.com/pranav797/news-sentiment-pipeline) | 0 | 2026-10-13 | None | RSS + prices, LLM + FinBERT scoring, DuckDB, FastAPI, Streamlit. Same stack shape as ours. |
| [amazon-science/chronos-forecasting](https://github.com/amazon-science/chronos-forecasting) | 6,065 | 2026-10-05 | Apache-2.0 | Zero-shot time-series foundation model. A 2026 study finds TSFMs don't reliably beat HAR for volatility, so not worth our time. |
| [google-research/timesfm](https://github.com/google-research/timesfm) | 34,400 | 2026-09-29 | Apache-2.0 | Same conclusion as Chronos. |
| Gold-price-prediction repos (e.g. [MohammadvHossein/predict-gold-price](https://github.com/MohammadvHossein/predict-gold-price), [AnthonyRui/Gold-Price-Forecasting-ML-Macroeconomic-Data](https://github.com/AnthonyRui/Gold-Price-Forecasting-ML-Macroeconomic-Data), [R-Mahesh45/...](https://github.com/R-Mahesh45/Gold-Price-Prediction-Using-Machine-Learning)) | small | — | mixed | Mostly LSTM/RF on *outright* gold, often claiming "97% accuracy". **Irrelevant to PS03**, which explicitly asks to separate strategy from gold-price direction. Useful only as an example of what *not* to pitch. |

---

## G. Visualisation and storage

| Repo | ★ | Last push | Licence | Use |
|---|---|---|---|---|
| [apache/echarts](https://github.com/apache/echarts) | 67,488 | 2026-10-12 | Apache-2.0 | Heatmaps, Gantt-style custom series (contract calendar), waterfalls, mark areas (tender shading). |
| [tradingview/lightweight-charts](https://github.com/tradingview/lightweight-charts) | 17,551 | 2026-10-12 | Apache-2.0 | Price and spread time series that look like a trading desk. |
| [duckdb/duckdb](https://github.com/duckdb/duckdb) | 42,147 | 2026-10-13 | MIT | Single-file analytical store over Parquet. |

---

## Reusability verdict

| Priority | Take | From |
|---|---|---|
| Must | Chrome-TLS impersonating HTTP client | `curl_cffi` |
| Must | OHLC spread estimator for measured slippage | `bidask` (EDGE) |
| Must | Block bootstrap, tear-sheet metrics | `arch`, `quantstats` |
| Should | Contract-keyed "multiple prices" storage idea, roll calendar concept | `pysystemtrade` (design only) |
| Should | Terminal layout patterns | `OpenTerminalUI`, `brent-spread-backtester` (MIT) |
| Should | Participant-category OI Excel parsers | `mcxlib` (Apache-2.0), after fixing URLs |
| Avoid | Gold *price* forecasting models, TSFMs, generic sentiment | Off-problem for PS03 |
| Study, don't copy | Competitors' methods and their documented limitations | gold-rv, auraspread, goldparity |
