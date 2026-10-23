# 06 · Data Sources and APIs

"Verified" means we called the source from this machine on **13 Oct 2026** and received data. The sample files in `data_probe/` came from those calls.

## A. MCX (primary, free, verified)

### Access reality
- Plain `curl` and Python `requests` get an **HTTP 403 "Access Denied" from Akamai** (`errors.edgesuite.net`), even on the HTML page.
- **`curl_cffi` with `impersonate="chrome"`** (Chrome TLS fingerprint) returns **HTTP 200** for every endpoint below. No cookies or API key are needed.
- `mcxlib` 0.4 still calls the old `POST /backpage.aspx/GetDateWiseBhavCopy`, which **now returns a 404 page**. MCX moved to `GET` endpoints under each page's path. The page script `/assets/customjs/data.js` builds every URL as `location.origin + location.pathname + MethodName`.
- **Policy:** be polite (≥1.5 s between calls, a single session), cache every raw response, and **commit a Parquet snapshot** so the demo never depends on MCX being reachable. Endpoints can change again without notice.

### Endpoints

| Purpose | Request (all `GET`, header `X-Requested-With: XMLHttpRequest`) | Notes |
|---|---|---|
| **Daily bhavcopy, all contracts** | `https://www.mcxindia.com/market-data/bhavcopy/GetDateWiseBhavCopy?InstrumentName=FUTCOM&fromDate=DD/MM/YYYY` | Returns `{IsSuccess, Message, Data[], Metadata}`. On 9 Oct 2026 it gave 163 FUTCOM rows, 31 of them gold. Use `InstrumentName=ALL` to include options. |
| **Per-contract history (fast backfill)** | `.../market-data/bhavcopy/GetCommoditywiseBhavCopy?InstrumentName=FUTCOM&Symbol=GOLDTEN&Expiry=30OCT2026&fromDate=01/01/2026&toDate=09/10/2026` | **One call gives a contract's whole life** (e.g. 115 rows for GOLDTEN Oct-26). Backfill cost is about the number of contracts × 1 call, not the number of days. |
| **Polled spot archive (the settlement reference)** | `https://www.mcxindia.com/GetSpotMarketArchive?Product=GOLDTEN&Location=AHMEDABAD&fromDate=01/09/2026&toDate=30/09/2026&Session=0&culture=en` | Each contract has its **own spot series**: GOLD, GOLDM, GOLDGUINEA and GOLDTEN at AHMEDABAD; GOLDPETAL at MUMBAI. There are several polls per day (sessions). 30 Sep 2026 final polls: GOLDTEN ₹148,206/10 g, GOLDGUINEA ₹118,565/8 g (both exactly ₹14,820.6/g), GOLDPETAL ₹14,819/g, GOLDM ₹147,613/10 g at 995 (= ₹148,206 at 999). |
| Contract specs (versioned PDFs) | Linked from `https://www.mcxindia.com/products/bullion/gold` | e.g. `gold-petal-july-2026-contract-onwards.pdf`, `gold-ten-july-2026-contract-onwards.pdf`, `gold-mini-august-2026-contract-onwards….pdf`, plus older versions under `/docs/default-source/products/contract-specification/…`. |
| Circulars | `https://www.mcxindia.com/circulars` (page script `Circulars.js`) | Used to annotate spec changes. Also mirrored by brokers (steelcitynettrade.com) and TeamLease RegTech summaries. |
| Category-wise OI, trading statistics (monthly Excel) | `https://www.mcxindia.com/docs/default-source/market-data/historicaldata/{year}/{month}/…` (paths in `mcxlib`) | Participant-category open interest (hedgers vs others). Not verified this session. |
| Quotes, intraday graph | `/GetQuote`, `/GetIntradayGraph_Quote`, `/GetHistoricGraphData` (from `MarketData.js`) | Possible intraday cross-check. Not verified. |

### Bhavcopy field notes (verified on real rows)

| Field | Example | Gotcha |
|---|---|---|
| `Date` | `"10/09/2026"` for 9 Oct 2026 | **MM/DD/YYYY**, while the request uses DD/MM/YYYY (confirms the PS). goldparity's CSV export showed `"18 Sep 2026"`; `DateDisplay` carries that format. |
| `Symbol` | `"GOLDPETAL    "` | Space-padded; strip it. Options share the same symbol, so filter `InstrumentName == "FUTCOM"`. |
| `ExpiryDate` | `"30OCT2026"` | DDMMMYYYY. Key positions by `(symbol, expiry_date)`. |
| `Open/High/Low/Close` | `0.0` OHLC with `Close = PreviousClose` | **No-trade day:** OHLC is zero, Close is carried forward and Volume is 0. Never fill on these. |
| `Volume` | lots | `VolumeInThousands` is a text field in thousands of grams with a unit suffix (`"80.896 GRMS "` = 10,112 GOLDGUINEA lots × 8 g). |
| `Value` | `12190.73` (GOLDGUINEA Oct-26, 9 Oct 2026) | **Turnover in ₹ lakh.** Gives a daily **VWAP per gram = Value × 10⁵ ÷ (Volume × grams per lot)**, with lot grams GOLD 1000, GOLDM 100, GOLDTEN 10, GOLDGUINEA 8, GOLDPETAL 1. Verified: the VWAP fell inside [Low, High] for all 31 gold rows on 9 Oct 2026. VWAP doesn't depend on when the last trade happened, so it is the G0 mark that directly tests the Close-timing artefact. Also use it for turnover statistics. |
| `OpenInterest` | lots | |
| `Close` | — | Whether it is the **settlement price or the last traded price** is not stated. The PS calls it settlement. Expiry-day closes were *not* the DDR (GOLDGUINEA +68 bp above its own polled spot on 30 Sep 2026), so the final settlement must come from the polled spot / DDR, not from `Close`. |

**Holiday behaviour.** In our tests, 02/10/2026 (holiday) and 11/10/2026 (Sunday) returned `Data: []`, *not* the previous day's data. The PS warns MCX *may* return the most recent day. **Guard both cases**: empty data, and a returned `Date` that doesn't match the requested date.

**Coverage.** The date picker allows dates back to 01/01/2003. Gold rows exist for 2020 and 2025 (verified). GOLDTEN appears from Apr 2025.

### Contract mechanics (from the 2026 spec PDFs, downloaded 13 Oct 2026)

| Contract | Trading unit / quote | Purity, delivery form | Price basis | **Final settlement (DDR)** | Tender period |
|---|---|---|---|---|---|
| GOLD | 1 kg / ₹ per 10 g | 995, 1 kg bars | ex-Ahmedabad | **Simple average** of last polled spot on E0, E-1, E-2 | last 3 trading days |
| GOLDM | 100 g / ₹ per 10 g | 995, serially numbered bars (999 delivery earns × 999/995) | ex-Ahmedabad | **3-day average** as for GOLD | last 3 trading days |
| GOLDTEN | 10 g / ₹ per 10 g | 999, serially numbered 10 g | ex-Ahmedabad | Ahmedabad 995 spot × 999/995, **single poll** around 5 pm on expiry | last 3 trading days, +8.34% margin |
| GOLDGUINEA | 8 g / ₹ per 8 g | 999, 8 g bar/coin | ex-Ahmedabad | Ahmedabad 995 spot × 999/995 × 8/10, single poll | last 3 trading days, +8.34% |
| GOLDPETAL | 1 g / ₹ per 1 g | 999, 1 g bar/coin; ₹100/g making charge (Dec 2024 circular) | **ex-Mumbai** | **Mumbai** 995 spot × 999/995 × 1/10, single poll | last 3 trading days |

Changes between versions:
- **2025 specs:** tender period was the **last 5 trading days** with a 5% incremental margin. GOLDPETAL delivered as a "1 gram coin".
- **2026 specs:** tender period is **3 days** with **8.34%** margin. Delivery is a bar/coin from MCX-empanelled refiners.

Our spec table must be **versioned by contract month**.

> **Corrections (23 Oct 2026, from all 15 MCX spec PDFs, now in `data/specs/gold.yaml`):**
> - **Every small contract has a making charge**, paid by the buyer to the seller over the DDR: **GOLDTEN ₹300 per 10 g (₹30/g), GOLDGUINEA ₹200 per 8 g (₹25/g), GOLDPETAL ₹100 per 1 g.** It is in every version we hold (GOLDTEN since Apr 2025, GOLDGUINEA since Jan 2025, GOLDPETAL since Apr 2025). G0_RESULTS said GOLDGUINEA had none; that was wrong.
> - **The 5 → 3 day tender change came earlier than "2026 specs"**: with the Nov 2025 contracts for GOLDTEN and GOLDM, Dec 2025 for GOLDGUINEA and GOLDPETAL, and Aug 2026 for GOLD.
> - **`Close` is defined in the specs**: "closing price (weighted average price of last half an hour)". It is not the last traded price. On expiry day the settlement price is the DDR instead.
> - The delivery-period margin (after allocation) is the higher of 3% + 5-day 99% VaR or 25%, separate from the 8.34% tender-period margin.
>
> **Data behaviour found while building M1 (23 Oct 2026, details in `data/snapshot/VALIDATION.md`):**
> - **Until the Oct 2023 expiries, the last-day `Close` *was* the DDR.** Our DDR rebuilt from polled spot matches it on all 145 such contracts. From Oct 2023 the last-day Close is a traded price. (So the "expiry-day close isn't the DDR" note above holds only from Oct 2023.)
> - **MCX republishes the previous day's spot when the spot market is shut** (holidays, Diwali week, 49 days in the 2020 lockdown, 21 in 2021). GOLD/GOLDM's 3-day DDR skips those days.
> - **Expiries get brought forward** when the published expiry has no spot poll: 31 Mar 2025 → 28 Mar, 31 Mar 2026 → 30 Mar, GOLD 5 Oct 2022 → 4 Oct.
> - **Lead for S1:** from Oct 2023 to early 2024, GOLDPETAL's last-day close sat 125–255 bp *below* its own DDR while GOLDGUINEA's sat above. That is the pre-2025 GOLDPETAL discount seen at expiry.

## B. Rates, spot cross-checks and macro context

| Source | What | Access | Cost | Use |
|---|---|---|---|---|
| **FBIL** ([fbil.org.in](https://www.fbil.org.in/)) | T-bill benchmarks (14 d to 12 m, published since Aug 2017), MIBOR/MIBOR-OIS, USD/INR reference | Website download (needs a browser session) | Free | Compare implied gold carry with risk-free rates. Not verified via script. |
| **RBI DBIE** ([dbie.rbi.org.in](https://dbie.rbi.org.in/)) | Money-market rates, FX | Web download; `jugaad-data` has RBI helpers | Free | Fallback for rates. |
| **IBJA** ([ibjarates.com](https://www.ibjarates.com/)) | Daily AM/PM rates for 999, 995, 916 and more; 30-day PDFs | Scrape or PDF | Free | Independent spot cross-check of MCX polled spot. |
| **World Gold Council Goldhub** ([gold.org/goldhub](https://www.gold.org/goldhub)) | ETF flows (monthly Excel), India market updates, import duty notes | Free registration for some downloads | Free | Context and event annotation. |
| **CFTC Commitments of Traders** ([cftc.gov](https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm)) | COMEX gold positioning, weekly | CSV | Free | Global context only. |
| **yfinance** (`GC=F`, `INR=X`) | COMEX gold, USD/INR | Unofficial Yahoo scraper | Free, rate-limited | Global gold leg for attribution (MCX GOLD is the better local proxy). |
| FRED | US rates; LBMA gold series no longer offered (believed discontinued in 2022, not re-verified) | API key | Free | Low. |
| **Zerodha via `pyzdata`** | MCX intraday candles + OI | Needs a Zerodha session | Free for account holders; ToS risk | Stretch: intraday validation of EOD fills. |
| **TrueData / Global Datafeeds** | Authorised MCX tick, minute and EOD history | API | Paid (MCX plugin from ₹1,439.83/month; API on request) | Only if MCX scraping breaks. |

## C. News, weather and shipping (asked for; low relevance to PS03)

| Source | What | Access | Cost | Verdict |
|---|---|---|---|---|
| **GDELT DOC 2.0** ([blog](https://blog.gdeltproject.org/gdelt-doc-2-0-api-debuts/)) | Global news full-text search, 65 languages; `https://api.gdeltproject.org/api/v2/doc/doc?query=…&format=json` | No key | Free | Possible "what happened today" annotation for gold-wide volatility days. |
| NewsAPI.org | Headlines | Key; developer tier is not for production | Free dev tier | Low. |
| Google News RSS | Headlines by query | RSS | Free | Low. |
| **Open-Meteo** ([open-meteo.com](https://open-meteo.com/)) | Weather forecasts and history | No key; free for non-commercial use | Free | **Not relevant to gold.** Relevant only if we extend to agri (NCDEX). |
| **aisstream.io** ([aisstream.io](https://aisstream.io/)) | Real-time global AIS over WebSocket `wss://stream.aisstream.io/v0/stream` | Free key | Free | **Not relevant to gold** (bullion moves by air or vault). Relevant to energy (crude, natural gas). |
| NCDEX bhavcopy, data.gov.in | Agri futures and mandi prices | Web | Free | Out of scope. |

## D. Recommended data plan for the build

| Priority | Dataset | Source | Volume | Refresh |
|---|---|---|---|---|
| P0 | All gold futures (GOLD, GOLDM, GOLDTEN, GOLDGUINEA, GOLDPETAL), every expiry, Jan 2020 → today | `GetCommoditywiseBhavCopy`, one call per contract | About 5 symbols × ~12 expiries/yr × 7 yrs, so roughly 400 calls once | Daily: `GetDateWiseBhavCopy` |
| P0 | Polled spot per contract (all sessions) | `GetSpotMarketArchive`, monthly windows | About 5 × 80 months, so roughly 400 calls once | Daily |
| P0 | Versioned spec table + circular events | Spec PDFs (hand-curated YAML, about 15 versions) | Small | On change |
| P1 | 91-day T-bill (FBIL) or proxy | FBIL / RBI | Small | Weekly |
| P1 | IBJA 999/995 AM/PM | ibjarates.com | Small | Daily |
| P2 | Silver family (SILVER, SILVERM, SILVERMIC) | Same MCX endpoints | Similar | For the finale extension |
| P2 | Event list (import duty changes, Jan 2026 crash, SEBI circulars) | Articles (05) | Hand-curated | — |
