import { AlertTriangle, Info, CalendarClock } from 'lucide-react'
import { useState } from 'react'
import { ChooserForm, DEFAULTS, QuoteBoard, readParams } from '../components/Chooser.jsx'
import { Board, Contract, Posted, Ramp } from '../components/ui.jsx'
import { alerts, boardContracts, chooser } from '../lib/data.js'
import { bp, crore, date, perGram } from '../lib/format.js'

const ICON = { swing: AlertTriangle, tender: CalendarClock, control: Info, settlement: AlertTriangle }
const TONE = { swing: 'var(--caution)', tender: 'var(--info)', control: 'var(--info)', settlement: 'var(--negative)' }

export default function Rates({ query }) {
  // A link like #/?g=100&d=20&m=exit opens with the ranked board already in place.
  const [asked, setAsked] = useState(() => (new URLSearchParams(query).has('g') ? readParams(query) : null))
  const rows = boardContracts()
  const small = rows.filter((r) => r.symbol === 'GOLDGUINEA' || r.symbol === 'GOLDPETAL')
  const lo = Math.min(...small.map((r) => r.residual_bp)), hi = Math.max(...small.map((r) => r.residual_bp))
  const latest = alerts.alerts.slice(0, 4)
  return (
    <main className="page" id="main">
      <Board as="h1" title="Gold per gram, by contract" posted={<Posted asof={chooser.asof} />}
        note="Rate: MCX close (the last half-hour's average price) converted to ₹ per gram of 999 gold. Fair price: the day's Ahmedabad polled spot plus the timing and carry every contract shares. What's left over is each contract's premium.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead>
              <tr><th>Contract</th><th className="n">Rate</th><th className="hide-sm">Over fair price</th><th className="n hide-sm">Fair price</th><th className="n hide-sm">Turnover today</th><th className="n hide-sm">Exit by</th></tr>
            </thead>
            <tbody>
              {rows.map((c) => (
                <tr key={c.symbol} className={[c.thin && 'thin', chooser.asof >= c.tender_start && 'tender'].filter(Boolean).join(' ')}>
                  <td><Contract symbol={c.symbol} expiry={c.expiry} showLot /></td>
                  <td className="n"><span className="rate">₹{Math.round(c.close_g999).toLocaleString('en-IN')}<small>/g</small></span><Ramp value={c.residual_bp} className="show-sm" /></td>
                  <td className="hide-sm"><Ramp value={c.residual_bp} /></td>
                  <td className="n hide-sm num">{perGram(c.fair_g999)}</td>
                  <td className="n hide-sm num">{crore(c.value_lakh)}</td>
                  <td className="n num hide-sm">{date(c.exit_by, { year: false })}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Board>

      <p className="lede">
        The 8 g and 1 g contracts post <strong>{bp(lo)} to {bp(hi)}</strong> over fair price today, and have done so in every cycle since April 2025.
        Settlement removes it in one step, so <strong>the cheaper contract depends on how much gold you want and how long you hold it.</strong>
      </p>

      <Board title="What would you pay?" posted="Whole lots, all-in, per gram">
        <ChooserForm compact initial={asked ?? DEFAULTS} onSubmit={setAsked} />
        {asked && (
          <div style={{ borderTop: '1px solid var(--hairline-strong)' }}>
            <QuoteBoard key={`${asked.g}-${asked.d}-${asked.m}`} params={asked} />
            <p className="board-note">Ranked by all-in cost per gram. <a href={`#/choose?g=${asked.g}&d=${asked.d}&m=${asked.m}`}>Open in the full chooser</a> for the cost notes.</p>
          </div>
        )}
      </Board>

      <div className="two">
        <section>
          <h2 className="section-h">Latest notices</h2>
          <ul className="log">
            {latest.map((a, i) => {
              const I = ICON[a.type]
              return (
                <li key={i}>
                  <time dateTime={a.date}>{date(a.date)}</time>
                  <I size={16} style={{ color: TONE[a.type] }} aria-hidden="true" />
                  <div><b>{a.title}</b><p>{a.detail}</p></div>
                </li>
              )
            })}
          </ul>
          <p className="caption" style={{ marginTop: 8 }}><a href="#/alerts">All {alerts.alerts.length} notices since Apr 2025</a> · {alerts.summary.quiet_days} of {alerts.summary.trading_days} trading days were quiet.</p>
        </section>
        <section className="prose">
          <h2 className="section-h">How these prices are explained</h2>
          <p>Every MCX gold contract settles to a polled spot price, and the small contracts settle to <strong>exactly GOLDTEN's price per gram</strong>, in all 18 cycles we checked. So the premium can't survive settlement.</p>
          <p>Collecting it means delivering coins bought for under 0.3% over spot (8 g) or 1.1% (1 g). The cheapest retail coins cost 3.6% and 5.5%. The premium is the price of small gold, not a free lunch.</p>
          <div className="links" style={{ marginTop: 14 }}>
            <a href="#/basis">Why prices differ</a><a href="#/convergence">How they converge</a><a href="#/verdict">Who can collect it</a>
          </div>
        </section>
      </div>
    </main>
  )
}
