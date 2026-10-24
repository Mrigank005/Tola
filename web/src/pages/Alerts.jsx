import { useState } from 'react'
import { AlertTriangle, CalendarClock, Info, XCircle } from 'lucide-react'
import { Board, Contract, Posted } from '../components/ui.jsx'
import { alerts, calendar, chooser } from '../lib/data.js'
import { crore, date } from '../lib/format.js'

const TYPES = [
  ['all', 'All'], ['swing', 'Premium swings'], ['tender', 'Tender notices'], ['control', 'Control pair'], ['settlement', 'Settlement gaps'],
]
const ICON = { swing: [AlertTriangle, 'var(--caution)'], tender: [CalendarClock, 'var(--info)'], control: [Info, 'var(--info)'], settlement: [XCircle, 'var(--negative)'] }

export default function Alerts() {
  const [type, setType] = useState('all')
  const [shown, setShown] = useState(12)
  const list = alerts.alerts.filter((a) => type === 'all' || a.type === type)
  const s = alerts.summary
  const asof = alerts.asof
  return (
    <main className="page" id="main">
      <Board as="h1" title="Notices" posted={<Posted asof={asof} label="Logged to" />}
        note="A notice fires on the day a condition starts, not every day it stays true. Swing: the premium moves beyond 1.5 standard deviations of its last 40 days. Tender: a live contract is five trading days from its tender window. Control: GOLD and GOLDM drift more than 10 bp apart. Settlement: a same-reference pair settles more than 20 bp apart.">
        <div className="board-body" style={{ paddingTop: 18 }}>
          <div className="chart-tools">
            <p className="caption num">{s.quiet_days} of {s.trading_days} trading days since {date(s.from)} had no notice.</p>
            <div className="seg" role="group" aria-label="Filter notices">
              {TYPES.map(([k, l]) => (
                <button key={k} type="button" aria-pressed={type === k} onClick={() => { setType(k); setShown(12) }}>
                  {l}{k !== 'all' && <span className="dim num"> {s.by_type[k] ?? 0}</span>}
                </button>
              ))}
            </div>
          </div>
          {list.length ? (
            <ul className="log" style={{ marginTop: 12 }}>
              {list.slice(0, shown).map((a, i) => {
                const [I, c] = ICON[a.type]
                return (
                  <li key={i}>
                    <time dateTime={a.date}>{date(a.date)}</time>
                    <I size={16} style={{ color: c }} aria-hidden="true" />
                    <div><b>{a.title}</b><p>{a.detail}</p></div>
                  </li>
                )
              })}
            </ul>
          ) : <p className="prose" style={{ padding: '18px 0' }}>No notices of this kind since {date(s.from)}.</p>}
          {list.length > shown && <p style={{ padding: '14px 0 6px' }}><button type="button" className="btn btn-ghost" onClick={() => setShown(shown + 25)}>Show 25 more ({list.length - shown} older)</button></p>}
        </div>
      </Board>

      <Board title="Contract calendar" posted={`${calendar.contracts.length} live contracts`}
        note="Exit by: the last trading day before the tender window, counted on weekdays; future MCX holidays may move it earlier. Dashed rows didn't trade ₹1 Cr on the latest day; a struck code is already inside its tender window.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead><tr><th>Contract</th><th className="n">Exit by</th><th className="n">Tender opens</th><th className="n">Settles</th><th className="n hide-sm">Listed</th><th className="n hide-sm">Turnover</th></tr></thead>
            <tbody>
              {calendar.contracts.map((c) => (
                <tr key={c.symbol + c.expiry} className={[c.thin && 'thin', chooser.asof >= c.tender_start && 'tender'].filter(Boolean).join(' ')}>
                  <td><Contract symbol={c.symbol} expiry={null} /><span className="dim"> {date(c.expiry)}</span></td>
                  <td className="n num"><b style={{ color: 'var(--ink)', fontWeight: 600 }}>{date(c.exit_by)}</b></td>
                  <td className="n num">{date(c.tender_start)}</td>
                  <td className="n num">{date(c.last_trading_day)}</td>
                  <td className="n num hide-sm dim">{date(c.first_traded)}</td>
                  <td className="n num hide-sm">{c.value_lakh == null ? <span className="na">no trades</span> : crore(c.value_lakh)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Board>
    </main>
  )
}
