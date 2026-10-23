# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

React + Vite, built as a static site (deploy target: Vercel). No server: the app reads the JSON written by `python -m tola.export` (`data/export/`) at build time, and the chooser formula runs in the browser. Charts: ECharts, per the original architecture plan. (Confirmed by the user, 23 Oct 2026.)

## Users

**Primary: retail and HNI gold traders in India** who hold gold through MCX futures and must choose which contract to use: GOLD (1 kg), GOLDM (100 g), GOLDTEN (10 g), GOLDGUINEA (8 g) or GOLDPETAL (1 g). Their job is to get gold exposure, or physical gold, for a given quantity and period at the lowest all-in cost, and to know when they must exit to avoid compulsory delivery.

**First real audience: Hack in Hills '26 judges** (Round 2 submission 24 Oct 2026; finale 20 Nov 2026, Manali), evaluating PS03 "Commodity Derivatives Intelligence". They need to see that every number is defensible.

## Product Purpose

Tola is the fair-price desk for MCX gold. One gram of gold has five prices across MCX's gold contracts. Tola explains why: unit and purity, carry, settlement reference, delivery terms, and an unexplained small-lot residual. It tells a trader which contract is cheapest for their quantity, holding period and broker, whether delivery through futures beats buying a coin, and when they must exit. Success means a trader picks the cheaper contract and exits in time, and a judge can trace every figure to MCX data.

## Positioning

The only PS03 product that measures each contract against **the exchange's own polled spot price it settles to**, and that asks who can actually collect the small-lot premium. Findings it can state that neighbours can't:

- The premium is +79 bp (GOLDGUINEA) and +94 bp (GOLDPETAL) over GOLDTEN in all 18 cycles; it doesn't fade before tender and is removed in one step at settlement.
- Collecting it needs coins sourced under about 0.3% (8 g) or 1.1% (1 g) over spot; the cheapest retail coin is 3.6% / 5.5%. So it is the price of small gold, not a trader's arbitrage.
- The chooser turns that into a decision.

At least six competitor teams report the premium itself, so the premium alone is not the differentiator.

## Operating Context

- Traders compare contracts before entering a position, and check exit-by dates as a contract approaches its tender window (last 3 trading days, 5 before Nov/Dec 2025 contracts).
- Data is refreshed by a maintainer running `python -m tola.refresh` on a laptop (MCX blocks cloud fetchers). The app shows the snapshot's "as of" date and never claims to be live.
- MCX trading hours are 9:00 to 23:30 IST. Prices in Tola are daily (close = last-half-hour VWAP), not intraday quotes.

## Capabilities and Constraints

- **Chooser (core):** grams, holding period (trading days), broker preset, take delivery or not → each contract ranked by effective ₹/g, with exit-by date and premium risk; for delivery, comparison with buying the coin outright. Whole lots only; requests that can't be filled within 10% show why. Must reproduce `data/export/golden.json`.
- **Overview and evidence:** headline finding plus Basis (M2 waterfall), Convergence (M3 same-expiry premiums, live state) and Verdict (M4) pages.
- **Alerts and calendar:** quiet-by-default alert log (onset-only: swing, tender, control, settlement) and every live contract's key dates.
- **Methodology and data:** sources, validation checks, known limits, data as-of dates.
- Terminology: GOLD, GOLDM, GOLDTEN, GOLDGUINEA, GOLDPETAL; bp (basis points); DDR (due date rate, the final settlement price); tender window; polled spot; premium (small contract over GOLDTEN, same expiry); residual.
- Not investment advice; Tola does not place trades. Statutory charges come from Zerodha's published schedule (not yet checked against a contract note); delivery logistics are assumed. Exit-by dates don't know future MCX holidays.

## Brand Commitments

- Name: **Tola** (the traditional Indian gold weight, 11.66 g), team Numero Uno, Hack in Hills '26 PS03.
- Binding visual constraint from the user: **keep the colour palette of Lakshita's gold-terminal design system** (`Design/Design-gold-terminal.md`): near-black canvas #0B0E11, card charcoal #1E2329, hairlines #2B3139, ink #EAECEF, single gold accent #F0B90B reserved for actionable elements, fixed per-contract chart colours, neutral price direction (no red/green for premiums).
- Voice: plain, exact, honest about limits. A figure never appears without a source or an "as of" date.

## Evidence on Hand

- Committed data snapshot (`data/snapshot/`, 2020 to 22 Oct 2026) and app export (`data/export/`): live contracts, chooser inputs, golden quotes, 165 alerts, 30-contract calendar.
- Research write-ups: `PS Research/g0_gate/G0_RESULTS.md`, `m2_basis/M2_RESULTS.md`, `m3_convergence/M3_RESULTS.md`, `m4_verdict/M4_RESULTS.md`, `m5_chooser/M5_CHOOSER.md`; validation report `data/snapshot/VALIDATION.md`.
- Coin prices: two dated retail snapshots (Augmont 13 Oct 2026; five 1 g products 10 Jun 2026) in `data/specs/costs.yaml`.
- **Absent, never to be fabricated:** user testimonials, live intraday prices, broker contract notes, refiner fabrication costs, adoption numbers.

## Product Principles

1. **Decision first.** Every page ends in something a trader can act on: a contract, a date, a cost.
2. **Every number is traceable.** Source and as-of date beside each figure; uncertainty (CIs, risk bands) shown, not hidden.
3. **Honest about what isn't capturable.** Say plainly when an edge doesn't exist or is fragile.
4. **Direction is information, not alarm.** A premium is neither good nor bad; sign and words carry it.
5. **Quiet by default.** Alerts fire on onsets only; most days nothing needs attention.

## Accessibility & Inclusion

WCAG 2.1 AA: text contrast per the design system's verified ratios, 3:1 control boundaries, visible focus rings, identity never by colour alone (chart legends and labels, status icons), a table view for every chart, and `prefers-reduced-motion` respected.
