# Tola web app

The fair-price desk for MCX gold: a static React + Vite site. It has no server. Everything it shows is read at build time from `web/data/*.json`. That folder is a committed copy of `../data/export/` (written by `python -m tola.refresh` or `python -m tola.export` from the data snapshot); `npm run dev`, `build` and `test` re-sync it first, so `web/` also builds on its own, with no files from outside the folder.

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
| `#/` | Landing: the product tour from data to decision (M1 to M5), with a working chooser strip and a link into every page. Figures are [Hairline](https://github.com/lucasmarkes/hairline) (MIT) | all exports |
| `#/rates` | Today's rate board | `chooser.json` |
| `#/choose?g=100&d=20&m=exit` | Which contract to hold, ranked by all-in ₹/g; rows expand to the cost breakdown | `chooser.json` |
| `#/basis` | Why prices differ: timing, carry, reference, premium; carry vs T-bill | `evidence.json` |
| `#/convergence` | The premium today vs history, by month, by days to expiry | `evidence.json` |
| `#/verdict` | Who can collect the premium; pre-tender trading results | `evidence.json` |
| `#/alerts` | Quiet notice log and contract calendar | `alerts.json`, `calendar.json` |
| `#/method` | Sources, checks, coverage, limits | `evidence.json`, `meta.json` |

`src/lib/chooser.js` is a line-for-line port of `tola/chooser.py`, including Python's half-to-even rounding for lot counts. `src/lib/chooser.test.js` checks it against the reference quotes in `golden.json`.

## Deploy (Vercel)

Import the repo, set **Root Directory** to `web`, framework **Vite**. Build command `npm run build`, output `dist`. Nothing outside `web/` is needed.

To update the site, run `python -m tola.refresh` on a laptop (MCX blocks cloud fetchers), commit `data/` and `web/data/` (run `npm run sync-data` in `web/` if you only ran `tola.export`), and push.

## Design

Palette: `Design/Design-gold-terminal.md`. Direction (the Zaveri Bazaar rate board) and system decisions: `DESIGN.md` and `PRODUCT.md`, produced with the [Impeccable](https://impeccable.style) skill. To use it here, install it with `npx skills add pbakaus/impeccable` (it is not committed).
