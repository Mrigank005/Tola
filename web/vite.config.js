import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'

const dataDir = fileURLToPath(new URL('./data', import.meta.url))

// The app reads web/data/*.json at build time: a copy of ../data/export (see scripts/sync-data.mjs), so web/ builds on its own.
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@data': dataDir } },
})
