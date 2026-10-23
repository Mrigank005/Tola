---
name: Tola
description: The fair-price desk for MCX gold, set as a posted bullion rate board.
colors:
  canvas: "#0B0E11"
  surface: "#1E2329"
  raised: "#2B3139"
  row-focus: "#232A31"
  hairline: "#2B3139"
  hairline-strong: "#3E4651"
  control: "#707A8A"
  ink: "#EAECEF"
  body: "#B7BDC6"
  muted: "#848E9C"
  faint: "#6A7383"
  on-accent: "#0B0E11"
  accent: "#F0B90B"
  accent-hover: "#FFD84D"
  accent-pressed: "#D9A300"
  positive: "#0ECB81"
  caution: "#F0884A"
  negative: "#FF5A4D"
  info: "#5B9DF5"
  series-goldten: "#3987E5"
  series-goldguinea: "#DB3B3B"
  series-goldpetal: "#199E70"
  series-goldm: "#9085E9"
  series-gold: "#848E9C"
typography:
  rate:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "32px"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.4px"
    fontFeature: "tnum"
    fontVariation: "'wdth' 82"
  headline:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "27px"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "-0.3px"
  title:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "20px"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "-0.3px"
  figure:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "17px"
    fontWeight: 600
    fontFeature: "tnum"
  lede:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.55
  body:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "15px"
    fontWeight: 400
    lineHeight: 1.55
  caption:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "13px"
    fontWeight: 400
  label:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    letterSpacing: "0.08em"
  nav:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "14px"
    fontWeight: 500
  button:
    fontFamily: "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
    fontSize: "14px"
    fontWeight: 600
  code:
    fontFamily: "'JetBrains Mono', ui-monospace, 'Cascadia Mono', Consolas, monospace"
    fontSize: "15px"
    fontWeight: 600
rounded:
  xs: "4px"
  sm: "6px"
  md: "8px"
  lg: "12px"
  pill: "999px"
spacing:
  page-x: "32px"
  page-x-sm: "16px"
  stack: "32px"
  gutter: "24px"
  board-x: "28px"
  control-gap: "16px"
  row-y: "16px"
  cell-x: "12px"
components:
  button-primary:
    backgroundColor: "{colors.accent}"
    textColor: "{colors.on-accent}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: "0 20px"
    height: "42px"
  button-primary-hover:
    backgroundColor: "{colors.accent-hover}"
    textColor: "{colors.on-accent}"
  button-primary-active:
    backgroundColor: "{colors.accent-pressed}"
    textColor: "{colors.on-accent}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.body}"
    typography: "{typography.button}"
    rounded: "{rounded.md}"
    padding: "0 20px"
    height: "42px"
  button-ghost-hover:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.ink}"
  input:
    backgroundColor: "{colors.canvas}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0 14px"
    height: "42px"
  segment:
    backgroundColor: "transparent"
    textColor: "{colors.muted}"
    typography: "{typography.nav}"
    rounded: "{rounded.sm}"
    padding: "0 14px"
    height: "34px"
  segment-selected:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.ink}"
  nav-bar:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    height: "56px"
  nav-tab:
    textColor: "{colors.muted}"
    typography: "{typography.nav}"
    padding: "0 12px"
  nav-tab-active:
    textColor: "{colors.ink}"
  board:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.body}"
    rounded: "{rounded.lg}"
    padding: "22px 28px 18px"
  quote-row-open:
    backgroundColor: "{colors.row-focus}"
    textColor: "{colors.ink}"
  chip-neutral:
    backgroundColor: "{colors.raised}"
    textColor: "{colors.body}"
    rounded: "{rounded.pill}"
    padding: "0 10px 0 8px"
    height: "26px"
---

# Design System: Tola

## Overview

**Creative North Star: "The Posted Rate Board"**

Tola is set as the board every Zaveri Bazaar bullion dealer chalks up each morning: one posted price per gram for each contract, today's date stamped on it, and what you actually pay beside it. Every page leads with a ruled board on a near-black floor. Figures are large, condensed and right-aligned in fixed columns, so the eye runs down a column the way it runs down a jeweller's rate card. Everything else on the page (a lede, a note, a short log) sits below the board and answers to it.

The density is a trader's, not a dashboard's: tables sit tight, space goes between boards (32px), and nothing is decorated. Depth comes from three steps of black, never from shadow. Colour is scarce on purpose. Ink carries the numbers; Warm Gold appears only where a hand can press; the per-contract series colours appear only as a small dot or a chart line beside a contract's name. Price direction is told by a sign and a word, never by red or green.

The palette is pinned by the user from the teammate's gold-terminal document (`Design/Design-gold-terminal.md`, Colors section), and every colour name and role below agrees with it. The type and component layer is this build's: Archivo replaces Inter, and the board replaces that document's stat tiles, callout band and accent side bars, which the shipped app refuses.

**Key Characteristics:**
- A posted rate board leads every page: title, posted date stamp, ruled rows, a source note at its foot.
- One condensed 32px figure (₹ per gram) owns each row; all numerals are tabular and right-aligned.
- Premium size reads on one fixed magnitude ramp (0 to 160 bp) on every page.
- Row state is told by the form of the rule above it: solid live, dashed thin turnover, struck code in tender.
- Gold is only for what you press, the focus ring and the selected underline.
- Flat, dark only: canvas, surface, raised. No light theme.
- One authored motion: ranked quote rows resolve in rank order.

## Colors

A cool near-black floor, a charcoal board and steel rules, soft ink figures, and one warm gold kept for action.

### Primary
- **Warm Gold** (`{colors.accent}`): the press-here colour. Primary button fill, inline links, the active nav tab's 2px underline, the selected segment's 2px inset underline, the focus ring, text selection and the caret, and the ring around rank one in a ranked (pressable) quote board. Always carries Near-Black text (`{colors.on-accent}`), never white or ink.
- **Gold Lit** (`{colors.accent-hover}`): primary button and link hover.
- **Gold Pressed** (`{colors.accent-pressed}`): primary button active.

### Secondary
- **Contract series** (`{colors.series-goldten}` blue, `{colors.series-goldguinea}` red, `{colors.series-goldpetal}` aqua, `{colors.series-goldm}` violet, `{colors.series-gold}` slate): identity, fixed to the contract on every page, never to its rank. Shown as a 9px dot before the contract code, a legend swatch, or a 2px chart line. Text beside them stays ink.

### Tertiary
- **Status** (`{colors.positive}`, `{colors.caution}`, `{colors.negative}`, `{colors.info}`): data quality and notices only. Always an icon plus a label, on a 14% wash of the same hue in chips. Caution also strikes the code of a contract in its tender window. Never a chart series, never price direction.

### Neutral
- **Near-Black** (`{colors.canvas}`): the page floor, input wells and the segmented-control track.
- **Card Charcoal** (`{colors.surface}`): boards, the top nav, chart tooltips.
- **Raised Steel** (`{colors.raised}`): selected segment fill, ghost-button hover, the empty ramp track, neutral chips, skeletons.
- **Row Focus** (`{colors.row-focus}`): hover and open state of a quote row and its expanded detail; a half step between charcoal and steel.
- **Steel Hairline** (`{colors.hairline}`): row rules, board borders, the nav and footer edges, chart gridlines.
- **Strong Rule** (`{colors.hairline-strong}`): the rule under a board head, breakdown dividers, ghost-button and segment borders, chart axes and the parity line.
- **Control Border** (`{colors.control}`): input and select borders (clears 3:1 on canvas and surface) and the dashed rule of a thin-turnover row.
- **Soft Ink** (`{colors.ink}`): headings, posted rates, contract codes, figures that matter.
- **Body Slate** (`{colors.body}`): running text and ordinary table cells; the ramp fill.
- **Muted Slate** (`{colors.muted}`): column headers, posted stamps, notes, units, axis labels, rows stepped down behind an open quote.
- **Faint Slate** (`{colors.faint}`): the em dash for a missing value only.

### Named Rules
**The Press-Here Gold Rule.** If it is gold, it responds to a click or a key, or it is the focus ring or a selected underline. Never gold for a figure, a heading, a ramp, a chart series or a fill larger than a button.

**The Neutral Direction Rule.** A premium is information, not a loss. Signed values stay ink; "+" or "−" and the word carry direction. Red and green never mean up and down.

**The Contract Owns Its Colour Rule.** A contract's series colour is the same on every board and chart and travels as a dot or a line, never as the colour of its text.

## Typography

**Display Font:** Archivo (variable, width 75–100, weight 400–700), with -apple-system, Segoe UI, Roboto, sans-serif
**Body Font:** Archivo
**Label/Mono Font:** JetBrains Mono (500/600), with ui-monospace, Cascadia Mono, Consolas

**Character:** One grotesque does everything, and its width axis gives the posted rate its narrow, chalked-up stance without a second display face. The mono is a stamp, not a voice: it appears only on contract codes and source paths.

### Hierarchy
- **Rate** (700, 32px, line-height 1, width 82%, tabular): the posted ₹ per gram in a board row and "You pay" in a quote row, with a 15px/500 muted "/g" unit. 22px under 720px.
- **Headline** (700, 27px, 1.2): the title of a page's leading board (its h1).
- **Title** (700, 20px, 1.3): titles of following boards and of prose sections.
- **Figure** (600, 17px, tabular): secondary figures that must stand out in a cell or breakdown (break-even percentages, breakdown amounts).
- **Lede** (400, 17px, 1.55, max 70ch): the one-paragraph reading of the board under it; key phrases in ink at 600.
- **Body** (400, 15px, 1.55, max 68ch for prose): running text and table cells.
- **Caption** (400, 13px): posted stamps, board notes, units, timestamps, field labels (500).
- **Label** (600, 12px, 0.08em tracking, uppercase): table column headers only.
- **Code** (JetBrains Mono 600, 15px): contract codes in rows; 13px muted for source paths on Method.

### Named Rules
**The Posted Rate Rule.** The condensed 32px rate is the largest thing in a row and only rates wear it. Nothing on a page is set larger than the leading board's headline except those rates.

**The Mono Is A Stamp Rule.** JetBrains Mono is for contract codes and source file paths. Never for prose, headings or figures.

## Layout

A single centred column, max 1280px, with 32px side padding (16px under 720px) and 32px between stacked blocks. Each page is a vertical stack of boards, each led by the board that owns the page's figure; supporting text sits between boards as a 17px lede. Secondary content pairs in two equal columns (`two`, 24px gutter) or a 4:8 split for the chooser's inputs beside its result. Both collapse to one column at 1024px.

Inside a board the head and body share a 28px inset (16px on mobile). Table rows are 16px tall-padded with 12px cell gutters, and the first and last columns sit flush with the board's inset. The chooser docks as one row of controls (grams, hold days, exit or deliver, broker, Compare) on desktop, two columns under 1024px and one under 720px.

On mobile, columns marked secondary drop out of the rate tables and the ramp moves under the rate in the same cell; wide tables scroll inside their board, never the page. The nav tabs scroll sideways with a fade at the right edge; the as-of stamp hides under 1024px.

## Elevation & Depth

Flat. Depth is three steps of black: Near-Black floor, Card Charcoal boards with a 1px Steel Hairline border, Raised Steel for selected and nested things. The only shadow in the shipped app is the chart tooltip's (0 16px 48px rgba(0,0,0,0.5)), an overlay. The focus ring and the selected segment's underline are drawn with box-shadow but are strokes, not elevation.

### Shadow Vocabulary
- **Overlay** (`box-shadow: 0 16px 48px rgba(0,0,0,.5)`): chart tooltips only.

### Named Rules
**The Three Blacks Rule.** A surface lifts by stepping up one black, never by casting a shadow.

## Shapes

Boards are gently rounded (12px); buttons, inputs and the segmented track 8px; segment buttons and skeletons 6px; status chips are pills. Inside a board everything is ruled, not boxed: rows are separated by full-width 1px top rules, the board head by a stronger rule. The ramp is a 6px rounded bar. Contract dots and rank markers are circles. No side bars, no cards inside boards.

### Named Rules
**The Rule-Form State Rule.** A row's state is the form of its rule: solid for a live contract, dashed in Control Border for thin turnover (under ₹1 Cr today), and the contract code struck through in 1px caution for a contract in its tender window. State is never a coloured fill or a side bar.

## Components

### Buttons
Plain, confident, one per board.
- **Shape:** 8px corners, 42px tall, 20px side padding, 14px/600 label.
- **Primary:** Warm Gold fill, Near-Black text ("Compare contracts"). Hover Gold Lit, active Gold Pressed, 120ms colour transition.
- **Ghost:** transparent, Body Slate text, Strong Rule border; hover fills Raised Steel with ink text.
- **Focus:** 2px Near-Black gap then a 2px Warm Gold ring, on every focusable element.

### Chips
- **Style:** 26px pill, 13px/500 ink label after a 15px status icon in the status hue, on a 14% wash of that hue. Neutral variant on Raised Steel with Body Slate text.
- **State:** informational only; never a filter or toggle.

### Inputs / Fields
- **Style:** Near-Black well, 1px Control Border, 8px corners, 42px tall, 15px/500 ink tabular value right-aligned, with the unit ("grams", "trading days") in 13px muted inside the right edge. Label above in 13px/500 Body Slate.
- **Focus:** border turns Warm Gold plus the focus ring. Hover lifts the border to Body Slate.
- **Error:** border turns Negative; a 13px message with a Negative X icon sits under the field. The submit button disables.
- **Select:** same shell with a muted chevron.
- **Segmented control:** Near-Black track with a Strong Rule border and 3px inset; 34px buttons in muted text. Selected: Raised Steel fill, ink text and a 2px Warm Gold inset underline. Used for exit or deliver, chart or table, and notice filters.

### Navigation
- **Style:** sticky 56px Card Charcoal bar, Steel Hairline bottom edge. "Tola" wordmark at 18px/700 ink with a 12px muted tagline; page tabs at 14px/500 muted; the "MCX data to" stamp at the right.
- **States:** hover to Body Slate; current page in ink with a 2px Warm Gold bottom border.
- **Mobile:** the tabs scroll sideways with a right-edge fade and the current tab scrolls into view; the tagline and stamp hide.

### The Rate Board (signature)
The container every page leads with. Card Charcoal, 12px corners, Steel Hairline border. Its head carries the title (Headline or Title) on the left and the posted stamp on the right ("Posted **22 Oct 2026** · MCX close", date in ink at 600, the rest muted), above a Strong Rule. The body is a ruled table: uppercase 12px column headers, contract code in mono with its series dot and a muted expiry and lot line under it, the rate in condensed 32px ink, and every number right-aligned and tabular. A 13px muted note at the foot says where the numbers come from.

### The Magnitude Ramp (signature)
Premium size, drawn the same way everywhere: a 160px, 6px Raised Steel track that spans 0 to 160 bp, filled from the left in Body Slate to the premium's size (at least 1.5%), followed by the signed value in ink at 600. A negative premium is drawn hollow, as a 1.5px ink outline, so direction is told by form and sign, never by hue. The track shortens to 64px on mobile. The scale is fixed: never rescale a ramp to its own data.

### Quote Rows (chooser results)
A ranked board of what each contract costs. Each row leads with a 24px rank circle (rank one ringed in gold, the rest in Strong Rule) and is pressable: click, Enter or Space expands it in place to a breakdown (17px/600 figures over 13px muted labels, each under a Strong Rule) and a one-line comparison. While a row is open, the open row and its detail take Row Focus, and every other row steps down: its text to Muted Slate, its rate to Body Slate. The chevron turns 90° over 200ms. Contracts that cannot fill the request close the board as dashed rows with the reason.

**Motion:** the one authored motion in the system. When a quote arrives, ranked rows resolve in rank order, rising 6px and fading in over 260ms on cubic-bezier(0.16, 1, 0.3, 1), staggered 50ms per rank. Under reduced motion all transitions and animations are off.

### Notice Log
A ruled list: 13px muted date, a 16px status icon in its hue, then a 600 ink title over a 14px Body Slate line. Quiet by default; the count of quiet days is stated beside it.

### Charts
ECharts on SVG inside a board, always with a Chart / Table segmented switch so every value is readable without colour. Axes in Strong Rule, gridlines in Steel Hairline, labels 12px muted Archivo, 2px series lines in the contract's colour, a legend of short swatches; dashed lines mark reference series.

## Do's and Don'ts

### Do:
- **Do** lead every page with a rate board that carries a posted date stamp and a source note.
- **Do** set rates in Archivo 700 at 32px, width 82%, tabular, right-aligned, with a muted "/g".
- **Do** draw every premium on the fixed 0–160 bp ramp, hollow when negative.
- **Do** tell row state by rule form: solid live, dashed thin, struck code in tender.
- **Do** keep Warm Gold (#F0B90B) for things you press, the focus ring and the selected underline, with Near-Black text on it.
- **Do** give every status an icon and a label, and every chart a table view.
- **Do** step the other rows down to muted when one quote row is open, and expand it in place.
- **Do** turn all motion off under `prefers-reduced-motion`.

### Don't:
- **Don't** colour price direction red or green; sign and words carry it.
- **Don't** put a small uppercase eyebrow or kicker label above a heading; uppercase tracked type is for table column headers only.
- **Don't** mark a row, notice or callout with a coloured side bar (a left border thicker than 1px); state is told by rule form.
- **Don't** build hero-metric stat tiles or a big standalone number; a figure lives in a board row beside its contract.
- **Don't** use gold for figures, headings, ramps, chart series or large fills.
- **Don't** use JetBrains Mono for anything but contract codes and source paths.
- **Don't** add shadows outside the chart tooltip, or gradients to the floor.
- **Don't** rescale the magnitude ramp to fit a page's own data.
- **Don't** use pure white (#FFFFFF) or pure black (#000000).
