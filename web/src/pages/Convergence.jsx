import { useMemo } from 'react'
import Chart, { Legend } from '../components/Chart.jsx'
import { Board, Contract, Posted, Ramp } from '../components/ui.jsx'
import { evidence } from '../lib/data.js'
import { bp, date, monthYear, perGram, SERIES_HEX } from '../lib/format.js'

const PAIRS = ['GOLDGUINEA/GOLDTEN', 'GOLDPETAL/GOLDTEN']
const BUCKETS = ['60+', '40-59', '20-39', '10-19', '5-9']
function ord(p) {
  const n = Math.round(p * 100)
  const t = n % 100 >= 11 && n % 100 <= 13 ? 'th' : ({ 1: 'st', 2: 'nd', 3: 'rd' }[n % 10] ?? 'th')
  return `${n}${t}`
}

export default function Convergence() {
  const s = Object.fromEntries(evidence.summary.map((r) => [r.pair, r]))
  const live = evidence.live.filter((r) => PAIRS.includes(r.pair)).sort((a, b) => a.expiry.localeCompare(b.expiry) || a.pair.localeCompare(b.pair))
  const months = [...new Set(evidence.monthly.map((r) => r.month))].sort()
  const val = (pair, m) => evidence.monthly.find((r) => r.pair === pair && r.month === m)?.premium_vwap_bp ?? null
  const option = useMemo(() => ({
    xAxis: { data: months.map(monthYear) },
    yAxis: { axisLabel: { formatter: '{value} bp', color: '#848E9C' } },
    tooltip: { valueFormatter: (v) => (v == null ? '—' : `${v >= 0 ? '+' : '−'}${Math.abs(v).toFixed(0)} bp`) },
    series: PAIRS.map((p) => {
      const sym = p.split('/')[0]
      return { name: `${sym} over GOLDTEN`, type: 'line', data: months.map((m) => val(p, m)), showSymbol: true, symbolSize: 7,
        lineStyle: { width: 2, color: SERIES_HEX[sym] }, itemStyle: { color: SERIES_HEX[sym], borderColor: '#1E2329', borderWidth: 2 },
        markLine: p === PAIRS[0] ? { silent: true, symbol: 'none', lineStyle: { color: '#3E4651' }, label: { show: false }, data: [{ yAxis: 0 }] } : undefined }
    }),
  }), [months])
  const prof = (pair, b) => evidence.profile.find((r) => r.pair === pair && r.bucket === b)
  const g = s['GOLDGUINEA/GOLDTEN'], pt = s['GOLDPETAL/GOLDTEN'], ctl = s['GOLD/GOLDM']
  return (
    <main className="page" id="main">
      <Board as="h1" title="The premium today, against its own history" posted={<Posted asof={evidence.asof} />}
        note="Premium: the small contract's VWAP over GOLDTEN's, per gram, same expiry. Rank: where today's premium sits among the 16–18 expired cycles at the same number of days to expiry.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead><tr><th>Contract</th><th className="n hide-sm">Days left</th><th>Premium over GOLDTEN</th><th className="n">Same stage, past cycles</th><th className="n">Percentile</th><th className="n hide-sm">5-day change</th></tr></thead>
            <tbody>
              {live.map((r) => {
                const sym = r.pair.split('/')[0]
                return (
                  <tr key={r.pair + r.expiry} className={r.eligible ? '' : 'thin'}>
                    <td><Contract symbol={sym} expiry={r.expiry} /></td>
                    <td className="n num hide-sm">{r.tdte}</td>
                    <td><Ramp value={r.premium_vwap_bp} /></td>
                    <td className="n num">{bp(r.history_mean_bp)}</td>
                    <td className="n num">{r.history_pct_rank === 0 ? 'Lowest' : r.history_pct_rank === 1 ? 'Highest' : ord(r.history_pct_rank)}</td>
                    <td className="n num hide-sm">{bp(r.change_5d_bp)}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      </Board>

      <p className="lede wide">
        Over 18 expired cycles GOLDGUINEA ran <strong>{bp(g.pooled_vwap_bp)} [{g.ci_lo_bp.toFixed(0)}, {g.ci_hi_bp.toFixed(0)}]</strong> and GOLDPETAL <strong>{bp(pt.pooled_vwap_bp)} [{pt.ci_lo_bp.toFixed(0)}, {pt.ci_hi_bp.toFixed(0)}]</strong> over GOLDTEN, positive in every cycle.
        At settlement GOLDGUINEA and GOLDTEN land on the same price per gram (never more than {g.settlement_gap_bp_maxabs.toFixed(2)} bp apart), so holding into settlement gives up about <strong>{perGram(g.given_up_inr_g_mean)}</strong> on GOLDGUINEA and <strong>{perGram(pt.given_up_inr_g_mean)}</strong> on GOLDPETAL.
      </p>

      <Board title="The premium by month" posted="Monthly median of liquid days, bp">
        <div className="board-body" style={{ paddingBottom: 20 }}>
          <Chart option={option} label="Monthly median premium of GOLDGUINEA and GOLDPETAL over GOLDTEN since April 2025"
            table={{
              legend: <Legend items={PAIRS.map((p) => [`${p.split('/')[0]} over GOLDTEN`, SERIES_HEX[p.split('/')[0]]])} />,
              body: (
                <table className="rates"><thead><tr><th>Month</th>{PAIRS.map((p) => <th key={p} className="n">{p.split('/')[0]}</th>)}</tr></thead>
                  <tbody>{months.slice().reverse().map((m) => <tr key={m}><td>{monthYear(m)}</td>{PAIRS.map((p) => <td key={p} className="n num">{bp(val(p, m))}</td>)}</tr>)}</tbody></table>
              ),
            }} />
        </div>
      </Board>

      <div className="two">
        <Board title="It doesn't fade before tender" posted="Mean of 18 cycles, bp">
          <div className="board-body scroll-x">
            <table className="rates">
              <thead><tr><th>Trading days to expiry</th>{PAIRS.map((p) => <th key={p} className="n">{p.split('/')[0]}</th>)}</tr></thead>
              <tbody>{BUCKETS.map((b) => <tr key={b}><td className="num">{b}</td>{PAIRS.map((p) => <td key={p} className="n num">{bp(prof(p, b)?.mean_vwap_bp)}</td>)}</tr>)}</tbody>
            </table>
          </div>
        </Board>
        <section className="prose">
          <h2 className="section-h">The control pair moved in 2026</h2>
          <p>GOLD (1 kg) and GOLDM (100 g) settle to the same three-day average, so their gap should be zero. Over {ctl.cycles} cycles it averaged <strong>{bp(ctl.pooled_vwap_bp)}</strong>, but in 2026 GOLD has traded about 9 bp cheaper in all four expired cycles: the same lot-size gradient, one step up. Four cycles is an early signal, not a result.</p>
          <p style={{ marginTop: 10 }} className="caption">Settlement prices are rebuilt from MCX polled spot and match MCX's published values on all 145 contracts checkable before October 2023. Last cycle: {date(g.last_expiry)}.</p>
        </section>
      </div>
    </main>
  )
}
