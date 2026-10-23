import { Board, Contract, Posted } from '../components/ui.jsx'
import { evidence } from '../lib/data.js'
import { bp, perGram } from '../lib/format.js'

const pctS = (v) => `${v.toFixed(2)}%`

export default function Verdict() {
  const d = evidence.delivery.filter((r) => r.entry === 'last pre-tender day')
  const wf = evidence.walk_forward.filter((r) => r.pair !== 'GOLDPETAL/GOLDGUINEA')
  return (
    <main className="page" id="main">
      <Board as="h1" title="Who can collect the premium" posted={<Posted asof={evidence.asof} label="Data to" />}
        note="Short the small contract, buy GOLDTEN, hold both into settlement and deliver coins. Headroom is what is left after the premium collected, making charges, bar resale, margin funding and costs, before buying the coins to deliver. Mean of 18 expired cycles.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead><tr><th>Deliver</th><th className="n">Headroom</th><th className="n">Coins must cost under</th><th className="n">Cheapest coin found</th><th className="n">Cycles that paid</th></tr></thead>
            <tbody>
              {d.map((r) => {
                const sym = r.pair.split('/')[0]
                return (
                  <tr key={r.pair}>
                    <td><Contract symbol={sym} expiry={null} showLot /></td>
                    <td className="n num">{perGram(r.headroom_inr_g)}</td>
                    <td className="n"><span className="rate-sm">{pctS(r.breakeven_coin_premium_pct)}</span><span className="dim"> over spot</span></td>
                    <td className="n num">{r.retail_coin_premium_pct.toFixed(1)}% over spot</td>
                    <td className="n num">{Math.round(r.retail_profitable_share * r.cycles)} of {r.cycles}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </Board>

      <p className="lede">
        <strong>Only a coin maker can collect it.</strong> The premium is the market price of small gold, set near what it costs to make 1 g and 8 g coins.
        A trader can't arbitrage it away, but can avoid paying it: hold GOLDTEN or GOLDM unless you need under 10 g.
      </p>

      <Board title="Trading the premium before tender" posted="Out of sample, net of costs, 200 g a leg"
        note="Drift: short the premium 60+ days out, exit before tender. Swing: trade the premium's moves around its last 20–60 days, with the setting re-chosen each month from trades already closed. 95% intervals resample whole cycles. Jan–Mar 2026 was the premium's spike and collapse.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead><tr><th>Pair</th><th>Rule</th><th className="n">Trades</th><th className="n">Net a trade</th><th className="n hide-sm">95% interval</th><th className="n">Without Jan–Mar 2026</th></tr></thead>
            <tbody>
              {wf.map((r) => (
                <tr key={r.pair + r.strategy}>
                  <td><Contract symbol={r.pair.split('/')[0]} expiry={null} /></td>
                  <td>{r.strategy === 'DRIFT' ? 'Drift' : 'Swing (walk-forward)'}</td>
                  <td className="n num">{r.trades}</td>
                  <td className="n"><span className="rate-sm">{bp(r.mean_net_bp)}</span></td>
                  <td className="n num hide-sm">[{r.ci_lo_bp.toFixed(0)}, {r.ci_hi_bp.toFixed(0)}]</td>
                  <td className="n num">{bp(r.mean_net_bp_ex_crash)} <span className="dim">({r.trades_ex_crash})</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Board>

      <section className="two">
        <div className="prose">
          <h2 className="section-h">A small edge in the swings, mostly in a crisis</h2>
          <p>Holding the premium's level earns nothing reliable: it doesn't fade before tender. Trading its swings earned about <strong>+5 to +15 bp a trade</strong> in the current contract era outside January–March 2026, positive in all 26 settings that traded. About 90% of the profit came from that one quarter.</p>
        </div>
        <div className="prose">
          <h2 className="section-h">What we assumed</h2>
          <p>Fills at the next day's VWAP, one tick of slippage per order (results survive ten), statutory charges from a published broker schedule, a GST-registered deliverer, a 0.25% bar resale discount and ₹10/g logistics. A forward test is frozen and runs to 20 November.</p>
        </div>
      </section>
    </main>
  )
}
