// Keeps web/data/ (the copy the app is built from) identical to ../data/export/ (what `python -m tola.export` writes).
// When the repo root isn't available, as on a host that builds only the web/ folder, the committed copy is used as is.
import { cpSync, existsSync, readdirSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

const from = fileURLToPath(new URL('../../data/export/', import.meta.url))
const to = fileURLToPath(new URL('../data/', import.meta.url))

if (existsSync(from)) {
  cpSync(from, to, { recursive: true })
  console.log(`synced ${readdirSync(from).length} files from data/export into web/data`)
} else if (existsSync(to)) {
  console.log('data/export not found; building from the committed web/data')
} else {
  console.error('No data found: run `python -m tola.export` first.')
  process.exit(1)
}
