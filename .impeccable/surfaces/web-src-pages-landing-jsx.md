---
version: 1
slug: "web-src-pages-landing-jsx"
primary_target: "web/src/pages/Landing.jsx"
related_targets: ["web/src/styles.css"]
---

# Tola landing page

Scope: `web/src/pages/Landing.jsx`, the new home route `#/`. Mode: Persuade. The tool and evidence pages stay Operate surfaces; this page sells and explains the whole product to hackathon judges first, traders second.

Audience, job, proof: judges on a laptop or projector in a hall (dark UI, one glance to be impressed, then they click in to verify); traders who need the chooser. Every number on the page comes from `data/export/*.json`. The brief pins the structure (user, 24 Oct): a SaaS-style landing page that explains what Tola provides, how the data is obtained, and the process behind M1 to M5, with a strong hero, animated Hairline figures, and a call to action in every section pointing at the working page. Palette pinned to `Design/Design-gold-terminal.md`. No concept round was run: the user's brief decided the structure. Image generation is unavailable, so the build is code-led.

## Direction contract

THESIS: The landing page is the rate board enlarged into a product tour: a working board and chooser in the first viewport, then one posted board of evidence per stage of the pipeline. It refuses the SaaS template of a split hero with a badge row, three equal feature cards and a logo wall.

OWN-WORLD: Gold-terminal palette only (near-black #0B0E11 floor, charcoal #1E2329 boards, steel rules, ink figures, gold #F0B90B on what is pressable). Archivo set extended and heavy for headlines, condensed for posted rates, JetBrains Mono for contract codes. Hairline's isometric line figures drawn in neutral ink (never gold, never a series colour), standing on the canvas with no card around them.

STORY: In one viewport the visitor reads the claim ("One gram of gold, five prices"), sees today's real board and the chooser already working; scrolling shows the five stages from raw MCX files to a decision, each with its finding and a button into the working page; the judge ends knowing the problem is solved end to end and where to verify it.

FIRST VIEWPORT: Top nav with a gold "Open the chooser" button. Headline across the left at display scale with one line of explanation; the Terrain figure rises behind and to the right of it; across the bottom of the viewport a full-width posting strip: five contract rows with live rate and animated premium ramp, and above it the chooser's four inputs with the gold Compare button, which opens the Choose page with the answer.

FORM: Pinned by the user's brief, so no form seed was rolled (disclosed deviation: the structure was dictated, not drawn). Signature moves: a pointer-responsive isometric figure per stage; premium ramps that grow in when the board scrolls into view; a ruled pipeline index from Collect to Decide that scrolls to each stage.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
