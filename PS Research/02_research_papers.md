# 02 · Research Papers

The papers below are grouped by the question they help us answer. Each entry says what the paper finds, the method behind it and why it matters for PS03.

**Verification key**
- ✅ Opened or abstract-fetched during this session (13 Oct 2026).
- 🔎 Confirmed through search results only.
- 📚 Canonical paper whose details come from prior knowledge (the DOI or SSRN link is given, but it was not opened this session).

---

## 1. Why futures on the same metal differ: storage, carry and convenience yield

### Working (1949), "The Theory of Price of Storage" 📚
*American Economic Review* 39(6), 1254–1262.
- **Finding:** the spread between futures maturities is the price of storage. It equals financing plus storage costs, minus a convenience yield.
- **Why it matters:** this is the textbook basis for our carry adjustment. GOLDM expires around the 5th of the month and the others near month-end, so carry over that gap must be removed before any comparison.

### Kaldor (1939) and Brennan (1958), "The Supply of Storage" 📚
*Review of Economic Studies* 7(1); *American Economic Review* 48(1).
- **Finding:** convenience yield explains why inventories are held even when futures are in backwardation.
- **Why it matters:** gold's convenience yield is near zero, so its curve should sit close to full carry. A carry that drifts from interest rates is itself a signal.

### Fama & French (1987), "Commodity Futures Prices: Some Evidence on Forecast Power, Premiums, and the Theory of Storage" 📚
*Journal of Business* 60(1). [doi:10.1086/296385](https://doi.org/10.1086/296385)
- **Finding:** basis variation for **metals** is driven mostly by interest rates. Seasonal and inventory effects matter mainly for agricultural commodities.
- **Why it matters:** it supports deriving gold carry from the curve and cross-checking it against Indian money-market rates. gold-rv's median implied carry of 8.03% sits above typical T-bill rates, a gap worth explaining.

### Gibson & Schwartz (1990); Schwartz (1997), "The Stochastic Behavior of Commodity Prices" 🔎
*Journal of Finance* 52(3), 923–973. [Journal of Finance 52(3) issue page](https://afajof.org/issue/volume-52-issue-3/) · [schwartz97 R package](https://rdrr.io/cran/schwartz97/man/schwartz97package.html)
- **Model:** a two-factor model in which the spot price follows geometric Brownian motion and the convenience yield follows a mean-reverting (Ornstein–Uhlenbeck) process.
- **Why it matters:** this is the formal model behind term-structure decomposition. It's probably too heavy for the hackathon, but useful as a cited "future work" item.

---

## 2. Separating carry from genuine price moves

### Koijen, Moskowitz, Pedersen & Vrugt (2018), "Carry" ✅
*Journal of Financial Economics* 127(2), 197–225. [SSRN 2632697](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2632697)
- **Finding:** expected return splits into **carry**, which is model-free and observable in advance, and expected price appreciation. Carry predicts returns across asset classes, commodities included.
- **Why it matters:** this is the language for the PS's term "mechanical roll-down". Roll-down is the carry earned if the curve stays unchanged, and genuine curve change is the remainder.

### Szymanowska, de Roon, Nijman & van den Goorbergh (2014), "An Anatomy of Commodity Futures Risk Premia" ✅
*Journal of Finance* 69(1), 453–482. [SSRN 1343809](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1343809)
- **Finding:** futures returns split into **spot premia** (risk in the underlying) and **term premia** (changes in the basis). Spot premia run 5–14% a year and term premia 1–3% a year.
- **Why it matters:** it gives the academic justification for our P&L attribution, which separates the gold-price leg (spot premium) from the basis or spread leg (term premium). That separation is exactly what the PS asks for: strategy performance apart from the gold price.

### Gorton & Rouwenhorst (2006), "Facts and Fantasies about Commodity Futures"; Erb & Harvey (2006), "The Strategic and Tactical Value of Commodity Futures" 📚
*Financial Analysts Journal* 62(2). [doi:10.2469/faj.v62.n2.4083](https://doi.org/10.2469/faj.v62.n2.4083) · [doi:10.2469/faj.v62.n2.4084](https://doi.org/10.2469/faj.v62.n2.4084)
- **Finding:** roll yield and term structure explain much of commodity futures returns.
- **Why it matters:** background framing for the judges.

---

## 3. Delivery terms are part of the price (the angle most competitors miss)

### Gay & Manaster (1984), "The Quality Option Implicit in Futures Contracts" ✅
*Journal of Financial Economics* 13(3), 353–370. [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/0304405X84900047) · [RePEc](https://ideas.repec.org/a/eee/jfinec/v13y1984i3p353-370.html)
- **Finding:** when the short side can choose what to deliver, that choice has option value and lowers the futures price.
- **Why it matters:** MCX gold contracts differ in delivery form (1 kg or 100 g bars versus 8 g or 1 g bar/coin), in delivery centre, and in making charges (₹100/g on GOLDPETAL coins under the Dec 2024 circular). They also have staggered-delivery tender windows. Theory says embedded delivery terms *can* move a futures price. **For MCX gold the mechanism is not obvious, so treat it as a hypothesis.**
  - The making charge is paid by the buyer to the seller *at delivery*, on top of a DDR the futures price converges to anyway.
  - At about ₹14,800/g it is worth about 67 bp, which is suspiciously close to the measured GOLDPETAL premium.
  - That is a coincidence to test (stretch item S1), not a mechanism.
  - It belongs, without doubt, in the chooser's "take delivery" cost.

### Boyle (1989), "The Quality Option and Timing Option in Futures Contracts" ✅
*Journal of Finance*. [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1989.tb02406.x)
- **Finding:** the timing option, meaning the ability to deliver on any day within a window, has value.
- **Why it matters:** MCX's "staggered delivery tender period" lets either side give delivery intention on any of the last 3 trading days (5 days under the 2025 specs). That is a timing option, and it changed between spec versions.

### Chance & Hemler (1993), "The Impact of Delivery Options on Futures Prices: A Survey" ✅
*Journal of Futures Markets* 13(2). [Wiley](https://onlinelibrary.wiley.com/doi/abs/10.1002/fut.3990130203)
- **Why it matters:** a survey to cite. Basis behaviour near maturity depends on delivery options.

---

## 4. Indian gold futures: price discovery and efficiency

| Paper | Status | Finding | Relevance |
|---|---|---|---|
| "Price discovery in the Indian gold futures market" ([ResearchGate](https://www.researchgate.net/publication/225545912_Price_discovery_in_the_Indian_gold_futures_market)) | 🔎 | Vector error-correction models (VECM) on MCX data from 2003–2007. Futures prices of **both standard and mini** contracts lead spot. | The earliest evidence that the mini contract is part of price discovery. |
| "An empirical analysis of efficiency in the Indian gold futures market", *Macroeconomics and Finance in Emerging Market Economies* 12(3), 2019 ([T&F](https://www.tandfonline.com/doi/abs/10.1080/17520843.2019.1604556)) | 🔎 | Spot and futures are cointegrated, and price discovery happens in futures. | Supports treating MCX futures as the price-setting venue. |
| "Price discovery and volatility connectedness in Indian gold market: ETFs, spot and futures", *IJFMD* 10(1), 2024 ([Inderscience](https://www.inderscience.com/info/inarticle.php?artid=140652)) | 🔎 | Price-leadership shares show futures leading, with ETFs improving relative to spot. | Context: SEBI's Feb 2026 rule ties ETF valuation to exchange **polled spot**. |
| "Examining Price Discovery in the Gold market: Evidence from India", *Management Dynamics* 22(2) ([link](https://managementdynamics.researchcommons.org/journal/vol22/iss2/4/)) | 🔎 | Johansen cointegration and Granger causality show MCX futures lead. | Same conclusion. |

**Gap in the literature:** we found **no paper on cross-contract pricing between MCX gold contract sizes** (GOLD, GOLDM, GOLDTEN, GOLDGUINEA, GOLDPETAL). For E-mini versus standard contracts on COMEX, micro-contract settlements are *derived from* the standard contract's settlement, so they cannot diverge at settlement ([Optimus Futures](https://optimusfutures.com/blog/micro-gold-futures/)). MCX instead gives each contract its **own polled spot reference**. That design difference is a researchable novelty for us.

---

## 5. Relative value and its limits

### Gatev, Goetzmann & Rouwenhorst (2006), "Pairs Trading: Performance of a Relative-Value Arbitrage Rule" 📚
*Review of Financial Studies* 19(3). [doi:10.1093/rfs/hhj020](https://doi.org/10.1093/rfs/hhj020)
- **Finding:** the canonical distance-based pairs rule. Its excess returns decline over time.
- **Why it matters:** our pairs are *mechanically linked* (the same metal and the same settlement formula), so they are far stronger than statistical pairs.

### Avellaneda & Lee (2010), "Statistical Arbitrage in the U.S. Equities Market" 📚
*Quantitative Finance* 10(7). [doi:10.1080/14697680903124632](https://doi.org/10.1080/14697680903124632)
- **Method:** model the residual as an Ornstein–Uhlenbeck process and trade on its standardised "s-score". Its mean-reversion speed implies a half-life.
- **Why it matters:** our entry rule should require that the expected reversion time is shorter than the days left before the tender period.

### Shleifer & Vishny (1997), "The Limits of Arbitrage" 📚
*Journal of Finance* 52(1). [doi:10.1111/j.1540-6261.1997.tb03807.x](https://doi.org/10.1111/j.1540-6261.1997.tb03807.x)
- **Finding:** mispricings persist when arbitrage is capital-intensive and risky.
- **Why it matters:** this is a *candidate* explanation for **the premium of GOLDGUINEA and GOLDPETAL over GOLDTEN we measured: pooled +79 bp (GOLDGUINEA) and +94 bp (GOLDPETAL) across 18 cycles, passing G0 on all four marks including VWAP**. All three settle to the same per-gram reference price, yet the gap persists in traded prices right up to expiry and is extinguished only by the final settlement. Closing it requires holding a short in small retail lots *through* settlement, i.e. compulsory delivery of 8 g or 1 g coins and bars, under 8.34% extra tender-period margin. The flat pre-tender profile is exactly what limits to arbitrage predicts.

---

## 6. Backtest rigour

### Bailey & López de Prado (2014), "The Deflated Sharpe Ratio" ✅
*Journal of Portfolio Management* 40(5), 94–107. [SSRN 2460551](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551) · [PDF](https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf)
- **Finding:** the Deflated Sharpe Ratio corrects for selection bias across N trials and for non-normal returns.
- **Why it matters:** we will report the trial count honestly.

### Bailey, Borwein, López de Prado & Zhu (2017), "The Probability of Backtest Overfitting" 📚
*Journal of Computational Finance* 20(4). [SSRN 2326253](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253)
- **Method:** estimate the probability of backtest overfitting (PBO) with combinatorially symmetric cross-validation (CSCV).

### Harvey, Liu & Zhu (2016), "…and the Cross-Section of Expected Returns" 📚
*Review of Financial Studies* 29(1). [doi:10.1093/rfs/hhv059](https://doi.org/10.1093/rfs/hhv059)
- **Finding:** after multiple testing, a t-statistic above 3 should be the bar.
- **Why it matters:** gold-rv's t = 1.89 falls well short of it.

### Fonseca (2026), "Look-Ahead-Freedom as Temporal Non-Interference" ✅
[arXiv 2607.04958](https://arxiv.org/abs/2607.04958)
- **Finding:** look-ahead bias is formalised as temporal non-interference over a time-indexed information lattice. It is decidable in linear time for value-independent pipelines (windowing, resampling, joins, point-in-time reads). Empirical detectors "certify nothing by their silence".
- **Why it matters:** this is the citation for our **truncation-invariance test**. Signals computed on data cut at day *t* must equal the full-data signals at *t*.

### "What survives honest evaluation? Leakage-safe, search-aware assessment of LLM-driven trading strategy discovery" 🔎
[arXiv 2608.27734](https://arxiv.org/pdf/2608.27734)
- **Why it matters:** recent support for counting every trial, LLM-proposed ones included.

---

## 7. Measuring trading costs from daily OHLC (since we have no order book)

### Roll (1984), "A Simple Implicit Measure of the Effective Bid-Ask Spread" 📚
*Journal of Finance* 39(4). [doi:10.1111/j.1540-6261.1984.tb03897.x](https://doi.org/10.1111/j.1540-6261.1984.tb03897.x)

### Corwin & Schultz (2012), "A Simple Way to Estimate Bid-Ask Spreads from Daily High and Low Prices" 📚
*Journal of Finance* 67(2). [doi:10.1111/j.1540-6261.2012.01729.x](https://doi.org/10.1111/j.1540-6261.2012.01729.x)

### Abdi & Ranaldo (2017), "A Simple Estimation of Bid-Ask Spreads from Daily Close, High, and Low Prices" ✅
*Review of Financial Studies* 30(12), 4437–4480. [EconPapers](https://econpapers.repec.org/article/ouprfinst/v_3a30_3ay_3a2017_3ai_3a12_3ap_3a4437-4480..htm)

### Ardia, Guidotti & Kroencke (2024), "Efficient Estimation of Bid-Ask Spreads from Open, High, Low, and Close Prices" (EDGE) ✅
*Journal of Financial Economics*. [PDF](https://acfr.aut.ac.nz/__data/assets/pdf_file/0016/570202/Efficient_Estimation_of_Bid_Ask_Spreads_from_OHLC_Prices-39.pdf) · code: `bidask`
- **Why it matters (all four):** gold-rv's verdict depends on an *assumed* 5 bp per order slippage against a 3.8 bp break-even. Estimating spreads per contract per day from bhavcopy OHLC replaces that assumption with a measurement.
- **Caveat:** the bhavcopy "Close" may be a last-traded or settlement value rather than a quote midpoint, and the estimators assume continuous trading. We report ranges, not single numbers.

---

## 8. Volatility, foundation models and LLMs: relevance check

| Paper | Status | Finding | Relevance to PS03 |
|---|---|---|---|
| Corsi (2009), HAR-RV, *Journal of Financial Econometrics* 7(2) [doi:10.1093/jjfinec/nbp001](https://doi.org/10.1093/jjfinec/nbp001) | 📚 | A simple HAR model is a hard-to-beat volatility benchmark. | Use for **risk sizing** of spread positions only. |
| Brini (2026), "Forecasting Realized Volatility with Time Series Foundation Models" [arXiv 2607.05291](https://arxiv.org/abs/2607.05291) | ✅ | 9 zero-shot TSFMs vs HAR across 50 assets. "Econometric benchmarks remain competitive"; only TTM wins, narrowly. | Strong reason **not** to spend hackathon time on foundation models. |
| "The Promise of Time-Series Foundation Models for Agricultural Forecasting" [arXiv 2601.06371](https://arxiv.org/abs/2601.06371) | ✅ | 17 approaches on USDA prices from 1997–2025. | Agricultural commodities only; low relevance. |
| Dai et al. (2026), "Beyond Polarity: Multi-Dimensional LLM Sentiment Signals for WTI" [arXiv 2603.11408](https://arxiv.org/abs/2603.11408) | ✅ | GPT-4o + FinBERT combined works best. **Intensity and uncertainty** beat polarity. | News moves *all* gold contracts together, so it is weak for cross-contract relative value. Possible use: explaining gold-wide volatility days. |
| Ghali et al. (2025), "Forecasting Commodity Price Shocks Using … Agentic Generative AI Extracted Economic News" [arXiv 2508.06497](https://arxiv.org/abs/2508.06497) | ✅ | Dual-stream LSTM + agentic news, AUC 0.94 on annual shock detection (1960–2023). | Macro horizon; not our problem. |
| "Not All News Is Equal: … Finetuned LLMs for Aluminum Price Forecasting" [arXiv 2603.09085](https://arxiv.org/pdf/2603.09085) | 🔎 | Fine-tuned Qwen3 sentiment improves LSTM Sharpe (1.04 vs 0.23) in high-volatility periods. | Same caveat. |
| Surveys: "LLM-based Agents for Forecasting" [2608.23058](https://arxiv.org/pdf/2608.23058); "LLMs in Financial Investments" [2507.01990](https://arxiv.org/pdf/2507.01990) | 🔎 | Landscape. | Background only. |

**Takeaway:** the literature points away from ML or LLM forecasting of gold *direction*. The defensible contribution is **microstructure and contract-design analysis**: delivery terms, settlement references, limits to arbitrage and measured costs. LLMs belong in the *explanation* layer, turning computed decompositions into plain language, and never in the signal.
