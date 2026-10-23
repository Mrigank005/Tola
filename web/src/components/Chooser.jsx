import { useMemo, useState } from 'react'
import { ChevronRight, XCircle } from 'lucide-react'
import { quote } from '../lib/chooser.js'
import { chooser } from '../lib/data.js'
import { date, LOT, perGram, rupees } from '../lib/format.js'
import { Contract, Chip } from './ui.jsx'

export const DEFAULTS = { g: 100, d: 20, m: 'exit' }
const LIMITS = { g: [1, 100000], d: [1, 120] }

export function readParams(search) {
  const p = new URLSearchParams(search)
  const n = (k) => Number(p.get(k) ?? DEFAULTS[k])
  return { g: n('g'), d: n('d'), m: p.get('m') === 'deliver' ? 'deliver' : 'exit' }
}

export function ChooserForm({ initial, onSubmit, compact = false }) {
  const [g, setG] = useState(String(initial.g))
  const [d, setD] = useState(String(initial.d))
  const [m, setM] = useState(initial.m)
  const gN = Number(g), dN = Number(d)
  const gBad = !Number.isFinite(gN) || gN < LIMITS.g[0] || gN > LIMITS.g[1]
  const dBad = !Number.isInteger(dN) || dN < LIMITS.d[0] || dN > LIMITS.d[1]
  const submit = (e) => { e.preventDefault(); if (!gBad && !dBad) onSubmit({ g: gN, d: dN, m }) }
  return (
    <form className={compact ? 'dock' : ''} onSubmit={submit} noValidate style={compact ? undefined : { display: 'grid', gap: 18 }}>
      <label className="field">
        <span>Gold you want</span>
        <span className="input-wrap">
          <input className="input" style={{ '--unit-w': '44px' }} inputMode="decimal" value={g} onChange={(e) => setG(e.target.value)} aria-invalid={gBad} aria-describedby="g-err" />
          <em>grams</em>
        </span>
        {gBad && <span className="err" id="g-err"><XCircle size={14} />Enter 1 to 1,00,000 grams.</span>}
      </label>
      <label className="field">
        <span>{m === 'deliver' ? 'Earliest settlement' : 'Hold for'}</span>
        <span className="input-wrap">
          <input className="input" style={{ '--unit-w': '84px' }} inputMode="numeric" value={d} onChange={(e) => setD(e.target.value)} aria-invalid={dBad} aria-describedby="d-err" />
          <em>trading days</em>
        </span>
        {dBad && <span className="err" id="d-err"><XCircle size={14} />Enter whole days, 1 to 120.</span>}
      </label>
      <div className="field">
        <span id="end-l">At the end</span>
        <div className="seg" role="group" aria-labelledby="end-l">
          <button type="button" aria-pressed={m === 'exit'} onClick={() => setM('exit')}>Exit before tender</button>
          <button type="button" aria-pressed={m === 'deliver'} onClick={() => setM('deliver')}>Take delivery</button>
        </div>
      </div>
      <label className="field">
        <span>Broker</span>
        <select className="select" defaultValue="zerodha" aria-describedby="broker-note">
          {Object.entries(chooser.costs.brokers).map(([k, b]) => <option key={k} value={k}>{b.label}</option>)}
        </select>
      </label>
      <button className="btn btn-primary" type="submit" disabled={gBad || dBad}>Compare contracts</button>
    </form>
  )
}

function Breakdown({ q, deliver }) {
  const L = q.lines
  const per = (v) => perGram(v / q.grams)
  const items = deliver
    ? [['Trading costs', L.trading], ['Premium paid (lost at settlement)', L.premium], ['Carry above T-bill', L.net_carry],
       ['Making charge', L.making_charge], ['GST 3%', L.gst], ['Margin funding', L.margin_funding], ['Vault, assay, transport', L.logistics]]
    : [['Trading costs, in and out', L.trading], ['Expected premium change', L.premium], ['Carry above T-bill', L.net_carry]]
  return (
    <>
      <div className="breakdown num">
        {items.map(([k, v]) => <div key={k}><b>{per(v)}</b><span>{k}</span></div>)}
        {!deliver && q.premium_risk_inr_g > 0.5 && <div><b>±{perGram(q.premium_risk_inr_g)}</b><span>Premium risk (1 sd, history since Apr 2025)</span></div>}
      </div>
      <p className="versus num">
        {deliver
          ? q.retail_coin_alt_inr_g != null
            ? <>Buying a {LOT[q.symbol]} coin instead costs about <b>{perGram(q.retail_coin_alt_inr_g)}</b> over spot (cheapest observed, incl. GST). Through {q.symbol} you pay <b>{perGram(q.total_inr_g)}</b>.</>
            : <>No retail coin comparison for {LOT[q.symbol]} bars. Settles {date(q.settles)}; tender opens {date(q.tender_start)}.</>
          : <>Carry is {(q.carry_pa * 100).toFixed(1)}% a year against a {q.rf_pct.toFixed(2)}% T-bill; only the excess is a cost, since your cash keeps earning until settlement. {q.lots} lot{q.lots > 1 ? 's' : ''} = {q.grams} g, {rupees(q.notional_inr)} notional.</>}
      </p>
    </>
  )
}

export function QuoteBoard({ params }) {
  const deliver = params.m === 'deliver'
  const rows = useMemo(() => quote({ grams: params.g, hold_days: params.d, take_delivery: deliver }, chooser), [params.g, params.d, deliver])
  const ok = rows.filter((r) => r.feasible)
  const no = rows.filter((r) => !r.feasible)
  const [open, setOpen] = useState(ok[0]?.symbol ?? null)
  const toggle = (s) => setOpen((o) => (o === s ? null : s))
  if (!ok.length) {
    return (
      <div className="board-body" style={{ padding: '20px 28px 24px' }}>
        <p className="prose"><strong>No contract fits {params.g} g {deliver ? 'for delivery' : `for ${params.d} trading days`}.</strong> Contracts trade in whole lots of 1 g, 8 g, 10 g, 100 g and 1 kg, and live expiries run about five months out. Try a multiple of 10 g, or a shorter holding period.</p>
      </div>
    )
  }
  return (
    <div className="board-body scroll-x">
      <table className={`rates quotes${open ? ' has-open' : ''}`}>
        <thead>
          <tr>
            <th>Contract</th><th className="hide-sm">Lots</th>
            <th>{deliver ? 'Settles' : 'Exit by'}</th><th className="hide-sm">Tender opens</th>
            <th className="n">You pay</th><th className="n hide-sm">{deliver ? 'All-in' : 'Risk'}</th><th className="hide-sm" aria-hidden="true" />
          </tr>
        </thead>
        <tbody>
          {ok.map((q) => {
            const isOpen = open === q.symbol
            return [
              <tr key={q.symbol} className={`q${isOpen ? ' open' : ''}${q.reason ? ' thin' : ''}`} style={{ '--i': q.rank - 1 }} tabIndex={0} aria-expanded={isOpen}
                  onClick={() => toggle(q.symbol)} onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle(q.symbol) } }}>
                <td><span className="lead"><span className="rank">{q.rank}</span><Contract symbol={q.symbol} expiry={q.expiry} /></span></td>
                <td className="hide-sm num">{q.lots} × {LOT[q.symbol]}</td>
                <td className="num">{date(deliver ? q.settles : q.exit_by, { year: false })}</td>
                <td className="hide-sm num dim">{date(q.tender_start, { year: false })}</td>
                <td className="n"><span className="rate">₹{Math.round(q.total_inr_g).toLocaleString('en-IN')}<small>/g</small></span></td>
                <td className="n hide-sm num">{deliver ? `${(q.total_bp / 100).toFixed(1)}%` : q.premium_risk_inr_g > 0.5 ? `±${perGram(q.premium_risk_inr_g)}` : <span className="dim">none</span>}</td>
                <td className="n hide-sm"><ChevronRight size={18} className="chev" aria-hidden="true" /></td>
              </tr>,
              isOpen && (
                <tr key={`${q.symbol}-d`} className="detail"><td colSpan={7}><Breakdown q={q} deliver={deliver} /></td></tr>
              ),
            ]
          })}
          {no.map((q) => (
            <tr key={q.symbol} className="thin">
              <td colSpan={7}><Contract symbol={q.symbol} expiry={q.expiry} /><span className="why">{q.reason[0].toUpperCase() + q.reason.slice(1)}.</span></td>
            </tr>
          ))}
        </tbody>
      </table>
      {ok.some((q) => q.reason) && <p className="caption" style={{ padding: '12px 0 0' }}><Chip tone="caution">Thin turnover</Chip> Dashed rows traded under ₹1 Cr today; fills may cost more than shown.</p>}
    </div>
  )
}
