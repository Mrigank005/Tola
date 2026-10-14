# PS03 · Commodity Derivatives Intelligence: Research Index

**Hackathon:** Hack in Hills '26, Round 2 (prototype due **31 Oct 2026**); finale 20 Nov 2026, Manali
**Problem:** MCX gold futures in several sizes (GOLDM, GOLDTEN, GOLDGUINEA, GOLDPETAL). Build a defensible analytical product that explains and measures the relative pricing differences between them.
**Research date:** 13 Oct 2026 (revised twice the same day after review) · **Status:** scope **approved**. **G0 verdict: GO on both pairs**, and the **settlement-reference check passed** (GOLDTEN = GOLDGUINEA per gram in 18/18 cycles; 999/995 applied in every spec version). See [g0_gate/G0_RESULTS.md](g0_gate/G0_RESULTS.md). The deck is in progress.

## Contents

| File | What's inside |
|---|---|
| [01_github_repos.md](01_github_repos.md) | 11 competitor PS03 repos (feature by feature), MCX data libraries, backtest, stats and UI repos with stars, licence, activity and reuse verdict |
| [02_research_papers.md](02_research_papers.md) | Storage and carry theory, delivery options, Indian gold price discovery, limits to arbitrage, backtest rigour, OHLC spread estimators, ML/LLM relevance check |
| [03_patents.md](03_patents.md) | 11 **US** patents (CME ratio spreads for mixed contract sizes, calendar spreads, basis futures, stat-arb, alerts, strategy scoring) and IP takeaways. Indian filings were not searched. |
| [04_market_landscape.md](04_market_landscape.md) | Bloomberg, LSEG, Kpler, Vortexa, ChAI, Gro (failed), Indian retail tools and data vendors, competitor matrix, exploitable gaps |
| [05_articles_reports.md](05_articles_reports.md) | MCX bullion boom, SEBI 2026 changes, gold crash, import duty swings, pain points, **slide-claim verification table (§F)** |
| [06_data_sources.md](06_data_sources.md) | **Verified MCX endpoints** (bhavcopy, per-contract range, polled spot archive), field gotchas, versioned contract mechanics, other free and paid sources, data plan |
| [07_sources.md](07_sources.md) | Bibliography of 169 sources with URLs and how each was verified |
| [g0_gate/](g0_gate/) | G0 pre-registration (frozen before the run), fetch and analysis scripts, raw cache, results |
| [research_summary.html](research_summary.html) | Visual summary and **proposed scope with the G0 gate** (open in a browser) |
| [data_probe/](data_probe/) | Real data pulled during research: 9 Oct 2026 gold bhavcopy, Aug–Sep 2026 same-expiry convergence, Sep 2026 polled spot |

## Key takeaways

1. **The field is crowded.** At least 11 public Hack in Hills PS03 repos appeared between 1 and 8 Oct. The standard pipeline (normalize → carry-adjust → z-score → walk-forward → costs → "no edge" verdict) is now **table stakes**. gold-rv already does it well on three years of real data, with an honest verdict and a pitch deck. Carry adjustment alone is no longer a differentiator.
2. **Every contract settles to its own exchange-polled spot price, and nobody uses that data.** Per the 2026 specs:
   - GOLDTEN and GOLDGUINEA settle to Ahmedabad 995 spot × 999/995 (single poll).
   - GOLDPETAL settles to **Mumbai** spot.
   - GOLD and GOLDM settle to a **3-day average**.

   MCX publishes these polled spots per contract (`GetSpotMarketArchive`, verified). On 30 Sep 2026 the GOLDTEN and GOLDGUINEA references were both exactly ₹14,820.6/g.
3. **A small-lot premium appears in the data, but it is a lead, not yet a result.**
   - **G0 passed (GO on both pairs)** across all **18 same-expiry cycles** (Apr 2025 – Sep 2026), on all four marks including VWAP.
   - **Pooled premium over GOLDTEN: GOLDGUINEA +79 bp [61, 97], GOLDPETAL +94 bp [80, 109]** (VWAP, cycle-clustered 95% CI). Every cycle is positive. Cycle means range 34–145 bp, peaking in the Mar–Jun 2026 cycles.
   - **It does not decay before delivery.** It is still about +76 bp (GOLDGUINEA) and +91 bp (GOLDPETAL) 5–9 trading days out. Only the final settlement price, the same per gram for all three, extinguishes it. The two-cycle "decay" was specific to those cycles and is withdrawn.
   - **In rupees:** at about ₹14,800/g that is about ₹117–139/g, or **about ₹1,170–1,390 per 10 g**, *lost if held into final settlement or delivery*. A holder who exits before the tender window gets most of it back. Their cost is the *change* in premium, about 6–11 bp on average, but large when the premium regime shifts. The chooser must model holding horizon.
   - The superseded two-cycle probe figure was +47 to +56 bp.
   - **Who pays (reframe):**
     - *Traders* exit before tender, and brokers force it, so they pay only about ₹9–16/g on average.
     - *Delivery-takers* pay it in full, yet GOLDPETAL delivery (about ₹15,450/g incl. GST and making charge) is still about ₹610/g cheaper than a retail 1 g coin (₹16,060).
     - So the premium looks like the market price of small-denomination physical gold, not an overcharge.
     - Headline: *"Small MCX gold contracts trade 80–95 bp rich to an identical settlement price, in every cycle for 18 months. Here's who pays it, and when it's worth paying."*
   - It is only two cycles, measured on a `Close` field of uncertain meaning. **It must pass the G0 gate before it headlines anything.**
4. **Contract specs change between versions.**
   - The tender window went from **5 to 3** trading days, and tender margin from **5% to 8.34%**.
   - GOLDPETAL delivery changed from a "1 g coin" to a "1 g bar/coin".
   - A **₹100/g making charge** on GOLDPETAL delivery arrived (Dec 2024 circular). It is paid buyer → seller at delivery, on top of the DDR. That is about 67 bp at today's price, suspiciously close to the GOLDPETAL premium, **but the price mechanism is not obvious, so it stays a hypothesis (S1)**. It certainly belongs in the chooser's "take delivery" cost.
5. **Costs are assumed everywhere.**
   - Competitors plug in 2–5 bp of slippage, and gold-rv's own break-even is 3.8 bp.
   - OHLC spread estimators (Abdi–Ranaldo 2017; EDGE 2024 via `bidask`) let us **measure** slippage instead.
   - Broker charges confirm CTT at 0.01% sell side. Brokerage is **0.03% or ₹20 per order, whichever is lower**, so small single-lot orders cost about 3 bp each.
6. **MCX data is reachable, but only the right way.**
   - Plain HTTP requests get Akamai 403s, and the `mcxlib` endpoints are stale.
   - `curl_cffi` (Chrome TLS impersonation) plus the new `GET` endpoints work, including a **per-contract full-history call**. A complete backfill takes about 400 calls.
7. **ML and LLM forecasting is off-problem.** LLMs fit only as an explanation layer over computed numbers.
8. **The users nobody serves:**
   - **Retail** choosing which gold contract to hold. Bullion's share of MCX ADT rose from 44% to 57% (Q2 FY26 vs Q2 FY25, per MCX's release).
   - **Exchange and regulator** monitoring contract fairness.
9. **No US-filing IP blockers found.** The closest patent, CME's ratio spreads for mixed sizes (active to 2030), covers exchange matching; we don't match orders. Indian filings were not searched.
10. **Several headline stats were wrong or unverified in secondary sources.**
    - The "205%" is Q4 FY26 revenue growth, not FY26.
    - The gold peak was $5,586 on 29 Jan 2026 (COMEX front month), not "$5,600 on 28 Jan".
    - The crash day was Fri 30 Jan, not Sat 31 Jan.
    - The record-turnover tweet couldn't be opened.

    See §F of 05 before anything goes on a slide.
11. **Time is the main risk.** There are 18 days to Round 2, plus the deck, video and docs. The MVP has been cut (below).

## Proposed scope (summary; full version in `research_summary.html §5`)

**Working name: Tola**, the fair-price desk for MCX gold. (A tola is the traditional Indian gold weight, 11.66 g.)

### G0: premium gate (go/no-go, decide by **Fri 16 Oct**)

The full rule is frozen in [g0_gate/G0_PREREGISTRATION.md](g0_gate/G0_PREREGISTRATION.md) and was written before the backfill ran. In summary:

1. **Backfill** every same-expiry GOLDTEN / GOLDGUINEA / GOLDPETAL cycle from Apr 2025 to Sep 2026 (about 18 cycles), plus GOLDGUINEA vs GOLDPETAL back to 2020 as context.
2. **Four marks:**
   - `Close`, `Open` and (H+L)/2;
   - **VWAP = Value × 10⁵ ÷ (Volume × lot grams)**. `Value` is ₹ lakh, verified on real rows. VWAP doesn't depend on last-trade timing, so it directly tests the Close artefact.
   - Polled-spot basis was dropped as a mark: GOLDTEN and GOLDGUINEA share the Ahmedabad poll, so it cancels. It remains a GOLDPETAL-only diagnostic in M2.
3. **Eligible days:** not in the last 5 trading days, traded on both legs, and both legs ≥ ₹1 Cr turnover. A cycle survives with ≥10 eligible days.
4. **Statistics:** a cluster bootstrap that resamples whole cycles, 10,000 reps. Pooled mean = mean of cycle means.

| Outcome (per pair) | Criteria | Then |
|---|---|---|
| **GO** | ≥8 surviving cycles **and**, on every mark, pooled ≥ +15 bp, cluster-bootstrap CI above 0, and cycle hit rate ≥75% | The premium is the headline: "who pays, how much, when it closes" (passing pairs only). |
| **PARTIAL** | Fewer than 8 surviving cycles (**whatever the CI says**), or not GO but the VWAP and Close CIs are both above 0 | One finding inside the decomposition. Not the headline. |
| **NO-GO** | Anything else | **Agreed fallback:** "Tola, contract-fairness desk". This is the decomposition plus each contract's basis to its own settlement price, plus the chooser. Headline: "we tested the apparent small-lot premium against four price marks and it doesn't hold". |

### MVP (by 31 Oct)

- **M1: data layer.**
  - Chrome-TLS fetcher, contract-wise backfill, polled spot, versioned spec YAML, validation guards.
  - **A committed Parquet snapshot plus a one-command manual refresh script.** The GitHub Actions cron is optional and only if time permits.
- **M2: Basis Anatomy.** Per contract per day, with basis to its own polled spot.
- **M3: same-reference convergence monitor.**
  - GOLDTEN / GOLDGUINEA / GOLDPETAL.
  - GOLD vs GOLDM as a control pair **only on the near even-month contract** (GOLD lists Feb/Apr/Jun/Aug/Oct/Dec only, so about 6 usable cycles a year). On 9 Oct the shared Dec contract was at −2.6 bp; the far shared months barely trade.
- **M4: walk-forward verdict.** Models the **delivery leg explicitly**: short the small contract into settlement, deliver coins, including coin sourcing cost, 8.34% tender margin, vault and assaying. Expected result: "not capturable without delivery capability". A pre-tender mean-reversion rule is kept as the null. Also measured costs, P&L split, Deflated Sharpe, with and without the crash, truncation test.
- **M5: trader-facing layer. The chooser is the product core:** holding period and take-delivery decide the cost.
  - "Which contract?" **chooser**, with quantity as an input. The **broker is a parameter**; the default preset is labelled "Zerodha rates" (0.03% or ₹20 per order). It includes a "take delivery" cost line (making charge, delivery margin).
  - **In-app alert log**, quiet by default. Replaces Telegram.
  - Contract calendar.

### Stretch (finale, 20 Nov)

- S1: spec-change annotator (tests the making-charge and regime-break hypothesis).
- S2: silver family.
- S3: LLM explainer.
- S4: history back to 2011.
- S5: exchange fairness index.
- S6: **daily cron + Telegram alerts + about 5-week live track record**.

### Decisions (13 Oct 2026)

| Item | Call |
|---|---|
| Framing | **Approved:** fair-price desk with a retail chooser |
| G0 criteria and fallback | **Approved**, with the VWAP swap, cycle-clustered bootstrap and ≥8-cycle minimum |
| Primary user | **Approved:** retail and HNI gold traders |
| MVP cut line | **Approved** as revised |
| Name | **Approved: Tola**, pending a brand check. Quick web check (13 Oct): no Indian gold or fintech product named Tola found. There is an unrelated US B2B payments startup ("Tola", YC 2022) and a US VC (Tola Capital). "Tola" is a generic Indian gold-weight term, so it would be weak to register for gold services. Fine for the hackathon; use a distinctive compound mark and a formal IP India search if this is ever commercialised. |

**Next:** run G0, then start the deck on `ppt_template.pptx` with the headline G0 decides.
