# 03 · Patents

Every patent below was checked on its Google Patents page on 13 Oct 2026 for title, assignee, dates and legal status. One search-engine summary turned out to be wrong: US20050086152A1 is *not* about ratio spreads, so all statuses below come from the patent pages themselves. **This is research context, not legal advice.**

---

## Most relevant

### US8255305B2: "Ratio spreads for contracts of different sizes in implied market trading"
- **Assignee / inventor:** CME Group Inc. (orig. Chicago Mercantile Exchange); inventor Andrew Milne
- **Dates:** priority 15 Sep 2009 · granted 28 Aug 2012
- **Status:** **Active**, expires 9 Sep 2030
- **Link:** [patents.google.com/patent/US8255305](https://patents.google.com/patent/US8255305) · family: [US20110066536A1](https://patents.google.com/patent/US20110066536A1/en), [US8793180B2](https://patents.google.com/patent/US8793180), [US20120271755A1](https://patents.google.com/patent/US20120271755A1/en)

**What it covers.** An exchange matching engine generates *implied orders* where one leg is a ratio spread linking a **mini contract and a full-size contract on the same product**. It assigns "lot points", with the full-size contract's points set to the least common multiple of the minis' points. Many small orders can then match one big order.

**Why it matters to us.** It is the closest IP to our problem: same underlying, different sizes. It shows that CME treats cross-size linkage as a **liquidity-plumbing problem the exchange solves inside its matching engine**. MCX has no equivalent implied ratio-spread book between GOLDM, GOLDTEN, GOLDGUINEA and GOLDPETAL, which is one structural reason the gaps can persist. Our product does no order matching, so it does not practise this patent. The *idea* that an exchange-level implied ratio spread would compress the small-lot premium is a good line for the pitch's impact slide.

### US8639601B2: "Calendar spread futures"
- **Assignee / inventors:** CME Group Inc.; Eugene Mueller, Daniel Grombacher, Frederick Sturm
- **Dates:** filed 1 Jun 2010 · granted 28 Jan 2014
- **Status:** **Active**, expires 9 Jun 2031
- **Link:** [patents.google.com/patent/US8639601](https://patents.google.com/patent/US8639601)

**What it covers.** Calendar spreads listed as **stand-alone, cash-settled instruments**, so traders can lock in inter-month spreads without the roll period.

**Why it matters to us.** It confirms that inter-expiry spread risk, the GOLDM 5th-of-month versus month-end mismatch, is valuable enough to productise. We only *measure* it.

### US20110295734A1: "System and Method for Implementing and Managing Basis Futures"
- **Assignee / inventors:** CME Group Inc.; Richard Co, Brett Vietmeier, John Labuszewski
- **Dates:** filed 30 Jun 2010
- **Status:** **Abandoned** after a Board of Appeals decision on 7 Dec 2019
- **Link:** [patents.google.com/patent/US20110295734A1](https://patents.google.com/patent/US20110295734A1/en)

**What it covers.** Futures quoted as the *difference between spot and futures* (the basis), matched and cleared together with the outright.

**Why it matters to us.** "Basis to spot" is our core measurement, using MCX's own polled spot per contract. The application is abandoned and we don't trade, so there is no conflict. It is good evidence that basis-centric views are an institutional need.

---

## Statistical arbitrage and analytics

### US20140244474A1: "Automated trading system and methodology for realtime identification of statistical arbitrage market opportunities"
- **Applicant / inventor:** Remington John Sutton (individual)
- **Dates:** filed 5 May 2014 · published 28 Aug 2014
- **Status:** **Abandoned** (no response to office action, Sep 2015)
- **Link:** [link](https://patents.google.com/patent/US20140244474A1/en)

**What it covers.** Bid/ask ratio indicators between correlated instruments, with z-score entry and mean-reversion exit.

**Why it matters to us.** Z-score pairs logic is old, public and unprotected. We should **not claim novelty** for z-scores or rolling bands, and neither can any competitor.

### US20160350855A1: "Commodities Trading Platform"
- **Applicant / inventor:** Julie A. Lerner (individual)
- **Dates:** filed 1 Jun 2016
- **Status:** **Abandoned**
- **Link:** [link](https://patents.google.com/patent/US20160350855A1/en)

**What it covers.** Metadata-driven detection of spread disparities across commodity, transport and futures markets, with conditional execution.

### US8612332B1: "Valuing futures contracts"
- **Assignee / inventors:** Teucrium Trading LLC; Sal Gilbertie, Barbara Riker, Dale Riker, Kelly Teevan
- **Dates:** filed 1 Dec 2011 · granted 17 Dec 2013
- **Status:** **Active**, expires around 1 Dec 2031
- **Link:** [link](https://patents.google.com/patent/US8612332B1/en)

**What it covers.** When a futures contract is "locked" at its daily price limit, its value is synthesised from options (call price + strike) instead of the frozen settlement.

**Why it matters to us.** It is an analogue of the PS warning that **settlement prices are not executable**. Our thin-day and limit-day guards (MCX gold has 3% daily limits that expand) address a similar concern without using options.

### US20050086152A1: "System and method for providing futures contracts in a financial market environment"
- **Assignee / inventor:** BGC Partners (orig. eSpeed); Michael Sweeting
- **Dates:** filed 20 Oct 2003
- **Status:** Active, adjusted expiry 8 Jan 2029
- **Link:** [link](https://patents.google.com/patent/US20050086152)

**What it covers.** Multi-asset deliverable baskets designed to prevent delivery squeezes.

**Why it matters to us.** Tangential. Delivery squeezes in thin tender periods are a real risk in small-lot gold, which supports our "never hold into tender" rule.

---

## Alerts, scoring and backtest evaluation

### US20200273104A1: "Advanced financial alerts generation based on automatic analysis of price charts"
- **Assignee / inventors:** TrendSpider LLC; Daniel L. Ushman, Ruslan Lagutin
- **Dates:** filed 20 Feb 2020
- **Status:** **Granted, active**
- **Link:** [link](https://patents.google.com/patent/US20200273104A1/en)

**What it covers.** Alerts on chart behaviours ("touch", "bounce", "break through") with sensitivity zones.

**Why it matters to us.** Our alerts are **gated on economics**: the residual must exceed measured cost plus a buffer, with liquidity and calendar gates. They are not chart-pattern triggers, so we stay clear of these claims. Avoid describing our feature as "chart-pattern alerts".

### US12271950B2: "Scoring and recommendation system, method and program product for quantitative trading strategies"
- **Inventor:** Francesco Parrella (individual)
- **Dates:** filed 5 Sep 2024 · granted 8 Apr 2025
- **Status:** **Active**
- **Link:** [link](https://patents.google.com/patent/US12271950B2/en)

**What it covers.** Combined normalised scoring of strategies across in-sample/out-of-sample tests, parameter sensitivity (overfitting), costs and execution delays, producing recommendations.

**Why it matters to us.** This is the closest active patent to a "backtest lab". Our use is a non-commercial, academic hackathon prototype built on published methods (Deflated Sharpe Ratio, PBO, bootstrap). Still, **don't market a single composite "strategy score" with recommendations**. Report the standard statistics separately.

### Exchange matching infrastructure (context only)
[US8165951B2](https://patents.google.com/patent/US8165951) / [US7260554B2](https://patents.google.com/patent/US7260554) "Implied market trading system", [US11042935B2](https://patents.google.com/patent/US11042935) "Spread price scaling for implied trade matching", all CME.

**Why it matters to us.** Exchange-side; we do not match orders, so no overlap.

---

## IP takeaways for our build

**Scope of this search:** US filings and applications on Google Patents only. Indian (IP India / InPASS), EPO and WIPO filings were not searched, so "no blockers" below means **no US-filing blockers found**.

1. **Nothing we plan is novel in the patent sense, and that's fine.** Normalisation, carry adjustment, z-scores, OU half-lives and walk-forward testing are textbook prior art. Judges score rigour and insight, not IP.
2. **Avoid three framings:**
   - "automated execution" (we analyse; we don't trade);
   - "chart-pattern alerts";
   - a single proprietary "strategy score" with recommendations.
3. **The genuinely new contribution is empirical, not a method.** Measuring each contract against its *own exchange-polled settlement reference*, and decomposing the gap into contract-design components, is analysis of public data. It is publishable as insight, and patents don't apply to findings.
4. **Gaps in this search:**
   - Indian patents (InPASS / IP India) were **not searched**. The portal needs an interactive session.
   - We found no patent on cross-size gold contract analytics specifically.
   - If the team ever commercialises, a professional freedom-to-operate search is required.
