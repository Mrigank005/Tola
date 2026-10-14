# 05 · Articles, Reports, Trends and Pain Points

## A. MCX and the Indian bullion derivatives boom

- **MCX FY26 results (published May 2026).**
  - **The "205%" is Q4 FY26 revenue growth**, not full-year: consolidated revenue from operations was ₹889 Cr vs ₹291 Cr in Q4 FY25.
  - FY26 revenue roughly doubled to ₹2,302 Cr, and FY26 PAT was ₹1,332 Cr (+138%).
  - FY26 ADT was ₹5.4 lakh crore (+145%), and bullion "grew more than 4x".
  - Sources: [DSIJ](https://insights.dsij.in/dsijarticledetail/mcx-q4-results-pat-surges-291-revenue-jumps-205-in-q4-fy26-profit-doubles-to-rs-1332-crore-id003-56986), [ScanX](https://scanx.trade/stock-market-news/companies/mcx-delivers-record-fy26-performance-pat-more-than-doubles-to-rs-1-332-crores-total-income-up-101-yoy/39820418).
  - [FOW (12 May 2026, paywalled)](https://www.fow.com/insights/indias-mcx-sees-205-fy26-revenue-surge-on-bullion-and-energy-derivatives-growth) headlines "205% FY26 revenue surge" and "bullion ADT +496%". That **mislabels the 205% as FY26** and cites no MCX source.
  - The 496% ("~6x") also sits oddly with the ">4x" bullion figure.
  - **Before any slide, open MCX's own Q4 FY26 results release.**
  - *Why it matters:* our market is booming, not niche, and judges will recognise it.
- **Bullion's share of MCX ADT rose from 44% to 57%** ✅. The release says "Bullion segment has increased its share in ADT from 44% to 57%", supported by the launch of Gold Mini and Gold Ten futures. Q2 FY26 futures-and-options ADT was ₹4,11,270 Cr, up 87% from ₹2,20,249 Cr. **Primary source:** MCX Q2 FY26 results press release, board approval 6 Nov 2025 ([mirror](https://uk.marketscreener.com/news/multi-commodity-exchange-of-india-mcx-q2-fy26-results-ce7d5cd3d98ff020), [BSE filing PDF](https://bsmedia.business-standard.com/_media/bs/data/announcements/bse/06112025/729e51e7-7b6e-42fc-9ea0-6c58e9179c95.pdf)). The comparison is Q2 FY26 vs Q2 FY25, so say so on any slide.
  - *Why it matters:* the small variants are a large share of activity, so a small-lot premium affects many traders.
- **Record bullion futures turnover of ₹5,563 Cr in one day.** That split into GOLDTEN ₹2,046 Cr, GOLDGUINEA ₹1,031 Cr and GOLDPETAL ₹2,486 Cr. Source: [MCX on X](https://x.com/MCXIndialtd/status/2013930573988048901). The post date wasn't visible, but the status ID points to roughly Jan 2026.
  - *Why it matters:* GOLDPETAL turnover alone rivalled GOLDTEN, which confirms retail-scale participation in the 1 g contract.
  - ⚠ **Not verified.** X returns 402 to scripts, so the post and its date couldn't be opened. Don't put it on a slide as is. Better: compute per-contract turnover ourselves from the bhavcopy `Value` field for a date we choose, so the number is ours and reproducible.
- **GOLDTEN launched on 1 Apr 2025.** Specs at launch: 10 g at 999 purity, ex-Ahmedabad. Settlement price (DDR) = Ahmedabad 995 spot × 999/995. Initial daily price limit 3%. Sources: [HDFC Sky](https://hdfcsky.com/blogs/share-market/gold-ten-10g-futures-set-to-launch-on-mcx-from-1st-april-2025), [Zee Biz](https://www.zeebiz.com/personal-finance/news-10-gm-gold-futures-contract-mcx-trading-from-april-1-2025-sip-transparent-price-discovery-retail-investor-353191).
  - *Why it matters:* GOLDTEN history starts in 2025, as the PS says. The GOLDTEN Oct-2026 contract first traded on 5 Jan 2026 according to our probe.
- **GOLDPETAL April 2025 contract (circular MCX/TRD/858/2024, 31 Dec 2024).** Buyers pay **₹100 per 1 g coin over the DDR** as a making charge to the seller at delivery. Source: [TeamLease RegTech](https://www.teamleaseregtech.com/updates/article/38209/mcx-notified-regarding-the-commencement-of-futures-trading-in-gold-pet/).
  - *Why it matters:* a contract-specific delivery cost of about 0.67–1.2% of the price per gram, depending on the gold price. Its timing coincides with the GOLDPETAL basis shift that gold-rv flagged.
- **MCX extended Good Delivery to BIS-standard gold and silver from 13 Jul 2026.** Source: [Business Standard](https://www.business-standard.com/markets/capital-market-news/mcx-expands-gold-delivery-ecosystem-aligns-bis-standard-bullion-with-good-delivery-norms-126070600841_1.html).
  - *Why it matters:* another dated change to deliverable supply. The 2026 spec PDFs now name "MCX empanelled domestic refiners".
- **Launch calendars for gold variants keep changing.** Sources: [MarketScreener](https://www.marketscreener.com/news/multi-commodity-exchange-of-india-modification-in-launch-calendar-of-gold-mini-gold-ten-gold-gui-ce7d59d3d88bf32c), [circular MCX/TRD/456/2025](https://www.steelcitynettrade.com/Circulars/Modification%20in%20Launch%20Calendar%20of%20Gold%20Mini,%20Gold%20Ten,%20Gold%20Guinea.pdf).
  - *Why it matters:* listing dates should be inferred from the bhavcopy itself, not hard-coded.

## B. Regulation (SEBI)

- **SEBI circular, 26 Feb 2026.** Gold and silver ETFs must value physical bullion using **domestic polled spot prices published by exchanges** (the MCX benchmark). Sources: [Samco](https://www.samco.in/knowledge-center/articles/gold-and-silver-etf-valuation-rules-changed-how-sebis-new-framework-will-impact-etf-nav-from-april-2026-stock-market-today/), [Business Upturn](https://www.businessupturn.com/sectors/commodities/sebi-changes-gold-and-silver-etf-pricing-rule-what-it-means-for-mcx-and-investors/).
  - *Why it matters:* polled spot is now a **regulated benchmark** for ETF valuation, which gives our "basis to own polled spot" metric policy relevance.
- **SEBI consultation paper, May 2026.** Proposes doubling client-level position limits in commodity derivatives, a graduated penalty structure, and removing the Close-to-the-Money (CTM) option-series mechanism. Sources: [CorpLaw Updates](https://www.corplawupdates.in/updates/sebi-position-limits-penalty-commodity-derivatives-may-2026), [Kotak Neo](https://www.kotakneo.com/news/market-news/sebi-derivatives-market-overhaul-commodity-norms-simplified-2026/), [Zee Biz](https://www.zeebiz.com/market-news/news-mcx-shares-hit-fresh-highs-as-sebi-signals-overhaul-of-commodity-derivatives-gold-silver-at-record-levels-386258).
  - *Why it matters:* the regulatory momentum is toward deeper commodity markets. Useful for the "impact" slide.
- **SEBI revised settlement guarantee fund rules for commodity derivatives** (stress-testing coverage). Source: [SRP](https://www.structuredretailproducts.com/insights/82912/indian-market-regulator-revises-sgf-rules-for-commodity-derivatives).
  - *Why it matters:* background only.
- **Commodity transaction tax (CTT) is 0.01% on the sell side of non-agricultural futures** (0.05% on options), with no change in FY25. Sources: [Rupeezy](https://rupeezy.in/blog/commodity-transaction-tax), [BankBazaar](https://www.bankbazaar.com/tax/commodity-transaction-tax.html).
  - *Why it matters:* a cost-model input.
  - **Cross-checked against [Zerodha's charges page](https://zerodha.com/charges/)** (13 Oct 2026), commodity futures, non-agri:
    - CTT **0.01% on the sell side**;
    - MCX transaction charge **0.0021%**;
    - SEBI ₹10/crore;
    - stamp duty **0.002%** on the buy side;
    - GST 18% on brokerage + SEBI + transaction charges;
    - brokerage **0.03% or ₹20 per executed order, whichever is lower**.
  - AurumIQ's 0.0125% looks wrong.
  - Still **confirm against a real contract note** before the final numbers.
  - **Cost-model implication (Zerodha rates):** with the 0.03% cap, a single ₹15k GOLDPETAL lot pays about **3 bp brokerage per order**, while a multi-lot order hits the ₹20 cap and pays far less. Small-lot costs depend on order size, so the chooser must take quantity as an input.
  - **Brokerage is broker-specific**, so the chooser makes the broker a parameter, with "Zerodha rates" as a labelled default preset.
  - Statutory items (CTT, stamp duty, SEBI fee, MCX transaction charge, GST) are the same across brokers.

## C. Gold market events that act as regime markers

- **Gold crash, Jan–Mar 2026.**
  - **Checked against market data:** COMEX gold front-month (`GC=F` via yfinance) made an intraday high of **$5,586 on Thu 29 Jan 2026**, then fell from a $5,318 close to a $4,745 close on **Fri 30 Jan (−10.8%)**.
  - The widely repeated "$5,600 on 28 Jan" and "−12% on 31 Jan" are rounded and misdated in secondary sources. 31 Jan 2026 was a Saturday.
  - The −31% silver figure and the "about 4% MCX decline" are **unverified** (secondary blogs only: [Sahi](https://www.sahi.com/blogs/why-gold-is-falling-even-as-the-world-burns), now HTTP 410; [Bullion Trading LLC](https://bulliontradingllc.com/blog/gold-and-silver-price-crash-january-2026/); [Finance Magnates](https://www.financemagnates.com/trending/why-is-gold-crashing-how-low-can-gold-go-and-gold-price-prediction-2026/)).
  - For slides, use our own MCX bhavcopy numbers for the Indian move.
  - *Why it matters:* gold-rv found its entire unseen-year profit came from trades closed in this crash. Any backtest must report results with and without this window.
- **Import duty swings.** India cut gold import duty **from 15% to 6% in Jul 2024** (5% basic + 1% AIDC; [WGC](https://www.gold.org/goldhub/gold-focus/2024/07/indian-gold-import-duties-reduced-lowest-level-over-decade), [Kitco](https://www.kitco.com/news/off-the-wire/2024-07-23/india-slashes-import-tax-gold-silver-tackle-smuggling)). It **raised it back to 15% in May 2026** ([WGC India update](https://www.gold.org/goldhub/gold-focus/2026/05/india-gold-market-update-import-tightening), [Bigul](https://bigul.co/blog/market-update/gold-import-duty-hiked-to-15-what-changes-for-prices-demand-and-investors-in-india), [EBC](https://www.ebc.com/forex/gold-import-duty-hike-reopens-india-smuggling-premium-risk)).
  - *Why it matters:* MCX prices are quoted "inclusive of import duty", so these are level shifts for every contract. They should cancel in relative value but may shift dealer premiums and city spreads, so annotate them on charts.
- **Current level.** MCX gold was about ₹1.50 lakh/10 g in mid-Oct 2026 (Goodreturns, 12 Oct 2026), consistent with our probe: GOLDM Nov at ₹1,50,130 on 9 Oct. 24K city rates on 13 Oct were Mumbai ₹149,670 and Ahmedabad ₹149,710 per 10 g, a difference of only about 3 bp. Source: [search snippet / Goodreturns](https://goodreturns.in/news/gold-rates-silver-rates-today-12-10-2026-live-spot-gold-mcx-gold-silver-price-24k-22k-18k-gold-price-1540727.html).
  - *Why it matters:* the Mumbai vs Ahmedabad polled-spot difference (GOLDPETAL vs GOLDTEN/GOLDGUINEA) is small, so **city basis cannot explain a premium of +79 to +94 bp** (G0 pooled).

## D. Practitioner education

- **Zerodha Varsity, gold parts 1 and 2** ([1](https://zerodha.com/varsity/chapter/gold-part-1/), [2](https://zerodha.com/varsity/chapter/gold-part-2/)).
  - Variant table, delivery intent rules, and the advice to trade only GOLD or GOLDM for liquidity (written in 2016, before GOLDPETAL and GOLDTEN became liquid).
  - On cross-variant arbitrage: "you will have to match the quantities", and different expiries complicate it.
  - CME vs MCX gaps reflect import costs, not arbitrage.
  - *Why it matters:* it frames the retail user's mental model.
- **Precious-metals expiry bulletins** (e.g. [Zerodha Dec 2025](https://zerodha.com/marketintel/bulletin/437006/mcx-precious-metals-expiry-december-2025), [FYERS Sep 2026](https://fyers.in/notice-board/precious-metals-gold-petal-gold-guinea-gold-ten-silver-100-gold-10g-ncom-expiry-30th-september-2026-staggered-delivery-contracts)).
  - Brokers force-close or block positions before staggered-delivery windows.
  - *Why it matters:* an **effective retail exit deadline that comes earlier than the exchange tender start**, which our calendar should show.

## E. Pain points

| # | Pain point | Evidence |
|---|---|---|
| 1 | Raw prices across variants aren't comparable (units, purity, expiry), so retail sees false bargains. | PS text; every competitor README; Varsity |
| 2 | Each variant settles to a *different* polled spot (city, single-day vs 3-day average) with *different* delivery forms and charges, and none of this is visible in trading apps. | 2025 and 2026 spec PDFs (06_data_sources); Dhan page shows "premium over spot" without a definition |
| 3 | Small-lot contracts carry a persistent premium that retail implicitly pays. | G0 (18 cycles): GOLDGUINEA +79 bp, GOLDPETAL +94 bp over GOLDTEN at the same settlement reference. Lost in full by anyone holding into settlement or delivery. |
| 4 | Settlement and close prices aren't fills; tender-period prints are thin and erratic. | PS text; our probe: GOLDGUINEA volume fell to 20 lots on expiry day and its close was +68 bp above its settlement reference |
| 5 | Backtests lean on assumed costs and a single crash. | gold-rv limitations 4, 6 and 7 |
| 6 | MCX data access is brittle: Akamai blocks scripts, endpoints changed, history is limited to 365 days per request in some endpoints. | Our probe; mcxlib caveats; goldparity "needs session handling" |
| 7 | Contract specs change silently between versions (tender days, margins, delivery form). | 2025 vs 2026 spec PDFs |

## F. Slide-claim verification status (rule: nothing goes on a slide unless it's ✅)

| Claim | Status | Primary source / action |
|---|---|---|
| Bullion share of MCX ADT 44% → 57% (Q2 FY26 vs Q2 FY25) | ✅ Verified | MCX Q2 FY26 results release (board approval 6 Nov 2025). State the quarter on the slide. |
| Q2 FY26 F&O ADT ₹4,11,270 Cr (+87%) | ✅ Verified | Same release |
| "MCX revenue +205%" | ⚠ Corrected: Q4 FY26 vs Q4 FY25 (₹889 Cr vs ₹291 Cr), not FY26 | Secondary (DSIJ, ScanX). Open MCX's Q4 FY26 results release before use. |
| Bullion ADT +496% in FY26 | ❌ Unverified, conflicts with ">4x" | Paywalled FOW only. Don't use. |
| Record bullion day ₹5,563 Cr (GOLDPETAL ₹2,486 Cr) | ❌ Unverified (X blocks fetch) | Replace with our own turnover from the bhavcopy `Value` field (₹ lakh, verified). |
| Gold peak about $5,600, crash on 31 Jan | ⚠ Corrected: COMEX front-month high $5,586 on 29 Jan 2026; −10.8% close-to-close on Fri 30 Jan | yfinance `GC=F` (exchange data via Yahoo). Use LBMA PM fix if quoting "spot". |
| Silver −31% in one day; MCX gold −4% from peak | ❌ Unverified | Secondary blogs only. Don't use. |
| CTT 0.01% sell side (non-agri futures) | ✅ Broker-confirmed | Zerodha charges page. A contract note is still preferred. |
| Import duty 15 → 6% (Jul 2024), 6 → 15% (May 2026) | 🔎 WGC pages seen in search, not opened | Open the WGC Goldhub notes before use. |
| SEBI 26 Feb 2026 circular (ETF valuation on polled spot) | 🔎 Secondary summaries | Open the SEBI circular before use. |
| GOLDTEN launch 1 Apr 2025 | 🔎 Multiple secondary sources, consistent with our data | Fine for context. The MCX circular is preferred. |
| Small-lot premium: GOLDGUINEA +79 bp [61, 97], GOLDPETAL +94 bp [80, 109] over GOLDTEN | ✅ G0 GO (18 cycles, 4 marks incl. VWAP, cycle-clustered CI) | g0_gate/G0_RESULTS.md. Say "Apr 2025 – Sep 2026, time-varying 34–145 bp". The old "+47 to +56 bp, decays into tender" is withdrawn. |
| Market size: premium on small-contract positions entering delivery, ₹10.3 Cr over the last 12 cycles (₹1.65 Cr held to settlement) | ✅ Our pipeline | g0_gate/G0_RESULTS.md, Follow-up 4. Cycle-mean premium used as a proxy. |
| Retail coin prices: Augmont 1 g ₹16,060, 8 g ₹1,26,167 (incl. GST) | ✅ Live product page, 13 Oct 2026 | One-day snapshot. MMTC-PAMP and Tanishq stay ❌ (snippet only). |
| Delivery cost per gram by route (GOLDTEN ₹15,198, GOLDGUINEA ₹15,315, GOLDPETAL ₹15,450) | ✅ Our pipeline | MCX polled spot 13 Oct + 3% GST + G0 premium (+ ₹100/g GOLDPETAL making charge). Vault, assay and transport not modelled. |
| "Commodity services market $3.87B → $8.16B" | ❌ Unverified | Don't use. Use our own market size instead. |
