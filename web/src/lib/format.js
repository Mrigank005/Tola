// Number and date formats from the design system: Indian grouping, signed bp, "23 Oct 2026".
const inr0 = new Intl.NumberFormat('en-IN', { maximumFractionDigits: 0 })
const inr1 = new Intl.NumberFormat('en-IN', { minimumFractionDigits: 1, maximumFractionDigits: 1 })

export const rupees = (v, digits = 0) => (v == null ? '—' : `₹${(digits ? inr1 : inr0).format(v)}`)
export function perGram(v) {
  if (v == null || Number.isNaN(v)) return '—'
  const r = Math.round(v)
  return r === 0 ? '₹0/g' : `${r < 0 ? '−' : ''}₹${inr0.format(Math.abs(r))}/g`
}

export function crore(lakh) {
  if (lakh == null) return '—'
  const cr = lakh / 100
  return cr >= 100 ? `₹${inr0.format(cr)} Cr` : `₹${cr.toFixed(cr >= 10 ? 0 : 1)} Cr`
}

export function bp(v, { sign = true } = {}) {
  if (v == null || Number.isNaN(v)) return '—'
  const a = Math.abs(v)
  const s = a < 10 ? a.toFixed(1) : a.toFixed(0)
  if (s === '0' || s === '0.0') return '0 bp'
  return `${sign ? (v < 0 ? '−' : '+') : v < 0 ? '−' : ''}${s} bp`
}

export const pct = (v, d = 1) => (v == null ? '—' : `${v.toFixed(d)}%`)

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
export function date(iso, { year = true } = {}) {
  if (!iso) return '—'
  const [y, m, d] = iso.slice(0, 10).split('-').map(Number)
  return year ? `${d} ${MONTHS[m - 1]} ${y}` : `${d} ${MONTHS[m - 1]}`
}
export function monthYear(iso) {
  const [y, m] = iso.slice(0, 7).split('-').map(Number)
  return `${MONTHS[m - 1]} ${y}`
}

export const SERIES = {
  GOLDTEN: 'var(--s-goldten)', GOLDGUINEA: 'var(--s-goldguinea)', GOLDPETAL: 'var(--s-goldpetal)',
  GOLDM: 'var(--s-goldm)', GOLD: 'var(--s-gold)',
}
export const SERIES_HEX = { GOLDTEN: '#3987E5', GOLDGUINEA: '#DB3B3B', GOLDPETAL: '#199E70', GOLDM: '#9085E9', GOLD: '#848E9C' }
export const LOT = { GOLD: '1 kg', GOLDM: '100 g', GOLDTEN: '10 g', GOLDGUINEA: '8 g', GOLDPETAL: '1 g' }
