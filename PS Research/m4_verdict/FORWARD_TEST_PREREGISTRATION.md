# M4 forward test: pre-registration

**Frozen:** 23 Oct 2026, before any data after 22 Oct 2026 is fetched. Nothing below changes once written. Any change goes in a dated addendum at the bottom, and results are reported both with and without it.

## What is being tested

Whether the mean-reversion rule on the same-expiry premium keeps earning net of costs on data it has never seen. In-sample it earned about +5–15 bp a trade in the current contract regime outside Jan–Mar 2026 (M4_RESULTS.md).

## The rule (exactly as in `tola/backtest.py` on this date)

- **Pairs:** GOLDGUINEA/GOLDTEN, GOLDPETAL/GOLDTEN, GOLDPETAL/GOLDGUINEA; same expiry; 200 g per leg, gram-matched.
- **Eligible day:** both legs ₹1 Cr+ turnover, neither leg in its tender window.
- **Signal:** z = (close premium − mean of the previous W eligible days in the same cycle) / their sd. Enter short the premium at z > k, long at z < −k. Exit when z crosses 0, or on the last eligible day before tender.
- **Fills:** the next eligible day's VWAP.
- **Configs:** W ∈ {20, 40, 60}, k ∈ {1.0, 1.5, 2.0}.
- **Walk-forward:** each month uses the config with the best mean net bp over trades already closed before the month began (5+ trades; otherwise W=40, k=1.5).
- **Costs:** `data/specs/costs.yaml` as of this date (statutory, Zerodha-rate brokerage, 1 tick of slippage per order).

## Forward window and data

- **Trades counted:** walk-forward trades whose **entry date is after 22 Oct 2026**, through the finale on **20 Nov 2026**. A trade still open on 20 Nov is reported both marked to that day's VWAP and as open.
- **Data:** `python -m tola.refresh` run at least every few trading days. Earlier signals can't change when later data arrives; the truncation test in `tests/test_backtest.py` guarantees it.
- **Report:** section 10 of `m4_tables.md` (`python "PS Research/m4_verdict/summarise_m4.py"`).

## What we expect, written down in advance

- **Few trades.** The premium has been calm since April 2026, and the rule traded only 3 times from April to October. **0–6 forward trades is the expected range.** Zero trades is a valid outcome and will be reported as "the rule stayed quiet".
- **If it trades:** the in-sample current-regime outcome is about +5–15 bp a trade net. A forward mean below 0 over 5+ trades counts against the edge. A few trades can't confirm it; they can only fail to contradict it.
- **Nothing in this test changes the delivery verdict.** That rests on settlement prices and coin costs, not on trading.

## Addenda

(none)
