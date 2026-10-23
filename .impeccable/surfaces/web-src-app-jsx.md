---
version: 1
slug: "web-src-app-jsx"
primary_target: "web/src/App.jsx"
related_targets: ["web/index.html"]
---

# Tola web app

Scope: the whole static web app (`web/`): Rates (home), Choose, Why prices differ, Convergence, Verdict, Alerts & calendar, Method. Mode: Operate.

Audience and job: retail/HNI gold traders choosing which MCX gold contract to hold and when to exit; Hack in Hills judges checking that every number is traceable. Data comes only from `data/export/*.json`. Constraints: palette pinned to `Design/Design-gold-terminal.md`; neutral price direction; not investment advice.

## Direction contract

THESIS: Tola is the bullion rate board every Indian gold buyer already reads: one posted price per gram for each MCX contract, today, with what you actually pay beside it. It refuses the trading-dashboard default of stat tiles, a hero number and a chart wall.

OWN-WORLD: The gold-terminal palette (near-black #0B0E11 floor, charcoal #1E2329 board, steel #2B3139 rules, ink #EAECEF figures, gold #F0B90B only on what you press). Rows ruled like a jeweller's rate card, large tabular numerals right-aligned in fixed columns, contract codes in JetBrains Mono, a posted date stamp on every board, Archivo for everything else (rates set condensed at 82% width; Inter was dropped as an overused face, and only the palette was pinned).

STORY: The visitor sees five contracts' rates per gram for the day, learns the small ones post 40–60 bp richer, asks for their quantity and holding period, and leaves knowing which contract to hold, what it costs and the date to exit by.

FIRST VIEWPORT: Top nav (Tola, page tabs, as-of stamp). A full-width rate board: five contract rows (code, ₹/g at 999, premium over GOLDTEN as a fixed magnitude tick, fair price, today's turnover) under a posted date stamp. Directly below, the chooser docked as one row of inputs (grams, hold days, exit or deliver, broker) with the gold "Compare" button; results appear as a ranked board in place.

FORM: Zaveri Bazaar rate board, position 1 on the ordered list (taken as IMPECCABLE'S PICK over the assigned Railway Timetable). seed:a0e6500dd6fffd74. Signature move: every page leads with a posted rate board; premium size reads on one fixed magnitude ramp everywhere. Kept disciplines: row state by rule form (solid live, dashed thin, struck in tender), one figure owns each page, focus expands a row in place, plain labels.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
