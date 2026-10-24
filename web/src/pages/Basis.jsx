import { useMemo } from 'react'
import Chart, { Legend } from '../components/Chart.jsx'
import { Board, Contract, Posted, Ramp } from '../components/ui.jsx'
import { evidence } from '../lib/data.js'
import { bp, monthYear, perGram, SERIES_HEX } from '../lib/format.js'

const ORDER = ['GOLD', 'GOLDM', 'GOLDTEN', 'GOLDGUINEA', 'GOLDPETAL']

export default function Basis() {
  const rows = ORDER.map((s) => evidence.waterfall_today.find((r) => r.symbol === s)).filter(Boolean)
  const carry = evidence.carry_monthly.filter((r) => r.month >= '2023-01')
  const option = useMemo(() => ({
    xAxis: { data: carry.map((r) => monthYear(r.month)) },
    yAxis: { axisLabel: { formatter: '{value}%', color: '#848E9C' } },
    tooltip: { valueFormatter: (v) => `${v.toFixed(1)}%` },
    series: [
      { name: 'Implied carry', type: 'line', data: carry.map((r) => +(r.carry_pa * 100).toFixed(2)), showSymbol: false, lineStyle: { width: 2, color: '#EAECEF' }, itemStyle: { color: '#EAECEF' } },
      { name: 'Risk-free (T-bill, repo before Oct 2025)', type: 'line', data: carry.map((r) => r.rf_pct), showSymbol: false, lineStyle: { width: 2, type: 'dashed', color: '#848E9C' }, itemStyle: { color: '#848E9C' } },
    ],
  }), [carry])
  const years = [...new Set(evidence.residual_by_year.map((r) => r.year))].sort()
  const res = (y, s) => evidence.residual_by_year.find((r) => r.year === y && r.symbol === s)?.residual_bp
  return (
    <main className="page" id="main">
      <Board as="h1" title="Why one gram has five prices" posted={<Posted asof={evidence.asof} />}
        note="Each row splits today's futures price, per gram at 999, into parts that add up exactly. Timing and carry are common to every contract that day; the reference is the spot each contract settles to; what is left over is the premium. The making charge is paid on top of settlement, so it is shown, not subtracted.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead><tr>
              <th>Contract</th><th className="n">Spot, Ahmedabad 999</th><th className="n">Timing</th><th className="n">Carry</th>
              <th className="n hide-sm">Settles to</th><th>Left over</th><th className="n">Futures</th><th className="n hide-sm">Making charge</th>
            </tr></thead>
            <tbody>
              {rows.map((r) => (
                <tr key={r.symbol}>
                  <td><Contract symbol={r.symbol} expiry={r.expiry} /></td>
                  <td className="n num">{perGram(r.ref_spot_g999)}</td>
                  <td className="n num">{bp(r.timing_bp)}</td>
                  <td className="n num">{bp(r.carry_bp)}</td>
                  <td className="n num hide-sm">{Math.abs(r.reference_bp) < 0.5 ? <span className="dim">Ahmedabad</span> : <>Mumbai {bp(r.reference_bp)}</>}</td>
                  <td><Ramp value={r.residual_bp} /></td>
                  <td className="n"><span className="rate-sm">{perGram(r.close_g999)}</span></td>
                  <td className="n num hide-sm">{r.making_charge_inr_g ? `₹${r.making_charge_inr_g}/g` : <span className="na">none</span>}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Board>

      <section className="two">
        <div className="prose">
          <h2 className="section-h">Timing is the biggest daily swing</h2>
          <p>MCX polls spot around 5–6 pm; the futures close is the 11:00–11:30 pm average. Gold moves in between, so every contract shares a timing term of <strong>±50 bp on half of all days</strong>. Comparing a futures price with spot without removing it is mostly noise.</p>
          <p style={{ marginTop: 10 }}>The <strong>making charge is not in the futures price</strong>: GOLDTEN carries ₹30/g (about 21 bp) yet sits within a few bp of fair price. GOLDGUINEA's charge is smaller, yet its premium is far larger.</p>
        </div>
        <div className="prose">
          <h2 className="section-h">Carry broke away from T-bills</h2>
          <p>From 2020 to 2024 gold futures carried 1.4–2.8 points <em>below</em> the risk-free rate. From October 2025 carry climbed, peaking at <strong>17% in January 2026</strong> against T-bills near 5.3%. Holding gold through futures has cost far more than cash since.</p>
        </div>
      </section>

      <Board title="Implied carry against the risk-free rate" posted="Monthly median, % a year">
        <div className="board-body" style={{ paddingBottom: 20 }}>
          <Chart option={option} label="Implied carry versus risk-free rate by month since January 2023"
            table={{
              legend: <Legend items={[['Implied carry', '#EAECEF'], ['Risk-free (T-bill; repo before Oct 2025)', '#848E9C', true]]} />,
              body: (
                <table className="rates"><thead><tr><th>Month</th><th className="n">Carry</th><th className="n">Risk-free</th></tr></thead>
                  <tbody>{carry.slice().reverse().map((r) => <tr key={r.month}><td>{monthYear(r.month)}</td><td className="n num">{(r.carry_pa * 100).toFixed(1)}%</td><td className="n num">{r.rf_pct.toFixed(2)}%</td></tr>)}</tbody></table>
              ),
            }} />
        </div>
      </Board>

      <Board title="Premium left over, by year" posted="Median bp over fair price, liquid days before tender"
        note="GOLDPETAL traded at a widening discount until the April 2025 contract, then flipped to a premium. The big contracts sit on their own curve, within a few bp, every year.">
        <div className="board-body scroll-x">
          <table className="rates">
            <thead><tr><th>Year</th>{ORDER.map((s) => <th key={s} className="n"><span className="dot" style={{ background: SERIES_HEX[s] }} />{s}</th>)}</tr></thead>
            <tbody>{years.map((y) => <tr key={y}><td className="num">{y}</td>{ORDER.map((s) => <td key={s} className="n num">{res(y, s) == null ? <span className="na">—</span> : bp(res(y, s))}</td>)}</tr>)}</tbody>
          </table>
        </div>
      </Board>
    </main>
  )
}
