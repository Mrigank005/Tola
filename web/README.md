# Tola web app

The fair-price desk for MCX gold: a static React + Vite site. It has no server. Everything it shows is read at build time from `../data/export/*.json`, which `python -m tola.refresh` (or `python -m tola.export`) writes from the committed data snapshot.

```bash
cd web
npm install
npm run dev       # http://localhost:5173
npm test          # the chooser port must reproduce data/export/golden.json
npm run build     # static files in web/dist/
```

## Pages

| Route | Page | Data |
|---|---|---|
| `#/` | Rates: today's rate board, the docked chooser, latest notices | `chooser.json`, `alerts.json` |
| `#/choose?g=100&d=20&m=exit` | Which contract to hold, ranked by all-in ₹/g; rows expand to the cost breakdown | `chooser.json` |
| `#/basis` | Why prices differ: timing, carry, reference, premium; carry vs T-bill | `evidence.json` |
| `#/convergence` | The premium today vs history, by month, by days to expiry | `evidence.json` |
| `#/verdict` | Who can collect the premium; pre-tender trading results | `evidence.json` |
| `#/alerts` | Quiet notice log and contract calendar | `alerts.json`, `calendar.json` |
| `#/method` | Sources, checks, coverage, limits | `evidence.json`, `meta.json` |

`src/lib/chooser.js` is a line-for-line port of `tola/chooser.py`, including Python's half-to-even rounding for lot counts. `src/lib/chooser.test.js` checks it against the reference quotes in `golden.json`.

## Deploy (Vercel)

Import the repo, set **Root Directory** to `web`, framework **Vite**, and keep "Include files outside the root directory" on, because the build reads `../data/export`. Build command `npm run build`, output `dist`.

To update the site, run `python -m tola.refresh` on a laptop (MCX blocks cloud fetchers), commit `data/`, and push.

## Design

Palette: `Design/Design-gold-terminal.md`. Direction (the Zaveri Bazaar rate board) and system decisions: `DESIGN.md` and `.impeccable/surfaces/web-src-app-jsx.md`, produced with the [Impeccable](https://impeccable.style) skill. To use it here, install it with `npx skills add pbakaus/impeccable` (it is not committed).
