# M5 · "Which contract?" chooser, alert log and calendar

**Built:** 23 Oct 2026 on the snapshot (data through 22 Oct 2026). The code is `tola/chooser.py`, `tola/alerts.py` and `tola/export.py`; the web app reads `data/export/*.json`. Tests are in `tests/test_chooser.py`.

## The question it answers

*"I want G grams of gold for H trading days (or delivered after H days). Which MCX contract costs me least, and by when must I get out?"*

M4 showed nobody but a coin maker can collect the small-lot premium. So the useful product for a trader is the cost of *holding* gold through each contract, which is what this ranks.

## The formula (per contract, ₹ per gram)

For each symbol, the chooser uses the nearest live expiry that fits the holding period.
- **If you exit before tender:** the contract's last day before its tender window must be at least H trading days away.
- **If you take delivery:** the contract must settle at least H trading days out.

It uses whole lots only: GOLD 1 kg, GOLDM 100 g, GOLDTEN 10 g, GOLDGUINEA 8 g, GOLDPETAL 1 g. Lots must land within 10% of the grams asked for; anything else is listed as not possible, with the reason.

| Line | Exit before tender | Take delivery |
|---|---|---|
| Trading | Entry and exit orders: statutory charges + broker preset + 1 tick | Entry order |
| Premium | Expected **change** in the premium over GOLDTEN (same expiry) over H days, from history since Apr 2025. ±1 sd shown as risk. 0 for GOLDTEN, GOLDM and GOLD (the reference contracts). | Today's **residual** (M2), lost in full at settlement (M3) |
| Net carry | (implied carry − risk-free rate) × calendar days held | Same, to settlement |
| Making charge | — | From the contract's spec version (₹30/g GOLDTEN, ₹25/g GOLDGUINEA, ₹100/g GOLDPETAL) |
| GST | — | 3% of value |
| Margin funding | — | 8.34% tender margin over the tender days + 25% delivery margin for 2 days, at the risk-free rate |
| Logistics | — | ₹10/g vault, assay, transport (assumed) |
| **Compare with** | — | Buying the coin outright: cheapest observed retail premium + GST (`data/specs/costs.yaml`) |

**Why net carry?** A futures buyer keeps their cash until settlement and earns the risk-free rate on it, so only carry *above* that rate is a cost. It's the same for every contract with the same holding period, so it never changes the ranking. It is shown because it changes the decision against buying physical gold: on 22 Oct 2026, implied carry was 12.1% against a 5.73% T-bill.

## What it says today (22 Oct 2026)

| Request | Cheapest | Then | Notes |
|---|---|---|---|
| 100 g, exit after 20 days | **GOLDTEN Nov** ₹73.3/g, GOLDM Dec ₹73.4/g | GOLDPETAL ₹82.6/g (±₹91 risk), GOLDGUINEA ₹86.0/g (±₹99) | GOLD can't do 100 g. Net carry is about ₹70/g of the ₹73. |
| 10 g, exit after 60 days | **GOLDTEN Jan** ₹222/g | GOLDPETAL ₹258/g (±₹156) | Only GOLDTEN and GOLDPETAL can do 10 g |
| 1 kg, exit after 40 days | **GOLDTEN / GOLDM / GOLD** ₹145–146/g | GOLDPETAL ₹165/g, GOLDGUINEA ₹171/g | The big lots tie; small lots cost ₹20–26/g more |
| 8 g, take delivery | **GOLDGUINEA Nov** ₹650/g over spot | GOLDPETAL ₹736/g | **Buying an 8 g coin costs ₹953/g over spot** |
| 100 g, take delivery | **GOLDM Dec** ₹562/g (100 g bar, 995) | GOLDTEN ₹577/g; GOLDGUINEA ₹647/g; GOLDPETAL ₹733/g | 3% GST is about ₹430/g of every delivery cost |
| 1 g, take delivery | **GOLDPETAL Nov** ₹738/g | — | **A 1 g coin costs ₹1,227/g over spot** |

Two messages for the pitch:
- **For trading, the small contracts cost more** (₹9–27/g) and carry ±₹91–156/g of premium risk. GOLDTEN or GOLDM is the answer unless you need fewer than 10 g.
- **For delivery, futures beat the coin shop** by ₹300–490/g, even after paying the premium, making charge and GST.

## Alert log (quiet by default)

An alert fires on the day a condition **starts**, not every day it stays true:

| Type | Fires when |
|---|---|
| swing | The premium over GOLDTEN (most liquid same-expiry pair) moves beyond 1.5 sd of its last 40 eligible days: M4's mean-reversion signal |
| tender | A live contract is 5 trading days from its tender window (gives the exit-by date) |
| control | GOLD vs GOLDM moves beyond 10 bp |
| settlement | A same-reference pair settles more than 20 bp apart |

From Apr 2025 to 22 Oct 2026: **301 of 402 trading days had no alert.** The 165 alerts break down as 84 tender notices, 49 swings, 28 control-pair moves and 4 settlement gaps. The latest swing: on 14 Oct 2026, GOLDGUINEA was at +64 bp over GOLDTEN, against a 40-day average of +45 bp.

## Calendar

All 30 live contracts with first traded day, tender start, exit-by date (the last trading day before tender), last trading day and today's turnover (thin or untraded flagged). Dates past the last observed trading day use weekdays: future MCX holidays aren't known.

## For the web app

`data/export/chooser.json` holds everything the formula needs: live contracts, premium-change history, cost schedule, delivery inputs, coin prices and lot sizes. That lets the app recompute quotes for any input in the browser. `golden.json` holds this module's answers for seven reference requests; the app's version must match them.

## Limits

- **Premium change and risk** come from 18 months of history, including the Jan–Mar 2026 swing.
- **Exit-by dates for live contracts** don't know future holidays.
- **Broker forced exits:** brokers may close positions *before* the tender window. Check yours.
- **Delivery assumptions:** logistics (₹10/g) is assumed. GST is treated as a cost (a GST-registered buyer could reclaim it).
