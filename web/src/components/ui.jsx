import { AlertTriangle, CheckCircle2, Info, XCircle } from 'lucide-react'
import { bp, date, LOT, SERIES } from '../lib/format.js'

// Premium size on one fixed ramp everywhere: the track is 100 bp end to end; a negative premium is drawn hollow.
export const RAMP_FULL_BP = 100
export function Ramp({ value, label, className = '' }) {
  if (value == null) return <span className="na">—</span>
  const share = Math.min(1, Math.abs(value) / RAMP_FULL_BP)
  return (
    <span className={`ramp${value < 0 ? ' neg' : ''} ${className}`}>
      <span className="track" aria-hidden="true"><i style={{ width: `${Math.max(share * 100, 1.5)}%` }} /></span>
      <b>{label ?? bp(value)}</b>
    </span>
  )
}

export function Contract({ symbol, expiry, showLot = false }) {
  return (
    <span className="code">
      <span className="sym"><span className="dot" style={{ background: SERIES[symbol] }} aria-hidden="true" />{symbol}</span>
      {(expiry || showLot) && (
        <span className="exp">
          {expiry && <span>{date(expiry)} expiry</span>}
          {expiry && showLot && <span className="sep" aria-hidden="true"> · </span>}
          {showLot && <span>{LOT[symbol]} lot</span>}
        </span>
      )}
    </span>
  )
}

const ICON = { caution: AlertTriangle, positive: CheckCircle2, info: Info, negative: XCircle }
export function Chip({ tone = 'info', children }) {
  const I = ICON[tone]
  return (
    <span className={`chip ${tone}`}>
      {I && <I size={15} aria-hidden="true" />}
      {children}
    </span>
  )
}

export function Board({ title, as: H = 'h2', posted, note, children, actions }) {
  return (
    <section className="board">
      <header className="board-head">
        <H>{title}</H>
        <span className="posted">{posted}</span>
        {actions}
      </header>
      {children}
      {note && <p className="board-note">{note}</p>}
    </section>
  )
}

export const Posted = ({ asof, label = 'Posted' }) => (
  <>
    {label} <b>{date(asof)}</b> · MCX close
  </>
)
