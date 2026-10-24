import { lazy, Suspense } from 'react'

// Hairline's isometric line figures (MIT, @lucasmarkes/hairline). They answer the pointer, and play on their own
// until it arrives. Loaded on demand so the first paint doesn't wait for them.
const load = (name) => lazy(() => import('@lucasmarkes/hairline/react').then((m) => ({ default: m[name] })))
const FIGURES = {
  terrain: load('Terrain'), cabinet: load('Cabinet'), exploded: load('Exploded'),
  branches: load('Branches'), vault: load('Vault'), riffle: load('Riffle'), slow: load('Slow'),
}

export default function Figure({ name, label, caption, intensity = 0.6, className = '' }) {
  const F = FIGURES[name]
  return (
    <figure className={`fig ${className}`}>
      <Suspense fallback={<div className="fig-ph" aria-hidden="true" />}>
        <F play intensity={intensity} label={label} />
      </Suspense>
      {caption && <figcaption>{caption}</figcaption>}
    </figure>
  )
}
