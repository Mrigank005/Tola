import { CheckCircle2, AlertTriangle } from 'lucide-react'
import { Board } from '../components/ui.jsx'
import { evidence, meta } from '../lib/data.js'
import { date } from '../lib/format.js'

const PASSED = {
  'futures.vwap_outside_range': 'Every traded day’s average price sits inside its high–low range, so lot sizes and quote units are right.',
  'futures.missing_days': 'Every contract has a row on every MCX trading day of its life.',
  'futures.ohlc_inconsistent': 'Open and close sit inside the day’s range on every traded row.',
  'settlement.close_differs_from_ddr': 'Rebuilt settlement prices equal MCX’s published ones on all 145 contracts checkable (expiries before Oct 2023).',
  'settlement.rebuilt': 'Settlement price rebuilt for every expired contract from MCX polled spot.',
  'convergence.same_reference_settles_apart': 'GOLDGUINEA and GOLDTEN settle within 0.5 bp per gram in all 18 cycles.',
  'anatomy.waterfall_identity': 'Timing + carry + reference + left over = the futures price, on every row.',
}
const SOURCES = [
  ['MCX daily bhavcopy and contract-wise history', 'mcxindia.com/market-data/bhavcopy'],
  ['MCX polled spot archive (the settlement reference)', 'mcxindia.com/market-data/spot-market-price'],
  ['MCX contract specifications, 15 versions', 'mcxindia.com/products/bullion/gold'],
  ['FBIL 3-month T-bill benchmark', 'fbil.org.in'],
  ['Brokerage and statutory charges (Zerodha schedule)', 'zerodha.com/charges'],
  ['Retail coin prices (Augmont 13 Oct 2026; five 1 g products 10 Jun 2026)', 'data/specs/costs.yaml'],
]

export default function Method() {
  const v = evidence.validation
  return (
    <main className="page" id="main">
      <Board as="h1" title="Where every number comes from" posted={<>Data to <b>{date(meta.data_asof)}</b> · built {date(meta.built_at)}</>}
        note="Tola reads only public MCX, FBIL and broker data. A maintainer refreshes it with one command; if any check fails, nothing is published. Prices are daily, not live.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead><tr><th>Source</th><th>Where</th></tr></thead>
            <tbody>{SOURCES.map(([a, b]) => <tr key={a}><td style={{ color: 'var(--ink)' }}>{a}</td><td className="mono dim" style={{ fontSize: 13 }}>{b}</td></tr>)}</tbody>
          </table>
        </div>
      </Board>

      <div className="two">
        <Board title="Checks that passed" posted={`${v.passed.length} checks, 0 errors`} className="checks-card">
          <div className="board-body check-scroll">
            <ul className="log">
              {v.passed.map((k) => (
                <li key={k} style={{ gridTemplateColumns: '20px minmax(0,1fr)' }}>
                  <CheckCircle2 size={16} style={{ color: 'var(--positive)' }} aria-hidden="true" />
                  <p>{PASSED[k] ?? k}</p>
                </li>
              ))}
            </ul>
          </div>
        </Board>
        <Board title="Coverage" posted={`${evidence.tables.futures_daily.toLocaleString('en-IN')} contract-days`}>
          <div className="board-body scroll-x">
            <table className="rates">
              <thead><tr><th>Symbol</th><th className="n">From</th><th className="n">Contracts</th></tr></thead>
              <tbody>{Object.entries(evidence.coverage).map(([s, c]) => <tr key={s}><td className="code">{s}</td><td className="n num">{date(c.first)}</td><td className="n num">{c.contracts}</td></tr>)}</tbody>
            </table>
          </div>
        </Board>
      </div>

      <section className="prose wide">
        <h2 className="section-h">Known limits</h2>
        <ul className="log limits">
          {[
            'Prices are daily closes (the last half-hour average), not intraday quotes or fills. Slippage is assumed at one tick per order.',
            'Settlement prices after September 2023 use the verified rule, but MCX publishes no value to check them against.',
            'Statutory charges follow a broker’s published schedule and are not yet checked against a contract note.',
            'Coin prices are two dated retail snapshots. Refiners’ fabrication costs aren’t public.',
            'Exit-by dates don’t know future MCX holidays, and some brokers close positions before the tender window.',
            `${Object.values(v.warnings).reduce((a, b) => a + b, 0)} data warnings are logged, all one-off events such as a Sunday Budget-day session and lockdown-era spot freezes.`,
          ].map((t) => (
            <li key={t} style={{ gridTemplateColumns: '20px minmax(0,1fr)' }}>
              <AlertTriangle size={16} style={{ color: 'var(--caution)' }} aria-hidden="true" /><p>{t}</p>
            </li>
          ))}
        </ul>
        <p className="caption" style={{ marginTop: 16 }}>Tola is a research prototype by team Numero Uno for Hack in Hills ’26 (PS03). It does not place trades and is not investment advice.</p>
      </section>
    </main>
  )
}
