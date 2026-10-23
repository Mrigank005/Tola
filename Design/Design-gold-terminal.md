## Overview

Tola is the fair-price desk for MCX gold: a dark, data-dense web app that explains why one gram of gold has five prices, and helps a trader choose which contract to hold. The atmosphere is a **cool near-black canvas** (`{colors.canvas}` — #0B0E11, "Near-Black") with **soft ink typography** (`{colors.ink}` — #EAECEF) and a single **warm gold accent** (`{colors.accent}` — #F0B90B) that marks everything you can act on.

The structure is inherited from a high-contrast developer-tool system (one sans family, confident weight-700 headlines, flat surfaces, no shadows), re-tuned for a financial product. Pure white on pure black is replaced by a cool off-white (#EAECEF) on near-black (#0B0E11), which has lower glare and reads better over long sessions with tables and charts. The yellow is deliberately not the text color: it is the "press here" signal.

**Palette provenance.** The colors follow the Binance system: near-black canvas `#0B0E11`, card charcoal `#1E2329`, steel hairlines `#2B3139`, cool off-white text `#EAECEF`, muted slate `#707A8A` / `#848E9C`, and Warm Gold `#F0B90B` (hover `#FFD84D`, pressed `#D9A300`) as the one brand color, always with near-black text on it. Also borrowed: depth from flat color blocks (no gradients, no glow), hairlines that match the next surface step, and a single accent that stays scarce. Not borrowed: green/red price direction (Tola keeps direction neutral, see Status), the light-theme transactional mode, and BinanceNova/Plex (Inter and JetBrains Mono stay).

Type runs **Inter** at 700 / 600 / 500 / 400, with **tabular figures** wherever numbers line up, and **JetBrains Mono** for code, contract symbols in tables, and raw data.

### The 60 · 30 · 10 rule

| Share | Role | Tokens | Where |
|---|---|---|---|
| **60% dominant** | Dark surfaces | `{colors.canvas}` #0B0E11 · `{colors.surface}` #1E2329 · `{colors.hairline}` #2B3139 | Page canvas; cards, modals and top nav on the elevation shade; borders and dividers |
| **30% secondary** | Charcoal surfaces and soft ink | `{colors.surface}` #1E2329 · `{colors.surface-raised}` #2B3139, with `{colors.ink}` #EAECEF and derived text colors used for legibility | Cards, nested surfaces, text and supporting hierarchy |
| **10% accent** | Yellow | `{colors.accent}` #F0B90B | Primary buttons, active navigation, notification dots, focus rings, selected controls, high-importance lines |

**Key characteristics:**
- Cool near-black canvas with depth from three steps of black: canvas → surface → hairline. No drop shadows except on modals.
- Ink (`{colors.ink}`) carries all headline and primary text at 13–16:1 contrast, without the glare of pure white.
- Yellow (`{colors.accent}`) means "actionable". If something is yellow and you can't click it, it's a bug. **Never** yellow for paragraphs, headings, stat numbers or chart series.
- Numbers are the product. Tabular figures, signed basis points, Indian digit grouping (₹1,23,456; ₹10.3 Cr) and an "as of" date on every figure.
- Charts use a separate, validated data palette (blue, red, aqua, violet), so the series never compete with the yellow actions.
- Dark only. There is no light theme.

## Colors

### Surfaces (60%)
- **Canvas** (`{colors.canvas}` — #0B0E11, Near-Black): The page floor. Also the inset background of text inputs and code blocks.
- **Surface** (`{colors.surface}` — #1E2329, Card Charcoal): Cards, chart cards, modals, top navigation, table headers. The default container.
- **Surface Raised** (`{colors.surface-raised}` — #2B3139): Nested elements inside a surface (stat tiles in a card, secondary buttons, neutral tags), row hover, menu hover.
- **Hairline** (`{colors.hairline}` — #2B3139, Steel Hairline): 1px borders on cards, dividers, table row lines, chart gridlines.
- **Hairline Strong** (`{colors.hairline-strong}` — #3E4651): Chart axes and baselines, secondary-button borders, emphasis dividers.
- **Control Border** (`{colors.control-border}` — #707A8A): Borders of inputs, selects, checkboxes and toggles. Clears 3:1 against `{colors.surface-raised}` (3.0), `{colors.surface}` (3.65) and `{colors.canvas}` (4.46), as WCAG requires for control boundaries.
- **Scrim** (`{colors.scrim}` — rgba(8, 10, 12, 0.72)): Behind modals.

### Text (30%)
- **Ink** (`{colors.ink}` — #EAECEF): Headlines, large typography, stat numbers, primary text, table values. 16.4:1 on canvas, 13.4:1 on surface.
- **Body** (`{colors.body}` — #B7BDC6): Running text and paragraphs. 10.2:1 on canvas, 8.4:1 on surface.
- **Muted** (`{colors.muted}` — #848E9C): Captions, axis labels, table headers, timestamps, placeholders, footer links. 5.8:1 on canvas, 4.8:1 on surface (AA for small text).
- **Faint** (`{colors.faint}` — #6A7383): Disabled text and decorative separators **only**. 3.3:1 on surface, so it is never used for information.
- **On Accent** (`{colors.on-accent}` — #0B0E11): Text and icons on yellow. 13.6:1 (black on yellow is the signature pairing; never white on yellow).
- **On Ink** (`{colors.on-ink}` — #0B0E11): Text on ink key tags. 16.4:1.

### Accent (10%)
- **Accent** (`{colors.accent}` — #F0B90B): Primary buttons, active nav indicator, selected segment, checked toggle/checkbox, notification dots, focus ring, slider fill, inline links (short spans only, underlined).
- **Accent Hover** (`{colors.accent-hover}` — #FFD84D): Primary button hover.
- **Accent Pressed** (`{colors.accent-pressed}` — #D9A300): Primary button pressed. Keep near-black text for strong contrast.
- **Accent Wash** (`{colors.accent-wash}` — rgba(240, 185, 11, 0.12)): Background tint of a selected row or active menu item, always paired with a yellow indicator bar. Never a large fill.
- Disabled primary buttons drop the yellow entirely: `{colors.surface-raised}` background with `{colors.faint}` text.

### Status (reserved: alerts, data quality, deltas)
Status colors always ship with an icon and a label, never color alone. They are never used as chart series.

| Token | Hex | On surface | Use |
|---|---|---|---|
| `{colors.positive}` | #0ECB81 | 7.4:1 | Check passed, data fresh, value inside the normal band |
| `{colors.caution}` | #F0884A | 6.3:1 | Stale data, thin liquidity, inside the tender window, regime shift |
| `{colors.negative}` | #FF5A4D | 5.2:1 | Failed check, fetch error, value outside the band |
| `{colors.info}` | #5B9DF5 | 5.7:1 | Neutral notices, methodology notes |

Each status also has a wash for chip backgrounds: the hex at 14% alpha (for example rgba(240, 136, 72, 0.14)).

**Price direction is not a status.** A premium of +79 bp is not "bad". Signed numbers stay in `{colors.ink}`; the sign (+ / −) and the word ("rich", "cheap") carry direction. Only use `{colors.positive}` / `{colors.negative}` for deltas where up is genuinely good or bad, such as "cheaper than a retail coin by ₹610/g".

### Data visualization
Validated with the dataviz palette checker against `{colors.surface}` and `{colors.canvas}`: lightness band, chroma floor, colorblind (CVD) separation ≥ 8 on adjacent pairs, normal-vision separation ≥ 15, and ≥ 3:1 contrast.

**Categorical, fixed per contract** (color follows the contract, never its rank or the filter):

| Slot | Token | Hex | Contract | Why |
|---|---|---|---|---|
| 1 | `{colors.series-1}` | #3987E5 (blue) | GOLDTEN | The reference contract |
| 2 | `{colors.series-2}` | #DB3B3B (red) | GOLDGUINEA | |
| 3 | `{colors.series-3}` | #199E70 (aqua) | GOLDPETAL | |
| 4 | `{colors.series-4}` | #9085E9 (violet) | GOLDM | Control pair |
| — | — | — | GOLD (if shown) | Folds to `{colors.muted}`, dashed, labelled |

- Slots 1–3 pass the all-pairs test (scatter plots, overlapping dots). Slot 4 passes only beside its neighbours, so a chart with all four contracts must be a line or bar chart **with direct labels**, never a scatter.
- The premium charts (GOLDGUINEA and GOLDPETAL over GOLDTEN) use slots 2 and 3, which pass every test.

**Diverging, premium heatmaps** (cheap ← parity → rich), validated as two ordinal arms:

| cheap-3 | cheap-2 | cheap-1 | parity | rich-1 | rich-2 | rich-3 |
|---|---|---|---|---|---|---|
| #8DB8F0 | #3987E5 | #2B5C99 | #343B45 | #9E3030 | #DB3B3B | #F5887E |

The midpoint is a cool neutral, never a hue. Bigger magnitude = brighter.

**Sequential, magnitude only** (₹ crore at risk, volume): blue, #184F95 → #256ABF → #3987E5 → #6DA7EC → #9EC5F4.

**Chart chrome:**
- Gridlines `{colors.hairline}`, 1px, horizontal only.
- Axis and zero/parity baseline `{colors.hairline-strong}`.
- Axis labels and tick values `{colors.muted}`, 12px, tabular figures.
- Values, labels and legends use text tokens, never the series color. A colored swatch or line beside the text carries identity.
- Lines 2px, markers ≥ 8px, bars with 4px rounded data ends and a 2px surface gap.
- Event markers (expiry, tender window, crash day) are vertical `{colors.hairline-strong}` dashed lines with a `{typography.caption}` label.

## Typography

### Font Family
**Inter** for everything (display, body, navigation, buttons, captions, numbers). **JetBrains Mono** for code, raw data views, and contract symbols inside dense tables. Fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` and `ui-monospace, "Cascadia Mono", Consolas, monospace`.

### Hierarchy

| Token | Size | Weight | Line Height | Letter Spacing | Color | Use |
|---|---|---|---|---|---|---|
| `{typography.display-xl}` | 64px | 700 | 1.05 | -2px | ink | Landing h1 only |
| `{typography.display-lg}` | 48px | 700 | 1.1 | -1.5px | ink | Page headline ("Small contracts trade 80–95 bp rich") |
| `{typography.display-md}` | 36px | 700 | 1.15 | -1px | ink | Section heads |
| `{typography.display-sm}` | 28px | 700 | 1.2 | -0.6px | ink | Card headline, chooser result |
| `{typography.title-lg}` | 22px | 700 | 1.3 | -0.3px | ink | Panel titles |
| `{typography.title-md}` | 18px | 600 | 1.4 | 0 | ink | Card titles |
| `{typography.title-sm}` | 15px | 600 | 1.4 | 0 | ink | Chart titles, list labels |
| `{typography.stat-display}` | 48px | 700 | 1.0 | -1.5px | **ink** | Headline numbers ("+94 bp", "₹10.3 Cr") |
| `{typography.stat-md}` | 28px | 700 | 1.1 | -0.6px | ink | Stat-tile values |
| `{typography.body-md}` | 16px | 400 | 1.6 | 0 | body | Running text |
| `{typography.body-sm}` | 14px | 400 | 1.55 | 0 | body | Card text, table cells |
| `{typography.caption}` | 13px | 500 | 1.4 | 0 | muted | Captions, "as of" stamps, chart sources |
| `{typography.caption-uppercase}` | 12px | 600 | 1.4 | 1.2px | muted | Section labels, table headers |
| `{typography.data}` | 14px | 500 | 1.4 | 0 | ink | Numbers in tables and tiles (tabular-nums) |
| `{typography.code}` | 13px | 400 | 1.6 | 0 | body | JetBrains Mono |
| `{typography.button}` | 14px | 600 | 1.0 | 0 | — | Button labels |
| `{typography.nav-link}` | 14px | 500 | 1.4 | 0 | muted → ink when active | Top-nav items |

### Principles
- Display weights stay at 700 with negative tracking. Hierarchy comes from size and weight, not from color.
- Stat numbers are **ink, not yellow**. Yellow text would read as a link and spend the accent on something unclickable.
- `font-variant-numeric: tabular-nums` on every table cell, axis tick, stat tile and input. Hero numbers that stand alone may use proportional figures.

### Number & unit formatting
| Thing | Format | Example |
|---|---|---|
| Basis points | Signed, no decimals unless < 10 | +79 bp · −2.6 bp |
| Rupees | Indian grouping, ₹ prefix | ₹1,48,206 · ₹14,820.6/g |
| Large rupees | Lakh / crore | ₹3.2 L · ₹10.3 Cr |
| Percent | One decimal | 8.3% |
| Confidence interval | Square brackets after the estimate | +79 bp [61, 97] |
| Dates | Day Mon Year | 23 Oct 2026 |
| Times | 24h, IST | 23:30 IST |
| Contracts | Uppercase symbol, then expiry | GOLDPETAL · Nov 2026 |
| Missing value | Em dash in `{colors.faint}` | — |

Every figure on screen has a source line or "as of" stamp nearby, in `{typography.caption}`.

## Layout

### Spacing System
- **Base unit:** 4px.
- **Tokens:** `{spacing.xxs}` 4px · `{spacing.xs}` 8px · `{spacing.sm}` 12px · `{spacing.md}` 16px · `{spacing.lg}` 24px · `{spacing.xl}` 32px · `{spacing.xxl}` 48px · `{spacing.section}` 96px.
- **App pages:** 24px page padding (16px on mobile), 24px between cards, 48px between page sections.
- **Landing / story page:** `{spacing.section}` (96px) between bands.
- **Card padding:** `{spacing.lg}` (24px) for chart and data cards; `{spacing.xl}` (32px) for editorial feature cards.

### Grid & Container
- **Max content width:** 1280px, centered.
- **App shell:** 56px top nav, then content. No sidebar for the MVP; page tabs live in the top nav.
- **Dashboard grid:** 12 columns, 24px gutters. Typical rows: 4 stat tiles (3 cols each); chart 8 + context 4; full-width table.
- **Chooser:** inputs 5 cols, result 7 cols; stacks on mobile with the result first.

### Whitespace Philosophy
Dense but calm. Tables and charts sit tight; the space goes between groups, not inside them.

## Elevation & Depth

| Level | Treatment | Use |
|---|---|---|
| 0 Canvas | `{colors.canvas}` | Page floor, inputs, code blocks |
| 1 Surface | `{colors.surface}` + 1px `{colors.hairline}` border | Cards, top nav, table header |
| 2 Raised | `{colors.surface-raised}` | Nested tiles, hover rows, menus, secondary buttons |
| 3 Overlay | `{colors.surface}` + 1px `{colors.hairline-strong}` + shadow 0 16px 48px rgba(0,0,0,0.5) | Modals, popovers, tooltips. The only shadows in the system. |

Depth comes from the three blacks, not from shadows.

## Shapes

### Border Radius Scale

| Token | Value | Use |
|---|---|---|
| `{rounded.xs}` | 4px | Chart bar ends, checkboxes, small chips |
| `{rounded.sm}` | 6px | Small buttons, segmented-control items, tooltips |
| `{rounded.md}` | 8px | Buttons, inputs, selects, stat tiles |
| `{rounded.lg}` | 12px | Cards, chart cards, modals |
| `{rounded.pill}` | 9999px | Tags, status chips, toggles |
| `{rounded.full}` | 50% | Notification dots, avatars, icon buttons |

## Interaction States

Every interactive component documents default, hover, pressed, focus-visible, disabled and (where it applies) selected.

- **Hover:** surfaces step up one level (canvas → surface → raised); yellow buttons go to `{colors.accent-hover}`.
- **Pressed:** yellow goes to `{colors.accent-pressed}`; neutral elements go back down one level.
- **Focus-visible:** 2px `{colors.accent}` ring with a 2px `{colors.canvas}` offset. Never removed, never replaced by color alone.
- **Disabled:** no yellow anywhere; `{colors.faint}` text, `{colors.surface-raised}` fill, `cursor: not-allowed`.
- **Selected:** yellow indicator (bar, fill or check) plus `{colors.ink}` text. The text never turns yellow.
- **Motion:** 120ms ease-out for hover and press, 200ms for panels and tooltips. Respect `prefers-reduced-motion`: no animation, instant changes.

## Components

### Navigation

**`top-nav`** — 56px, `{colors.surface}`, bottom `{colors.hairline}`. Left: Tola wordmark in `{colors.ink}` (700, 18px). Center-left: page tabs (Overview, Basis, Convergence, Verdict, Chooser, Calendar, Method) in `{typography.nav-link}`, `{colors.muted}`. Right: data "as of" stamp, alert bell with `{component.notification-dot}`.

**`nav-tab-active`** — Text `{colors.ink}`, 2px `{colors.accent}` bar on the bottom edge. The yellow bar is the active signal.

**`notification-dot`** — 8px `{colors.accent}` circle with a 2px `{colors.surface}` ring, top-right of the icon. Paired with a count or an aria-label.

### Buttons

**`button-primary`** — `{colors.accent}` background, `{colors.on-accent}` text, `{typography.button}`, 40px tall, padding 0 × 20px, `{rounded.md}`. One per view where possible.

**`button-secondary`** — `{colors.surface-raised}` background, `{colors.ink}` text, 1px `{colors.hairline-strong}` border.

**`button-ghost`** — Transparent, `{colors.body}` text; hover `{colors.surface-raised}`.

**`button-icon`** — 36 × 36 (44 × 44 hit area), ghost style.

**`text-link`** — `{colors.accent}`, underlined, short spans only ("Read the method", "Source"). Never a whole sentence.

### Cards & Containers

**`card`** — `{colors.surface}`, 1px `{colors.hairline}`, `{rounded.lg}`, padding 24px.

**`stat-tile`** — `{colors.surface-raised}` (inside a card) or `{colors.surface}` (on canvas). `{typography.caption-uppercase}` label, `{typography.stat-md}` value in `{colors.ink}`, one-line context in `{typography.caption}` (CI, "as of", or delta).

**`headline-stat`** — Transparent. `{typography.stat-display}` in `{colors.ink}` with a `{typography.body-sm}` explanation and a source line underneath.

**`chart-card`** — A card with: title (`{typography.title-sm}`), one-line takeaway in `{colors.body}`, legend (always present for ≥ 2 series), plot, source/"as of" caption, and a "View table" toggle. Hover shows a crosshair and tooltip.

**`callout-band`** — Replaces the old full-bleed yellow band. `{colors.surface}` card with a 3px `{colors.accent}` left edge, headline in `{colors.ink}` and a `{component.button-primary}`. Yellow never fills a large area.

**`disclaimer`** — `{typography.caption}` in `{colors.muted}` at the foot of every page: "Research prototype. Not investment advice."

### Data

**`data-table`** — Header row `{colors.surface}` with `{typography.caption-uppercase}` in `{colors.muted}`. Rows 40px, 1px `{colors.hairline}` dividers, `{typography.data}` tabular numbers right-aligned, text left-aligned. Hover row `{colors.surface-raised}`. Selected row `{colors.accent-wash}` with a 2px yellow left bar. Sortable headers show an arrow in `{colors.ink}` when active.

**`contract-chip`** — Contract symbol in `{colors.ink}` with an 8px series-color dot before it. The dot carries identity, the text stays ink.

**`premium-value`** — Signed bp in `{colors.ink}`, tabular, with "rich"/"cheap" in `{colors.muted}` after it. Optional CI in `{colors.muted}`.

**`code-block`** — `{colors.canvas}` background, 1px `{colors.hairline}`, `{rounded.md}`, JetBrains Mono 13px. Syntax: keywords `{colors.series-1}` light (#8DB8F0), strings #9AD1B5, numbers `{colors.ink}`, comments `{colors.faint}`.

### Inputs & Forms

**`text-input`** — `{colors.canvas}` background, 1px `{colors.control-border}`, `{colors.ink}` text, `{colors.muted}` placeholder, 40px tall, `{rounded.md}`. Focus: border `{colors.accent}` plus focus ring.

**`number-input`** — Text input with a unit suffix ("g", "lots", "days", "₹") in `{colors.muted}`, tabular numbers, right-aligned value.

**`select`** — Text-input shell with a chevron in `{colors.muted}`. Menu: overlay level, items 36px, hover `{colors.surface-raised}`, selected item has a yellow check.

**`segmented-control`** — `{colors.canvas}` track, 1px `{colors.hairline}`, items in `{colors.muted}`. Selected item: `{colors.surface-raised}` fill, `{colors.ink}` text, 2px `{colors.accent}` bottom bar.

**`toggle`** — 36 × 20 pill. Off: `{colors.surface-raised}` track, `{colors.control-border}` border, `{colors.muted}` knob. On: `{colors.accent}` track, `{colors.canvas}` knob. Always has a visible label ("Take delivery").

**`checkbox`** — 16px, `{rounded.xs}`, `{colors.control-border}`. Checked: `{colors.accent}` fill, `{colors.on-accent}` check.

**`slider`** — 4px `{colors.surface-raised}` track, `{colors.accent}` fill, 16px `{colors.ink}` thumb with a yellow ring on focus. The value shows in a number input beside it.

**`field-error`** — `{colors.negative}` icon + message in `{colors.body}` under the field; the border turns `{colors.negative}`.

### Tags, Chips & Feedback

**`tag-key`** — The 30% tag: `{colors.ink}` background, `{colors.on-ink}` text, `{typography.caption}` 600, `{rounded.pill}`. For the one key label in a view ("PRE-REGISTERED", "18/18 CYCLES").

**`tag-neutral`** — `{colors.surface-raised}` background, `{colors.body}` text, `{rounded.pill}`.

**`status-chip`** — Status wash background, status-color icon and dot, label in `{colors.ink}`. Example: caution icon + "Inside tender window".

**`alert-row`** — An entry in the in-app alert log: status icon, title in `{colors.ink}`, one-line detail in `{colors.body}`, timestamp in `{colors.muted}`. Unread rows carry a `{component.notification-dot}`. Quiet by default.

**`tooltip`** — Overlay level, `{rounded.sm}`, padding 8 × 12, `{typography.body-sm}`. Chart tooltips list each series with its swatch, values tabular.

**`empty-state`** / **`loading`** / **`stale-data`** — Empty: `{colors.muted}` text plus one ghost action. Loading: `{colors.surface-raised}` skeleton blocks, no spinners on charts. Stale: a caution status chip with the last good "as of" date, never silently old numbers.

### Calendar

**`calendar-cell`** — 7-column grid. Days in `{typography.data}`. Expiry day: `{colors.ink}` outline. Tender window: caution wash with a caution label. Today: yellow dot under the date.

### Footer

**`footer`** — `{colors.canvas}`, top `{colors.hairline}`, `{typography.body-sm}` in `{colors.muted}`: data sources, method link, licence, disclaimer.

## Do's and Don'ts

### Do
- Keep the 60/30/10 balance: blacks dominate, ink carries the words, yellow marks the actions.
- Use yellow only on things that respond to a click or keyboard, plus focus rings and notification dots.
- Put every number in tabular figures with a sign, unit and source nearby.
- Give every chart a one-line takeaway, a legend, direct labels (≤ 4 series) and a table view.
- Keep contract colors fixed across every page: GOLDTEN blue, GOLDGUINEA red, GOLDPETAL aqua, GOLDM violet.
- Show uncertainty: confidence intervals next to estimates, "as of" dates next to live numbers.

### Don't
- Don't put white or ink text on yellow, and don't add gradients or glows to the canvas. Black on yellow and flat color blocks are the signature.
- Don't use yellow for text longer than a short link, for headings, for stat numbers or for chart series.
- Don't fill large areas with yellow (no yellow bands, yellow cards or yellow table rows).
- Don't use pure white (#FFFFFF) or pure black (#000000) anywhere.
- Don't color price direction red/green. A premium is information, not a loss.
- Don't use status colors as chart series, or a series color as a status.
- Don't use dual-axis charts. Two scales → two charts.
- Don't use `{colors.faint}` for anything a user needs to read.
- Don't add drop shadows outside the overlay level.

## Responsive Behavior

### Breakpoints

| Name | Width | Key Changes |
|---|---|---|
| Mobile | < 768px | Nav tabs move into a menu; 16px page padding; stat tiles 2-up; charts full-width; tables scroll horizontally inside their card with the first column pinned; display-lg 48 → 32px |
| Tablet | 768–1024px | Stat tiles 2-up; chart + context stack; chooser stacks |
| Desktop | 1024–1440px | Full nav; 4-up stat tiles; 8 + 4 chart rows |
| Wide | > 1440px | Same as desktop; content capped at 1280px |

### Touch Targets
- Buttons and inputs at least 40px tall; icon buttons have a 44 × 44 hit area.
- Chart hover targets are larger than the marks (full-height column per x value).

### Collapsing Strategy
- The page never scrolls sideways; wide tables and code scroll inside their own container.
- Chart legends wrap above the plot; direct labels drop on mobile if they collide, the legend stays.

## Accessibility

- Text contrast: ink 13.4:1, body 8.4:1, muted 4.8:1 on `{colors.surface}`. All AA or better; ink and body are AAA.
- Yellow on canvas is 13.6:1, so short yellow links pass AA, but long yellow text is still banned for comfort.
- Control borders clear 3:1. Focus rings are always visible.
- Identity is never color-only: contract chips have text, charts have legends and labels, status has icons.
- Every chart has a table view and an accessible name summarizing the takeaway.
- Honor `prefers-reduced-motion`.

## Iteration Guide

1. Work on one component at a time and reference its key (`{component.chart-card}`, `{component.segmented-control}`).
2. Variants live as separate entries (`-active`, `-disabled`, `-focused`, `-selected`).
3. Use tokens everywhere, never inline hex. CSS variables mirror the token names (`--canvas`, `--ink`, `--accent`).
4. When in doubt about emphasis: bigger Inter 700 in ink before adding color.
5. Before adding yellow, ask "can the user act on this?" If not, it is ink.
6. New chart colors must pass the dataviz palette validator against `#1E2329` and `#0B0E11`.
7. The visual reference is `Design/design-system.html`. Update it when tokens change.

## Known Gaps

- Iconography is not chosen yet. Use one outline icon set (for example Lucide) at 16/20px in `{colors.muted}`, `{colors.ink}` when active.
- The Tola wordmark is typographic for now.
- Print and forced-colors modes are not specified beyond keeping text tokens.
- A fifth contract color (GOLD, the 1 kg contract) is deliberately not assigned. If it becomes a first-class series, re-run the palette validator.
