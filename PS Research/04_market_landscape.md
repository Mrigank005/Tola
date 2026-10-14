# 04 · Market Landscape: Products, Competitors, Gaps

## Who needs "commodity derivatives intelligence"?

| Segment | What they decide | What they use today | Their pain |
|---|---|---|---|
| Institutional commodity desks and hedge funds | Curve trades, hedges, relative value across venues | Bloomberg, LSEG Workspace, Platts/Argus price assessments, Kpler/Vortexa flows | Expensive. India-specific contract mechanics (polled spot, coins vs bars) sit outside these tools' focus. |
| Indian prop desks and arbitrageurs | Cross-contract and cash-futures arbitrage on MCX | Broker terminals, in-house Excel/Python, paid MCX feeds (TrueData, Global Datafeeds) | Fragmented data. Each contract's settlement reference and delivery terms have to be tracked by hand. |
| **Indian retail traders and small investors** (the fastest-growing group) | *Which* gold contract to hold, when to roll, whether to take delivery | Broker apps (Zerodha, Groww, Dhan, Upstox), TradingView, options apps (Quantsapp, Sensibull, Opstra) | Apps show price, OI and "days to expiry". **None show whether a contract is rich or cheap relative to the others or to its own settlement reference.** |
| Jewellers and SIP-style buyers taking delivery | Cheapest route to physical 999 gold | GOLDGUINEA and GOLDPETAL delivery, IBJA rates, digital gold | Hidden costs: the making charge (₹100/g on GOLDPETAL coins), tender-period margin, delivery centre. |
| Exchange and regulator (MCX product team, SEBI) | Is each contract variant fairly priced? Is retail protected? | Internal surveillance | A public, explainable "contract fairness" monitor would complement their work. SEBI's Feb 2026 circular already ties ETF valuation to exchange polled spot. |

## Tier 1: global terminals

| Product | Relevant features | Gap vs PS03 |
|---|---|---|
| **Bloomberg Terminal** ([commodities brochure](https://assets.bbhub.io/professional/sites/10/Proprietary-Commodity-Data-on-Bloomberg-Brochure.pdf)) | `CCRV` commodity curve analysis (historical curves, comparison against exchange data), `HS` spread analysis (time and product spreads), `CT` futures contract table, `COMM` catalogue. Sources: [CFI](https://corporatefinanceinstitute.com/resources/equities/bloomberg-functions-shortcuts-list/), [UManitoba cheat sheet](https://umanitoba.ca/asper/sites/asper/files/2021-08/Commodities%20for%20equities%20cheat%20sheet.pdf) | Generic spread tooling. No awareness of MCX polled-spot settlement references, coin/bar delivery forms or making charges. About US$30k/seat/yr (widely reported figure, not verified this session). |
| **LSEG Workspace** (replaced Eikon from 30 Jun 2025) ([updates](https://www.lseg.com/en/data-analytics/products/workspace/updates), [commodities workflows](https://www.lseg.com/en/data-analytics/products/workspace/redi-on-workspace-oems/extend-workspace-into-trading-workflow/commodities-workflows-in-workspace)) | `CURVE` futures curves, `CFPD` Commodity Forward Pricing Discovery app to *identify arbitrage*, `COTR` positioning, `CARGO` physical flows | Same: global, institution-priced, nothing India-retail-specific. |
| **S&P Global Commodity Insights (Platts)**, **Argus** | Price-assessment benchmarks and forward curves | Physical benchmarks. No exchange-contract relative value. |

## Tier 2: alternative-data commodity intelligence

| Company | What they do | Lesson for us |
|---|---|---|
| **Kpler** ([site](https://www.kpler.com/product/commodities)) | Vessel tracking for 36k+ ships, cargo flows, Kpler AI. Acquired **Spire Maritime (Apr 2025)**. Reported to exceed $100M ARR in 2024 ([Lodfy comparison](https://lodfy.app/blog/kpler-vs-vortexa-vs-argus-vs-sp-coal-trade-analytics)). | "Intelligence" means a proprietary *explanation* of price via fundamentals. Gold's fundamentals aren't shipping flows, but for our product the "fundamental" is **contract design**. |
| **Vortexa** ([site](https://www.vortexa.com/)) | Energy flows, ML destination prediction, about $500M valuation ([Asymmetrix](https://asymmetrixintelligence.substack.com/p/vortexa-500m-ev-energy-and-commodities)) | Same. |
| **ChAI** ([Silicon Canals](https://siliconcanals.com/chai-british-startup-uses-ai-forecast-prices-raw-materials-raises-e1-5m/), [Tracxn](https://tracxn.com/d/companies/chai/__2Fi4-4fkn1cGUoNTx8SLULL81wAkQZ0EHjIy1CVnHoQ)) | AI price forecasts for raw-material buyers using satellite and shipping data; about $1.7M raised | Forecasting is crowded and hard to prove. |
| **Gro Intelligence** (shut down **June 2024**) ([Semafor](https://www.semafor.com/article/06/04/2024/kenyan-ai-data-gro-intelligence-startup-shuts-down), [TechMoran](https://techmoran.com/2024/06/03/agricultural-data-platform-gro-intelligence-shuts-down-after-financial-struggles/)) | AI agri/climate insights; failed on product-market fit and funding | A cautionary tale for the pitch: "AI insights" without a clear decision-maker don't sell. Name a user and a decision. |
| **Permutable AI** ([blog](https://permutable.ai/7-best-alternative-data-providers-for-commodity-trading/)) | News and sentiment data for commodities | The news angle is commoditised. |

Market size: one estimate puts commodity services at $3.87B (2025) growing to $8.16B (2034), cited inside search-result summaries. **The primary source was not verified**, so don't put it on a slide without a source.

## Tier 3: Indian retail tools

| Product | What it shows for MCX gold | Gap |
|---|---|---|
| **Dhan** ([GOLDPETAL page](https://dhan.co/commodity/gold-petal-futures-summary/)) | LTP, OI and OI-change interpretation, days to expiry, a warning to exit before the last 3 trading days. Its title says "Premium Over Spot", but **the page gives no formula**. | Single contract only, no cross-contract normalisation, no settlement-reference basis. |
| **Groww**, **Upstox**, **5paisa**, **INDmoney**, **Angel One** (price pages) | Live price, chart, specs | Information pages, not analytics. |
| **Zerodha Varsity** ([gold part 1](https://zerodha.com/varsity/chapter/gold-part-1/), [part 2](https://zerodha.com/varsity/chapter/gold-part-2/)) | Education: variants, margins, delivery intent before expiry, why CME and MCX prices differ | Says cross-variant arbitrage is possible but needs quantity matching and is complicated by different expiries. **No tool.** |
| **Quantsapp** ([MCX option chain](https://www.quantsapp.com/option-chain/mcx)), **Sensibull**, **Opstra**, **Quintal Mind** | Option chains, OI, IV, payoff, backtests. Quantsapp and Quintal Mind cover MCX options. | Options-centric. No futures cross-contract relative value. |
| **TradingView** (MCX symbols such as `GOLDM1!`, `GOLDGUINEA1!`) | Charts of continuous series and community ideas | Continuous series hide the expiry roll, which the PS explicitly warns against. |
| **IBJA** ([ibjarates.com](https://www.ibjarates.com/)) | AM/PM benchmark rates for 999, 995, 916 and more | Spot only. |

## Tier 4: Indian data vendors

| Vendor | Offer | Cost |
|---|---|---|
| **TrueData** ([pricing](https://www.truedata.in/price)) | Authorised NSE/BSE/MCX real-time and historical data, API, plugins | Velocity Lite MCX plugin from ₹1,439.83/month. API pricing on request. |
| **Global Datafeeds** ([products](https://globaldatafeeds.in/products/)) | Authorised vendor. Tick, minute and day history for MCX. | On request |
| **MCX website** (free) | Bhavcopy (date-wise and per-contract range), **per-contract polled spot archive**, spec PDFs, circulars | Free, but behind Akamai bot protection. Chrome-TLS impersonation works (see 06). |

## Tier 5: direct hackathon competitors (Hack in Hills '26, PS03)

Full notes are in `01_github_repos.md §A`. Feature matrix (✓ = present in README or code, ~ = partial or assumed, ✗ = absent):

| Capability | gold-rv | auraspread | GoldLens | PALLAK CDI | goldparity | AurumIQ | GOLDINTEL | radar | cdi-terminal |
|---|---|---|---|---|---|---|---|---|---|
| Real MCX data | ✓ | ~ (synthetic fallback) | ~ | ? | ✓ (manual upload) | ~ | ~ | ✓ | ✗ |
| Automated daily fetch | ✗ | ~ (WAF fail-safe) | ~ | ✗ | ✗ | ~ (diagnostic) | ~ | ? | ✗ |
| Purity + unit normalisation | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ |
| Carry / expiry adjustment | ✓ | ✓ | ✓ | ~ (assumed rates) | ✓ | ? | ✓ | ✗ | ✗ |
| Walk-forward with t+1 fills | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ~ |
| Indian statutory costs | ✓ | ✓ | ✓ | ✓ | ~ | ✓ | ✓ | ✓ | ✗ |
| **Measured** slippage (OHLC estimator) | ✗ (assumed 5 bp) | ✗ | ✗ | ✗ | ✗ | ~ (bid-ask proxy) | ✗ | ✗ (2 bp assumed) | ✗ |
| Deflated Sharpe / multiple testing | ~ (t-stat) | ✗ | ✓ | ✗ | ~ (bootstrap) | ✗ | ✗ | ✗ | ✗ |
| Contract lifecycle / tender calendar | ✓ | ✓ (blackout) | ? | ✓ | ✗ | ✓ | ✓ | ✓ | ~ |
| **Exchange polled-spot (settlement reference) data** | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Versioned contract specs** (tender 5→3 days, margins, making charge) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Explains the structural small-lot premium** | ✗ (flags a regime break) | ✗ | ✗ | ✗ | ✗ | ✗ | ~ ("retail convenience premium" named) | ✗ | ✗ |
| Retail decision tool ("which contract should I hold?") | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |
| Pitch deck already built | ✓ (3D interactive) | ? | ✓ (demo script) | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

## Gaps we can exploit

1. **Settlement-reference blindness.** Every competitor compares futures with futures. Nobody uses MCX's **per-contract polled spot archive**: GOLDTEN, GOLDGUINEA and GOLDM against Ahmedabad spot, GOLDPETAL against Mumbai, GOLD and GOLDM against a 3-day average. We verified that the archive is reachable and that the references coincide per gram at expiry (₹14,820.6/g on 30 Sep 2026 for GOLDTEN and GOLDGUINEA).
2. **Contract design is treated as constant.** Specs changed: the tender period went from 5 to 3 days, tender margin from 5% to 8.34%, GOLDPETAL delivery from a "1 g coin" to a "1 g bar/coin", the ₹100/g making charge came in, and Good Delivery norms changed from 13 Jul 2026. gold-rv's unexplained ~250 bp GOLDPETAL regime shift (Dec 2024–Mar 2025) lines up in time with the Dec 2024 GOLDPETAL contract circular. That's a hypothesis to test, not a confirmed cause.
   - The **mechanism is unclear**: the making charge is paid buyer → seller *at delivery*, on top of a DDR that the futures price converges to anyway.
   - Its size (about 67 bp at ₹14,800/g) being close to the measured GOLDPETAL premium is a coincidence to test (S1).
   - Separately, it is a real cost for anyone **taking delivery**, so it goes into the chooser.
3. **The small-lot premium is real (G0: GO).** Across all 18 same-expiry cycles (Apr 2025 – Sep 2026), GOLDGUINEA trades at **+79 bp** and GOLDPETAL at **+94 bp** over GOLDTEN (VWAP, cycle-clustered CIs well above 0, positive in every cycle on every mark), despite an identical per-gram settlement reference.
   - It does **not** decay before delivery.
   - It is extinguished only by the final settlement, so it is lost in full by anyone holding into settlement or delivery.
   - It varies over time (cycle means 34–145 bp).
   - No competitor frames this as a *retail cost* or measures it.
4. **Costs are assumed, not measured.** Every competitor plugs in a slippage figure. The OHLC spread estimators (Abdi–Ranaldo 2017, EDGE 2024) make it measurable.
5. **No one serves a decision-maker.** All builds are "terminals for arbitrageurs" that conclude there is no arbitrage. A **retail "cheapest way to hold gold" chooser** and an **exchange or regulator "contract fairness" monitor** have real users even when the arbitrage verdict is "no edge".
6. **Live pipeline (finale, not Round 2).** Most builds are static snapshots or manual uploads. For Round 2, a committed snapshot plus a one-command refresh script is enough. A cron-driven daily refresh with a live alert log pays off at the finale (20 Nov), when we'd have weeks of untouched live data to show.
