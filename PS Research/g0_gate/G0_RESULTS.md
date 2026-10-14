# G0 · Small-Lot Premium Gate: Results

**Run:** 13 Oct 2026 · **Rule:** [G0_PREREGISTRATION.md](G0_PREREGISTRATION.md), frozen before the run and applied unchanged by [analyze_g0.py](analyze_g0.py) · **Data:** 260 MCX calls + 1 re-fetch. That covers 180 contract histories (GOLDTEN since Apr 2025; GOLDGUINEA and GOLDPETAL since Jan 2020), cached in `raw/`.

## Verdict: **GO**, on both pairs

| Pair | Surviving cycles | Close | Open | Mid (H+L)/2 | **VWAP** | Hit rate | Verdict |
|---|---|---|---|---|---|---|---|
| GOLDGUINEA − GOLDTEN | 18 / 18 | +78.9 bp [61.6, 98.0] | +81.8 [65.6, 99.3] | +78.7 [60.6, 97.4] | **+78.7 [61.0, 97.4]** | 100% on every mark | **GO** |
| GOLDPETAL − GOLDTEN | 18 / 18 | +94.6 [80.6, 109.8] | +92.9 [80.3, 106.5] | +93.2 [79.5, 107.8] | **+94.1 [80.4, 108.8]** | 100% on every mark | **GO** |

Pooled = mean of 18 cycle means. Brackets are the 95% cluster-bootstrap CI (whole cycles resampled, 10,000 reps). Eligible days: 1,407 (GOLDGUINEA) and 1,482 (GOLDPETAL).

Every GO condition holds with room to spare:
- **Cycles:** 18 survive, against a minimum of 8.
- **Size:** the lowest CI bound on any mark is +60.6 bp, against a 15 bp bar.
- **Consistency:** every cycle has a positive mean on every mark.
- **Close-timing artefact ruled out:** VWAP, which ignores when the last trade happened, agrees with Close to within 1 bp.

## Sensitivity (reported, not decisive)

| Variant | GOLDGUINEA−GOLDTEN VWAP (CI) | GOLDPETAL−GOLDTEN VWAP (CI) |
|---|---|---|
| Pre-registered (₹1 Cr floor, 5-day exclusion) | +78.7 (61.0, 97.4) | +94.1 (80.4, 108.8) |
| ₹0.25 Cr floor | +79.4 (61.9, 98.1) | +94.0 (80.9, 108.4) |
| ₹5 Cr floor | +76.7 (58.3, 97.1) | +93.7 (78.3, 110.5) |
| 3-day tender exclusion | +78.9 (61.4, 97.6) | +94.4 (80.9, 109.1) |
| Excluding Jan–Mar 2026 cycles (crash), 15 cycles | +69.4 (52.3, 89.0) | +88.4 (74.3, 104.8) |

## What the full sample changes vs the two-cycle probe

1. **The premium is larger and varies over time.**
   - The probe's +47 to +56 bp came from the two most recent cycles, which had already cooled. Across all 18 cycles the pooled premium is **+79 bp (GOLDGUINEA) and +94 bp (GOLDPETAL)**.
   - **Cycle means range from 34 to 145 bp.** They rose from about 35–55 bp (mid-2025) to a peak of about **140–148 bp in the Mar–Jun 2026 cycles**, then fell back to about 49–60 bp by Sep 2026.
2. **There is no systematic decay before delivery.** The probe's "decays toward tender" was specific to those two cycles. Pooled by days to expiry (VWAP):

   | Trading days to expiry | 60+ | 40–59 | 20–39 | 10–19 | 5–9 |
   |---|---|---|---|---|---|
   | GOLDGUINEA − GOLDTEN | +87 | +78 | +69 | +68 | +76 |
   | GOLDPETAL − GOLDTEN | +97 | +96 | +88 | +85 | +91 |

   Inside the excluded last 5 days, traded prices *still* carry about +65 to +110 bp even on expiry day, though volume collapses (median GOLDGUINEA volume falls from about 7,000 lots to about 35). **The premium is extinguished only by the final settlement price**, which is the same per gram for all three contracts. It does not converge in traded prices.
3. **Consequence for retail: the cost depends on how long you hold, not on when you buy.**
   - **Exit before the tender window:** you sell at roughly the same premium you bought at, so the realised cost is the *change* in premium over your holding period. Entering 60+ trading days out and exiting 5–9 days out gave up about 11 bp (GOLDGUINEA) and 6 bp (GOLDPETAL) on average. It can be far larger when the premium regime shifts. For example, anyone long the small contracts while the premium fell from about 140 bp (Jun 2026 cycle) to about 50 bp (Sep 2026 cycle) lost that difference.
   - **Hold into final settlement or delivery:** the full premium is marked away at settlement. At about ₹14,800/g that is **₹117/g (GOLDGUINEA) to ₹139/g (GOLDPETAL), about ₹1,170–1,390 per 10 g** at the pooled averages. GOLDPETAL deliveries also carry the ₹100/g making charge.

   **The chooser must model holding horizon.** "₹X paid at entry" is only the right number for someone who holds to expiry.
4. **This also explains why the gap can persist.** Capturing it needs a position held *through* settlement: short GOLDGUINEA or GOLDPETAL, long GOLDTEN. That forces compulsory delivery of 8 g or 1 g coins and bars by the short, under 8.34% extra tender-period margin. This is classic limits to arbitrage. M4 should test whether any pre-tender version of the trade survives costs. Given the flat decay profile, expect little.

## Context: the GOLDPETAL regime break (not part of the decision)

GOLDPETAL − GOLDGUINEA, VWAP, by cycle (81 surviving cycles since 2020; yearly means 2020 −35, 2021 −68, 2022 −47, 2023 −110, **2024 −213**, 2025 −5, 2026 +6 bp):

| Expiry | 2024-06 | 2024-09 | 2024-10 | 2024-11 | **2024-12** | 2025-01 | 2025-02 | 2025-03 | **2025-04** | 2025-05 → 08 |
|---|---|---|---|---|---|---|---|---|---|---|
| bp | −224 | −246 | −256 | −188 | **−114** | −84 | −101 | −50 | **−3** | +29 to +35 |

- **Confirmed:** gold-rv's break is real. GOLDPETAL went from about 2.5% cheaper than GOLDGUINEA to slightly richer, over the **Nov 2024 → Apr 2025** cycles. The Apr 2025 contract, the first launched under the 31 Dec 2024 circular (₹100/g making charge), is where it reached about 0.
- **Not confirmed:** the cause.
  - The timing fits a contract-terms change.
  - The *sign* is awkward for the making-charge story. A new buyer-paid charge should make long GOLDPETAL less attractive, not richer.
  - Earlier GOLDPETAL contracts may have had worse delivery or settlement terms. That needs the pre-2025 GOLDPETAL spec PDFs.
  - **This stays an S1 hypothesis.**

## Caveats
- **Sample.** 18 cycles from one 18-month regime that includes a historic gold crash and an import-duty hike (May 2026). The premium is time-varying, so treat the pooled mean as a description of that period, not a constant.
- **Settlement not measured.** We didn't pull DDR / polled spot for every cycle. "Extinguished at settlement" rests on the spec text and the one Sep 2026 cycle we checked (GOLDTEN and GOLDGUINEA reference both ₹14,820.6/g). Pulling DDR for all 18 cycles is a cheap M2 task and the obvious next check.
- **Eligibility.** The ₹1 Cr floor excludes some thin early days. The first GOLDTEN cycle (Apr 2025) has only 16 eligible days.
- **What G0 doesn't test.** G0 asks only whether the premium exists. Whether any of it is *tradable after costs* is M4's question.

## Files
- `results/g0_results.json`: full numbers, decay and sensitivity.
- `results/cycles_GOLDGUINEA-GOLDTEN.csv`, `results/cycles_GOLDPETAL-GOLDTEN.csv`: per-cycle means for each mark.
- `results/context_cycles_GOLDPETAL-GOLDGUINEA.csv`: 2020–2026 context.
- `results/gold_small_contracts_daily.csv`: the cleaned daily panel (all three contracts, every expiry).

---

## Follow-up 1 · Settlement-reference check: PASSED (13 Oct 2026)

Script: [settlement_check.py](settlement_check.py) · data: `results/settlement_check.csv` (MCX polled spot, last poll on each expiry day, per contract symbol and location).

| Check (18 G0 cycles) | Result |
|---|---|
| GOLDGUINEA vs GOLDTEN settlement reference, ₹/g | **Identical in 18/18 cycles.** Max \|diff\| 0.11 bp (paisa rounding). |
| GOLDTEN reference vs GOLDM 995 spot × 999/995 | **Exact in 18/18 cycles** (max 0.04 bp). The 999/995 factor was applied under every spec version (2025 and 2026). GOLDGUINEA shows the same in the 2024–25 context cycles. |
| GOLDPETAL (Mumbai poll) vs GOLDTEN (Ahmedabad poll) | Median **−3.8 bp**, range −26 to +10 bp, except **30 Jan 2026: −166 bp**. That was the crash day: the Mumbai poll was at 18:39, 56 minutes after Ahmedabad's on a −10% day. |
| 31 Mar 2026 cycle | No poll on 31 Mar. The last polls were on 30 Mar, consistent with an expiry moved to 30 Mar; we used those. |

**Conclusion:** none of the +79 to +94 bp is mechanical. The GOLDGUINEA vs GOLDTEN premium sits on top of an *identical* settlement price. GOLDPETAL's own reference is, if anything, slightly *below* GOLDTEN's, so its premium against its own settlement is a few bp *larger* than the headline. The headline stays conservatively measured against GOLDTEN.

**GOLDPETAL break (context):** in the 2024–25 context cycles, GOLDPETAL's polled spot matches GOLDGUINEA's per gram (−8 to +14 bp). The −250 bp futures discount of 2024 was therefore *not* a difference in the published spot reference. It could still be a difference in the old DDR formula or delivery terms, which needs the pre-2025 GOLDPETAL spec. **It stays in S1 and off the headline.**

## Follow-up 2 · Who actually pays (reframe)

Per-gram cost by route. MCX polled spot is from 13 Oct 2026 midday (Ahmedabad ₹14,755.8/g, Mumbai ₹14,768/g, 999-equivalent, ex-GST). Retail coins are from the same day. File: `results/who_pays.csv`.

| Route | ₹ per gram | Notes |
|---|---|---|
| GOLDTEN, take delivery (10 g bar) | **15,198** | DDR + 3% GST |
| GOLDGUINEA, take delivery (8 g bar/coin) | **15,315** | + entry premium (+79 bp) lost at settlement; no making charge in the spec |
| GOLDPETAL, take delivery (1 g bar/coin) | **15,450** | + entry premium (+94 bp) + ₹100/g making charge (GST on the making charge not modelled) |
| Retail 8 g coin (Augmont, live page) | 15,771 | incl. GST |
| Retail 1 g coin (Augmont, live page) | 16,060 | incl. GST |
| Retail 1 g coin (MMTC-PAMP / Tanishq) | 16,404 / 16,382 | search snippets only; unverified |
| **Trader who exits before tender** | **≈ 9–16** | Not a purchase price. The average premium given up between 60+ and 5–9 trading days out (6–11 bp). |

What this means:
- **Retail traders mostly don't pay it.** Brokers close or block positions before the staggered-delivery window, so the realistic retail cost is the *change* in the premium over the holding period, about ₹9–16/g on average. It is larger when the premium regime shifts (e.g. the 140 → 50 bp slide through mid-2026).
- **Delivery-takers pay it in full, and still beat the coin shop.** Even paying the whole premium plus the making charge:
  - GOLDPETAL delivery is about **₹610/g (3.9%) cheaper** than a retail 1 g coin;
  - GOLDGUINEA delivery is about **₹456/g (3.0%) cheaper** than a retail 8 g coin.
- **So the premium looks like the market price of small-denomination physical gold, not an overcharge.** Its likely ceiling is the retail coin premium. Compared with the 10 g GOLDTEN route, small denominations cost about ₹116/g (GOLDGUINEA) or ₹252/g (GOLDPETAL, incl. making charge) more.
- **Headline:** *"Small MCX gold contracts trade 80–95 bp rich to an identical settlement price, in every cycle for 18 months. Here's who pays it, and when it's worth paying."*
- **Caveats:**
  - Exchange delivery adds vault, assaying and transport costs from the delivery centre, which are not modelled.
  - Coin prices are a single-day snapshot.
  - The spot and coin quotes are hours apart on a volatile day, so treat the gaps as ±1%.

## Follow-up 3 · Implications for M4 and the deck
- **M4 models the delivery leg explicitly.** The only way to capture the premium is to stay short GOLDGUINEA or GOLDPETAL *into settlement* and deliver coins and bars. The model needs the coin sourcing cost (the retail coin premium sets the bar), 8.34% tender margin, vault and assaying, and making-charge receipts. The expected, citable result is "not capturable without delivery capability". A pre-tender mean-reversion rule is kept only as the null it is likely to be.
- **The chooser is the product core.** Holding period and take-delivery are the two inputs that decide the cost.
- **Cycle chart annotations:** the 30 Jan 2026 crash and the May 2026 import-duty hike overlap the Mar–Jun 2026 peak. Show them as *context*, not *cause*.

## Follow-up 4 · Market size: premium carried into delivery (pipeline output)

File: `results/market_size_premium_paid.csv`.
- **Method:** for each cycle, take GOLDGUINEA and GOLDPETAL open interest in grams at two points:
  - **into the window:** the close of the last day before the final 3 trading days;
  - **at expiry:** the final close, which settles at DDR.

  Multiply each by the cycle's G0 premium (VWAP mean) and the settlement price per gram.
- **Last 12 cycles (Oct 2025 – Sep 2026):**
  - **₹10.3 Cr** of premium on positions entering the delivery window (623 kg);
  - **₹1.65 Cr** on positions held to final settlement (104 kg).
- **All 18 cycles:** ₹10.45 Cr and ₹1.68 Cr.
- **Growth:** about ₹2–4 lakh per cycle in mid-2025, rising to ₹1–2 Cr per cycle in 2026 (peak ₹1.97 Cr, Feb 2026 cycle).
- **Caveat:** this uses the cycle-mean premium as a proxy for the premium those particular holders paid at entry.
