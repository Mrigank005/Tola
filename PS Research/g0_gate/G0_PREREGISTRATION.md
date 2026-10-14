# G0 · Small-Lot Premium Gate: Pre-Registered Decision Rule

**Frozen:** 13 Oct 2026, before the backfill was run. Only the two probe cycles (Aug and Sep 2026) had been seen. Approved by the team lead with three amendments: VWAP replaces the polled-spot mark, the bootstrap is clustered by cycle, and there is a minimum cycle count.
**Decision due:** Fri 16 Oct 2026.

## Hypothesis
At the same expiry, GOLDGUINEA and GOLDPETAL trade at a **positive premium per gram** over GOLDTEN on pre-tender days. All three settle to the same 999-equivalent polled spot price per gram.

## Data
- **Cycles.** Every completed cycle where GOLDTEN, GOLDGUINEA and GOLDPETAL share an expiry date, from GOLDTEN's first expiry (Apr 2025) to Sep 2026. That should be about 18 cycles.
- **Expiry discovery.** One date-wise bhavcopy call per month.
- **Contract histories.** One `GetCommoditywiseBhavCopy` call per contract.
- **Context only, not part of the decision.** GOLDGUINEA vs GOLDPETAL per cycle back to Jan 2020.

## Eligible day (both legs must pass)
1. The trading day is **not among the contract's last 5 trading days**. That is the 2025-spec tender window; the 2026 spec uses 3, so 5 is conservative for every cycle.
2. Volume > 0, and Open, High and Low are all non-zero (no carried-forward no-trade rows).
3. **Value ≥ ₹1 crore** (100 lakh) traded that day.

A cycle **survives** if it has **≥ 10 eligible days**.

## Price marks (per gram; all three contracts are 999, so no purity adjustment)
| Mark | Formula |
|---|---|
| Close | Close ÷ quote grams |
| Open | Open ÷ quote grams |
| Mid | (High + Low) ÷ 2 ÷ quote grams |
| VWAP | Value × 10⁵ ÷ (Volume × lot grams) |

Premium (bp) = 10⁴ × (mark_small ÷ mark_GOLDTEN − 1), computed for the pairs GOLDGUINEA−GOLDTEN and GOLDPETAL−GOLDTEN.

The polled-spot basis was **dropped as a mark**. GOLDTEN and GOLDGUINEA share the same Ahmedabad poll per gram, so the spot cancels and the comparison collapses back to Close. It remains a GOLDPETAL-only diagnostic (Mumbai vs Ahmedabad) in M2.

## Statistics (per pair, per mark)
- **Cycle mean** = mean premium over the cycle's eligible days.
- **Pooled mean** = mean of the cycle means (each cycle weighted equally).
- **95% CI** = percentile interval from a **cluster bootstrap over cycles**: resample whole cycles with replacement, 10,000 reps, seed 20261013.
- **Hit rate** = share of surviving cycles with cycle mean > 0.

## Decision rule (per pair)
- **GO** requires all of:
  - surviving cycles ≥ 8;
  - and on **every one of the four marks**: pooled mean ≥ +15 bp, CI lower bound > 0, and hit rate ≥ 75%.
- **PARTIAL** if either:
  - surviving cycles < 8 (whatever the CI says); or
  - not GO, but the **VWAP and Close** CIs both lie entirely above 0.
- **NO-GO** otherwise.

**Overall:**
- **GO** if at least one pair is GO. The headline names only the pairs that passed.
- **PARTIAL** if no pair is GO and at least one is PARTIAL.
- **NO-GO** otherwise, which triggers the agreed fallback framing: "contract-fairness desk".

## Sensitivity (reported, never decisive)
- Value floor ₹0.25 Cr and ₹5 Cr.
- 3-day instead of 5-day tender exclusion.
- Excluding cycles expiring Jan–Mar 2026 (the crash).
- Premium by days-to-expiry bucket (the decay shape).
