import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { fileURLToPath } from 'node:url'

const repoRoot = fileURLToPath(new URL('..', import.meta.url))

// The app reads ../data/export/*.json (written by `python -m tola.export`) at build time.
export default defineConfig({
  plugins: [react()],
  resolve: { alias: { '@data': `${repoRoot}data/export` } },
  server: { fs: { allow: [repoRoot] } },
})
