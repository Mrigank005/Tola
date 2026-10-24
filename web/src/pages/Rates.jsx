import { Board, Contract, Posted, Ramp } from '../components/ui.jsx'
import { boardContracts, chooser } from '../lib/data.js'
import { crore, date, perGram } from '../lib/format.js'

export default function Rates() {
  const rows = boardContracts()
  return (
    <main className="page" id="main">
      <Board as="h1" title="Gold per gram, by contract" posted={<Posted asof={chooser.asof} />}
        note="Rate: MCX close (the last half-hour’s average) in ₹ per gram of 999 gold. Fair price: the day’s Ahmedabad polled spot plus the timing and carry every contract shares. The premium is what is left.">
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
                  <td className="n hide-sm num">{date(c.exit_by, { year: false })}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Board>
      <p className="links">
        <a className="btn btn-primary" href="#/choose">Which contract should I hold?</a>
        <a className="btn btn-ghost" href="#/basis">Why the prices differ</a>
        <a className="btn btn-ghost" href="#/convergence">Where the premium goes</a>
      </p>
    </main>
  )
}
