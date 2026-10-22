# 08 · Competitor tracker (Round 2)

**Snapshot: 23 Oct 2026.** This updates [01_github_repos.md](01_github_repos.md) §A, which was pulled on 13 Oct. Sources: GitHub repository search (9 discovery queries, created on or after 20 Sep), each repo's README, and its commits since 13 Oct. Repo list and tiers: [tracker/repos.json](tracker/repos.json). To refresh, run `python "PS Research/tracker/track_competitors.py"`. It prints what changed since the last snapshot and lists any new repos to triage.

Tiers: **1** = closest to Tola's angle (premium, settlement, delivery), **2** = real data or a solid pipeline, **3** = UI-heavy, synthetic data or thin.

---

## Summary

1. **The field has roughly quadrupled.** We now track **42 public PS03 repos**, up from 11 on 13 Oct. That is 10 of the original 11 still live (the two govindbairagi3186 repos are still 404) and **32 new**. Three of the new ones predate our 13 Oct sweep and were missed: `japesh3737/AurumLens` (20 Sep), `Umar1988104/GoldParity` (21 Sep) and `NaitikBuilds/aurumspread` (28 Sep). Many teams pushed for the first time on 20–22 Oct, so expect more before 31 Oct.
2. **Our headline finding is no longer ours alone.** At least six teams now report that the small contracts trade rich to GOLDTEN for the same expiry:
   - **AuRA**: GOLDPETAL +69 bp median, GOLDGUINEA +51 bp. Calls it "a standing premium, not a mispricing".
   - **thedarknight262**: GOLDPETAL +76 bp, GOLDGUINEA +67 bp median over 2,030 same-expiry contract-days.
   - **Bullion Basis**: one day only (14 Oct), +55.7 / +49.1 bp.
   - **arb-bound**: explains it as a fabrication-cost "retail convenience premium".
   - **dhir-1 (Lexa)**: 2 expiries, settlement (DDR) convergence.
   - **gold-rv**: GOLDPETAL repricing break in Nov 2024.
3. **Two teams have intraday or daily-live data.** AuRA polls MCX's 5-level order book every 15 seconds during market hours and shows an *executable* premium at bid and ask. arb-bound-live commits a daily MCX scan through TinyFish.
4. **gold-rv is the most complete build.** It has 75 commits since 13 Oct, 47,596 prices from 2011 to 2026, a clean frozen-rule test on 2011–2023, a demo video, CI and a 3D pitch deck. It also **tried to measure slippage from daily OHLC (Roll 1984, Corwin–Schultz 2012) and found it measures volatility, not spread.** That bears directly on our M4 plan to use the EDGE estimator.
5. **Our repo has been public since 14 Oct 08:48 IST.** That includes `G0_RESULTS.md` (the premium, its CI, no decay, who pays) and our competitor research. AuRA and Bullion Basis were created on 15 Oct. That is timing, not evidence of copying. Several teams could have found the premium independently, but anyone can read our full plan.

---

## What still sets Tola apart (checked against every README on 23 Oct)

| Tola element (scope unchanged) | Who else does anything similar | Status |
|---|---|---|
| **Settlement-reference proof**: GOLDTEN and GOLDGUINEA settle to the identical price per gram in 18/18 cycles (≤ 0.11 bp), from MCX polled spot; GOLDPETAL 3.8 bp below via Mumbai spot | dhir-1: DDR convergence on **2 expiries**. Bullion Basis: one 30 Sep DDR, "secondary source, verify". | **Still ours.** We have the only multi-cycle version. Lead with it. |
| **Pre-registered gate, four marks including VWAP, cycle-clustered bootstrap** | Bullion Basis pre-registers one primary test. AuRA and SwarnaScope report Deflated Sharpe. Nobody uses VWAP or a cycle-clustered CI. | Ours on the robustness details |
| **Premium does not decay before delivery; only final settlement removes it** | dhir-1 notes the last traded close is still 0.44–1.02% above the DDR on 2 expiries. Nobody measures it by holding horizon. | Ours |
| **Who pays**: exit-before-tender cost (6–11 bp) vs delivery-takers; GOLDPETAL delivery vs retail 1 g coin (≈ ₹610/g cheaper) | arb-bound explains the premium with an *assumed* ₹20–60/bar fabrication cost. Nobody uses the real ₹100/g making charge (Dec 2024 circular) or a retail coin price. | **Ours, and the strongest story.** arb-bound is the closest framing. |
| **"Which contract?" chooser** (quantity, horizon, take-delivery) | **No README describes one.** Others offer z-score alerts or trade signals. | Ours. This is the product core. |
| **₹10.3 Cr of premium entering delivery windows (12 cycles)** | Nobody sizes it | Ours |
| **Measured slippage (EDGE via `bidask`)** | gold-rv tried Roll and Corwin–Schultz and got 26–31 bp for every contract alike (volatility). AuRA uses real live bid and ask. | **At risk.** See the implications below. |
| Normalize → carry → z-score → walk-forward → costs → "no edge" | 30+ teams | Table stakes, as expected on 13 Oct |

---

## Tier 1: profiles

**gold-rv** · [CodeByDivyansh-tech/nexora-gold-rv-](https://github.com/CodeByDivyansh-tech/nexora-gold-rv-) (renamed from `gold-rv`) · [gold-rv.vercel.app](https://gold-rv.vercel.app)
- **Data:** 2011 to 21 Oct 2026: 47,596 daily settlements, 599 contracts, downloaded per contract from MCX. Their data matches a 55,457-row copy shared by another team with 0 mismatches.
- **Headline:** "the gaps are real, but no persistent edge is proven after costs". The clean test, with the rule frozen on 2011–2023 data, loses ₹5.49 L over 151 trades (t = −3.63). Their own 2025–26 test year, t = 1.89, is honestly labelled "not a clean test".
- **Slippage:** assumed 5 bp per order, which is 82% of cost. OHLC estimators failed, and they say only real broker fills can settle it.
- **Nov 2024 GOLDPETAL repricing:** located with a level-shift test; cause unconfirmed.
- **Since 13 Oct:** 75 commits. Long-run history, daily data through 21 Oct, a pitch video (22 Oct), CI.

**AuRA** · [Surjune/aura-mcx-gold](https://github.com/Surjune/aura-mcx-gold) · team Lightning Logics · [aura.lightninglogics.me](https://aura.lightninglogics.me), [/live](https://aura.lightninglogics.me/live), [2-min video](https://youtu.be/29peqQnTcX8)
- **Data:** 716 sessions of real MCX data (Jan 2024 – Oct 2026), fetched with Playwright and Edge, plus DuckDB.
- **Findings:** standing premium (GOLDPETAL +69 bp median, never below +11; GOLDGUINEA +51 bp). Walk-forward: +22 bp per trade in development, **−1.4 bp on an untouched 6-month holdout**. 78% of the development profit came from the 30 Jan 2026 crash close. They report Deflated Sharpe and a bootstrap p-value.
- **Live monitor:** 5-level order book every 15 s, executable premium, flags only above a 13 bp cost hurdle, replays the last session when the feed is off.
- **Since 13 Oct:** 32 commits, mostly hourly live snapshots.
- **Why it matters:** the closest to our *finding*. It has a live layer and no chooser.

**arb-bound / arb-bound-live** · [j4yop/arb-bound](https://github.com/j4yop/arb-bound), [j4yop/arb-bound-live](https://github.com/j4yop/arb-bound-live) · [arb-bound.vercel.app](https://arb-bound.vercel.app), [arb-bound-live.vercel.app](https://arb-bound-live.vercel.app)
- **Approach:** a structural no-arbitrage bound = Δ fabrication overhead (assumed ₹20–60/bar) + purity wedge + statutory costs. It comes to 13–40 bp for 999/999 pairs and 240–362 bp against GOLDM. Only one direction is tradeable, because the small bar is dearer to mint.
- **Results:** walk-forward on 11,771 rows finds no edge. The Nov 2024 break is explained as "retail premium compression". A TinyFish agent read **204 MCX circulars** (Oct–Dec 2024) and found no spec change.
- **Extras:** Pyodide in-browser playground; 95 tests; PPTX generated from the report JSON.
- **Since 13 Oct:** 24 commits across both repos. The live repo commits a daily MCX scan (16–22 Oct).
- **Why it matters:** the closest to our *explanation* ("small gold costs more to make"). They assume the cost; we have the circular and a retail benchmark.

**Bullion Basis** · [strange-exe/Bullion-Basis](https://github.com/strange-exe/Bullion-Basis) · team Blaze · [bullion-basis.pages.dev](https://bullion-basis.pages.dev)
- **Findings:** one real bhavcopy (14 Oct). GOLDGUINEA +55.7 ± 5.0 bp, GOLDPETAL +49.1 ± 4.6 bp (curve fit). Spot is identical for GOLDTEN and GOLDGUINEA; GOLDPETAL is −4.5 bp (Mumbai). The 30 Sep DDR gap is 0.0 bp.
- **Method:** a pre-registered primary test (GOLDGUINEA vs GOLDTEN, level signal). The walk-forward runs on labelled synthetic history until they add more data.
- **Since 13 Oct:** created 15 Oct, 3 commits, quiet since.
- **Why it matters:** their framing is nearly ours, on 1 day of data instead of 18 cycles. Watch whether they backfill.

**thedarknight262** · [thedarknight262/HackNHills](https://github.com/thedarknight262/HackNHills)
- **Data and findings:** 9,616 contract-days, 2,030 same-expiry contract-days. "Persistent retail micro-contract markup": GOLDPETAL mean +95 bp, GOLDGUINEA +87 bp.
- **Backtest:** claims the edge survives T+1 with limit orders in a "peak liquidity window" (+3.2%, 16 trades). That is a thin sample, and judges may probe it.
- **Since 13 Oct:** created 21 Oct, 5 commits (Streamlit).

**Lexa** · [dhir-1/Mcx-gold-dhir](https://github.com/dhir-1/Mcx-gold-dhir)
- **Findings:** DDR settlement convergence on 2 expiries. GOLDGUINEA and GOLDPETAL settle within 0.00% and −0.26% of GOLDTEN, while the last traded close was 0.44–1.02% above.
- **Since 13 Oct:** 6 commits (20 Oct), Streamlit plus a walkthrough notebook.
- **Why it matters:** the only other team using settlement prices as the reference, but on 2 expiries.

---

## The original 11 (from 01 §A): what changed since 13 Oct

| Repo | Last push | Change |
|---|---|---|
| gold-rv → `nexora-gold-rv-` | 22 Oct | **Renamed, 75 commits.** See tier 1. |
| manaslalwani190/auraspread | 21 Oct | 6 commits. Added 2004–2024 data and a comparison table "vs Parity". The rest is UI polish (splash, light mode). |
| Mayank-iitj/GoldLens | 19 Oct | 1 dependency fix. Static. |
| PALLAK-DEVI/commodity-derivatives-intelligence | 8 Oct | None. The same team (Bits and Bytes) now builds in `pyharshcodes/Hack_In_Hills`: "triangular arbitrage detector", Monte Carlo, macro stress tests. |
| jayanti614/goldparity | 8 Oct | None. Identical README in `Umar1988104/GoldParity`, created 21 Sep, live at gold-parity.vercel.app. |
| rahulkumar1311/AurumIQ, aritradutta7858-netizen/AurumIQ | 4 Oct | None |
| mahamunisarvesh738/MCX_GOLDINTEL | 10 Oct | None |
| satyamkr11/gold-contract-radar | 2 Oct | None |
| krishsingh-ai/cdi-terminal | 6 Oct | None |
| govindbairagi3186/GOLDINTEL, /ARTHIQ | — | Still 404 |

## New entrants, tiers 2 and 3

| Repo | Tier | Created | Data | Note |
|---|---|---|---|---|
| [sru-codes/aurum-spread](https://github.com/sru-codes/aurum-spread) | 2 | 14 Oct | Synthetic demo fixture (labelled); import pipeline for real files | Strong data hygiene (hashing raw bytes, rejection reports). A separate `gold-api` repo provides XAU/USD and FX context. Live on Railway. |
| [Adarsh1577/goldlens-mcx-gold](https://github.com/Adarsh1577/goldlens-mcx-gold) | 2 | 21 Oct | Real, 35 days (1 Sep – 20 Oct) | "No edge even before costs", honestly stated |
| [SAHIBA-09/summit-syndicate-mcx-gold](https://github.com/SAHIBA-09/summit-syndicate-mcx-gold) | 2 | 18 Oct | Real, 25 days | Colab. Break-even falls from 3.7 to 0.8 bp with one-day execution delay. |
| [udayanbhandari/HackInHills](https://github.com/udayanbhandari/HackInHills) (SwarnaScope) | 2 | 22 Oct | Real with synthetic fallback | Five-part falsification suite: placebo, permutation, bootstrap, DSR, cost sweep |
| [Dhrupad-05/GoldMCX](https://github.com/Dhrupad-05/GoldMCX) | 2 | 9 Oct | Real files, staged validation | Median/MAD novelty scoring, backend-first |
| [NaitikBuilds/aurumspread](https://github.com/NaitikBuilds/aurumspread) (AurumEdge) | 2 | 28 Sep | — | Frozen verdict protocol; stats battery still "planned". Quiet since 1 Oct. |
| [Umar1988104/GoldParity](https://github.com/Umar1988104/GoldParity) | 2 | 21 Sep | Real | Mirror of jayanti614/goldparity |
| [pyharshcodes/Hack_In_Hills](https://github.com/pyharshcodes/Hack_In_Hills) | 3 | 20 Oct | — | Bits and Bytes v2. Feature-heavy terminal. |
| [Mohit-Tanwar25/Hack-in-Hills-Hackathon](https://github.com/Mohit-Tanwar25/Hack-in-Hills-Hackathon), [sunilgupta046/MCX-Gold-RVA](https://github.com/sunilgupta046/MCX-Gold-RVA), [Abhimanyu1712/Aureon](https://github.com/Abhimanyu1712/Aureon), [shivammaurya2903/MCX-Gold](https://github.com/shivammaurya2903/MCX-Gold), [SujalRathore18/GoldLens](https://github.com/SujalRathore18/GoldLens) | 3 | 7–22 Oct | **Synthetic or sample fixtures** | Full-stack shells with synthetic generators |
| [vds18/GoldLens](https://github.com/vds18/GoldLens), [jiyanmansuri/HackInHills](https://github.com/jiyanmansuri/HackInHills), [samuelmichaelalva/frostbite](https://github.com/samuelmichaelalva/frostbite), [shreaysvy/Aurum-Synthesis](https://github.com/shreaysvy/Aurum-Synthesis), [himanshugit786/…](https://github.com/himanshugit786/MCX-quantitative-arbitrage-), [Burhanmalu/Goldlens](https://github.com/Burhanmalu/Goldlens), [japesh3737/AurumLens](https://github.com/japesh3737/AurumLens) | 3 | 20 Sep – 21 Oct | Mixed or unclear | Dashboards and scrollytelling. Little method detail. |
| gfiinnovators/aureus-rv-3.0, sharayubhokare2396-tech/…, gayathrisnair2006/Nexora_gold_contract, arnavkotnala/-hack-in-hills-goldie, sm8935983-ai/× 2 | 3 | 5–22 Oct | — | Empty, README-only, or no README yet. **Re-check: aureus-rv-3.0 ("lifecycle-aware") is described like a serious entry.** |

---

## Libraries (01 §B–G): no material change

Stars and pushes moved a little; nothing changes a decision.
- `mcxlib` is still 0.4 (1 May 2026) with the stale POST endpoints.
- `bidask` is still 2.1.0.
- `curl_cffi`, `arch`, `duckdb` and `lightweight-charts` all had pushes on 22 Oct.
- `jugaad-data` no longer reports a licence through the API. Re-check before copying anything.

---

## Implications for our build (scope unchanged)

1. **Don't lead with "the premium exists".** Judges will see it in five other decks. Lead with what only we have:
   - settlement-reference proof over 18 cycles;
   - no decay until settlement, so the cost depends on holding horizon;
   - who pays, with the real making charge and retail coin benchmark;
   - the chooser.

   One slide should acknowledge that others see the gap, and show why ours is the explanation and the decision tool.
2. **De-risk M4 slippage on day 1.** Run EDGE (`bidask`) on our cycles before building on it. If, like gold-rv's Roll and Corwin–Schultz results, it returns similar numbers for every contract (volatility, not spread), fall back to the half-tick floor plus the broker preset, and say so on screen. AuRA's live order book shows real bid and ask are obtainable, but adding that would be a scope change, so flag it, don't build it.
3. **Nov 2024 GOLDPETAL break (stretch S1).** gold-rv located it; arb-bound reports, via 204 circulars, that no spec change happened then. Our S1 hypothesis (the Dec 2024 making-charge circular) is *after* that break. Read arb-bound's `docs/NOV2024.md` before spending time on S1.
4. **Repo visibility.** Everything we have, including G0 results and this tracker, is public at `Mrigank005/Tola`. Decide whether to keep it public until submission (check the Round 2 rules for whether the repo must be public).
5. **Re-run the tracker** around 27 Oct and 30 Oct. Many entrants first pushed on 20–22 Oct.
