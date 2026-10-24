import { ArrowDown, ArrowRight } from 'lucide-react'
import { ChooserForm, DEFAULTS } from '../components/Chooser.jsx'
import Figure from '../components/Figure.jsx'
import Reveal from '../components/Reveal.jsx'
import { Contract, Ramp } from '../components/ui.jsx'
import { quote } from '../lib/chooser.js'
import { alerts, boardContracts, calendar, chooser, evidence } from '../lib/data.js'
import { bp, date, monthYear, perGram } from '../lib/format.js'

const smooth = () => (window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth')
const jump = (id) => document.getElementById(id)?.scrollIntoView({ behavior: smooth(), block: 'start' })
const inr = (v) => `₹${Math.round(v).toLocaleString('en-IN')}`
const money = (v) => (v >= 1e7 ? `₹${(v / 1e7).toFixed(2)} Cr` : v >= 1e5 ? `₹${(v / 1e5).toFixed(1)} L` : inr(v))
const FINALE = '20 Nov' // Hack in Hills finale, a fixed fact rather than an export

function useFacts() {
  const s = Object.fromEntries(evidence.summary.map((r) => [r.pair, r]))
  const dl = Object.fromEntries(evidence.delivery.filter((r) => r.entry === 'last pre-tender day').map((r) => [r.pair.split('/')[0], r]))
  const board = boardContracts()
  const small = board.filter((c) => c.symbol === 'GOLDGUINEA' || c.symbol === 'GOLDPETAL')
  const peak = evidence.carry_monthly.reduce((a, b) => (b.carry_pa > a.carry_pa ? b : a))
  const q100 = quote({ grams: 100, hold_days: 20, take_delivery: false }, chooser).filter((q) => q.feasible)
  const q8 = quote({ grams: 8, hold_days: 20, take_delivery: true }, chooser).filter((q) => q.feasible)
  const nowSmall = evidence.live.filter((r) => ['GOLDGUINEA/GOLDTEN', 'GOLDPETAL/GOLDTEN'].includes(r.pair) && r.tdte > 20 && r.tdte < 40)
  const from = Object.values(evidence.coverage).map((c) => c.first).sort()[0]
  const a0 = new Date(alerts.summary.from), a1 = new Date(alerts.summary.to)
  return {
    s, dl, board, peak, q100, q8, from,
    contracts: Object.values(evidence.coverage).reduce((a, c) => a + c.contracts, 0),
    days: evidence.tables.futures_daily, polls: evidence.tables.spot_polls, expiries: evidence.tables.settlement,
    checks: evidence.validation.passed.length, specVersions: evidence.spec_versions, settle: evidence.settlement_check,
    smallLo: Math.min(...small.map((c) => c.residual_bp)), smallHi: Math.max(...small.map((c) => c.residual_bp)),
    nowLo: Math.min(...nowSmall.map((r) => r.premium_vwap_bp)), nowHi: Math.max(...nowSmall.map((r) => r.premium_vwap_bp)),
    months: Math.round((a1 - a0) / (30.44 * 86400000)),
  }
}

/* ---------- hero ---------- */
function Hero({ f, go }) {
  const gt = f.s['GOLDGUINEA/GOLDTEN']
  return (
    <section className="hero">
      <div className="hero-top">
        <div className="hero-copy">
          <h1>One gram of gold.<br />Five prices.</h1>
          <p>
            MCX lists gold in five contract sizes that should cost the same per gram. Today the 8 g and 1 g contracts post{' '}
            <strong>{bp(f.smallLo)} to {bp(f.smallHi)}</strong> over fair price, and have been positive in <strong>{gt.cycles} of {gt.cycles}</strong> cycles since {monthYear(gt.first_expiry)}.
            Tola shows why, who can profit from the gap, and which contract you should hold.
          </p>
          <div className="hero-links">
            <button type="button" className="btn btn-ghost" onClick={() => jump('pipeline')}>See how it works</button>
            <a className="btn btn-ghost" href="#/verdict">Read the verdict</a>
          </div>
        </div>
        <Figure name="terrain" className="hero-fig" label="Isometric pillars that rise around the pointer, standing for the five contracts" />
      </div>

      <div className="strip board" aria-label="Today's rates and chooser">
        <div className="strip-head">
          <h2>Which contract should you hold?</h2>
          <span className="posted">Snapshot of the MCX close on <b>{date(chooser.asof)}</b> · daily data, not live</span>
        </div>
        <ChooserForm slim compact initial={DEFAULTS} onSubmit={({ g, d, m }) => go(`/choose?g=${g}&d=${d}&m=${m}`)} />
        <ul className="strip-cells">
          {f.board.map((c) => (
            <li key={c.symbol}>
              <Contract symbol={c.symbol} expiry={null} />
              <span className="rate">₹{Math.round(c.close_g999).toLocaleString('en-IN')}<small>/g</small></span>
              <Ramp value={c.residual_bp} />
            </li>
          ))}
        </ul>
      </div>
    </section>
  )
}

/* ---------- the problem: why five boxes ---------- */
function Problem({ f }) {
  const lo = Math.log10(1e4), hi = Math.log10(2e7)
  return (
    <section className="band" id="problem">
      <Reveal className="problem">
        <div>
          <h2>Same metal, five boxes, and the small ones cost more per gram</h2>
          <p className="lede">
            MCX sells gold futures from 1 kg down to 1 g. Convert each to ₹ per gram of 999 gold and strip out what every contract shares: what is left should be about zero.
            For the big contracts it is. For the 8 g and 1 g contracts it is not.
          </p>
          <p className="lede">Small contracts let ordinary traders take part. They are also where the premium sits.</p>
        </div>
        <div className="lots board">
          <h3>What one lot costs</h3>
          <ul>
            {f.board.map((c) => {
              const v = c.lot_g * c.close_g999
              return (
                <li key={c.symbol}>
                  <Contract symbol={c.symbol} expiry={null} showLot />
                  <span className="lot-bar" aria-hidden="true"><i style={{ width: `${Math.max(4, ((Math.log10(v) - lo) / (hi - lo)) * 100)}%` }} /></span>
                  <b className="num">{money(v)}</b>
                </li>
              )
            })}
          </ul>
          <p className="caption">Lot size × today’s rate. The scale is logarithmic.</p>
        </div>
      </Reveal>
    </section>
  )
}

/* ---------- pipeline index ---------- */
const STAGES = [
  ['collect', 'Collect', 'MCX data, checked'],
  ['explain', 'Explain', 'Split every price'],
  ['converge', 'Converge', 'Track it to settlement'],
  ['test', 'Test', 'Can anyone collect it?'],
  ['decide', 'Decide', 'Pick the contract'],
  ['watch', 'Watch', 'Only when it matters'],
]
function Pipeline() {
  return (
    <section className="band" id="pipeline">
      <Reveal>
        <h2 className="band-h">From raw exchange files to a decision, in six stages</h2>
        <ol className="pipe">
          {STAGES.map(([id, name, line], i) => (
            <li key={id}>
              <button type="button" onClick={() => jump(id)}>
                <span className="n num">{i + 1}</span>
                <b>{name}<ArrowDown size={15} aria-hidden="true" /></b>
                <span>{line}</span>
              </button>
            </li>
          ))}
        </ol>
        <p className="caption pipe-note">The line drawings in each stage are illustrations of the idea, not charts. Hover or tap them.</p>
      </Reveal>
    </section>
  )
}

/* ---------- a stage ---------- */
function Stage({ id, title, lede, how, lead, facts, figure, figLabel, visual, cta, to, flip }) {
  return (
    <div className={`wrap${flip ? ' alt' : ''}`}>
      <section className="band stage" id={id}>
        <Reveal className="stage-in">
          <div className="stage-copy">
            <h2>{title}</h2>
            <p className="lede">{lede}</p>
            {lead}
            {how && <ol className="how">{how.map((t, i) => <li key={i}>{t}</li>)}</ol>}
            <ul className="facts">
              {facts.map(([n, t], i) => <li key={i}><b className="num">{n}</b><span>{t}</span></li>)}
            </ul>
            <div className="stage-cta">
              <a className="btn btn-primary" href={`#${to}`}>{cta}<ArrowRight size={16} aria-hidden="true" /></a>
            </div>
          </div>
          {visual ?? <Figure name={figure} label={figLabel} />}
        </Reveal>
      </section>
    </div>
  )
}

function MiniQuotes({ rows }) {
  return (
    <div className="mini board">
      <h3>100 g held for 20 trading days</h3>
      <ol>
        {rows.map((q) => (
          <li key={q.symbol}>
            <span className="rank">{q.rank}</span>
            <Contract symbol={q.symbol} expiry={null} />
            <span className="dim num">exit by {date(q.exit_by, { year: false })}</span>
            <span className="rate">₹{Math.round(q.total_inr_g)}<small>/g</small></span>
          </li>
        ))}
      </ol>
      <p className="caption">Live from the same calculation as the Choose page. All-in cost per gram, whole lots.</p>
    </div>
  )
}

/* ---------- what a product like this has to get right ---------- */
const checks = (f) => [
  ['Compare contracts that differ in size, unit and purity', `Every price converted to ₹ per gram at 999, with ${f.specVersions} versions of MCX’s own contract specs.`, '/basis', 'Why prices differ'],
  ['Separate carry from a real mispricing', 'A daily carry curve from the big contracts, set against the T-bill rate, so what is left is the premium.', '/basis', 'Why prices differ'],
  ['Know what each contract settles to', `MCX’s own polled spot for every contract (Ahmedabad or Mumbai), with settlement prices rebuilt for ${f.expiries} expiries.`, '/convergence', 'Convergence'],
  ['Test trading rules without fooling yourself', 'Next-day fills, real charges, out-of-sample walk-forward, overfitting-adjusted scores, a look-ahead test, and a forward test frozen for the finale.', '/verdict', 'Verdict'],
  ['Tell a trader what to do, quietly', `Notices fire only when a condition starts; ${alerts.summary.quiet_days} of ${alerts.summary.trading_days} trading days had none.`, '/alerts', 'Notices'],
  ['Respect the contract lifecycle', 'Tender windows, exit-by dates and settlement for every live contract.', '/alerts', 'Calendar'],
  ['Survive the data traps', 'Moved expiries, frozen holiday spot, month-first dates, no-trade rows: handled and listed.', '/method', 'Method'],
]

export default function Landing({ go }) {
  const f = useFacts()
  const gt = f.s['GOLDGUINEA/GOLDTEN'], pt = f.s['GOLDPETAL/GOLDTEN']
  const small = f.q100.filter((q) => q.symbol === 'GOLDPETAL' || q.symbol === 'GOLDGUINEA')
  const dG = f.dl.GOLDGUINEA, dP = f.dl.GOLDPETAL
  const del8 = f.q8[0]
  const smallMin = Math.min(...small.map((q) => q.total_inr_g)), smallMax = Math.max(...small.map((q) => q.total_inr_g))

  const compare = (
    <dl className="compare">
      {[['8 g coins · GOLDGUINEA', dG], ['1 g coins · GOLDPETAL', dP]].map(([label, d]) => (
        <div key={label}>
          <dt>{label}</dt>
          <dd>
            <b className="num">{d.breakeven_coin_premium_pct.toFixed(2)}%</b><span>over spot is the most a deliverer can pay and break even</span>
            <b className="num dim">{d.retail_coin_premium_pct}%</b><span>is the cheapest retail coin we found · 0 of {d.cycles} cycles paid</span>
          </dd>
        </div>
      ))}
    </dl>
  )

  return (
    <main id="main" className="landing">
      <Hero f={f} go={go} />
      <Problem f={f} />
      <Pipeline />

      <Stage id="collect" figure="cabinet" figLabel="A rack of drawers, standing for the data snapshot" to="/method" cta="See sources and checks"
        title={`The full MCX gold history since ${f.from.slice(0, 4)}, checked before you see it`}
        lede="MCX blocks ordinary scripts, so Tola fetches the exchange’s own files through a browser-grade connection, keeps every raw response, and rebuilds one snapshot with a single command. Nothing reaches the app unless every check passes."
        how={['Fetch daily bhavcopy, each contract’s full history and its polled spot price from MCX.', `Read ${f.specVersions} versions of MCX’s contract-spec PDFs for lot size, purity, tender window and making charge.`, 'Validate every row, then publish the snapshot. One failed check stops the build.']}
        facts={[
          [f.days.toLocaleString('en-IN'), `contract-days across ${f.contracts} contracts, plus ${f.polls.toLocaleString('en-IN')} polled-spot readings`],
          [`${f.checks} checks`, 'passed with 0 errors, from lot sizes to settlement prices'],
          [`${f.settle.matched} of ${f.settle.checked}`, 'rebuilt settlement prices match MCX’s published ones, where MCX published them'],
        ]} />

      <Stage id="explain" flip figure="exploded" figLabel="An app window in four layers, standing for the parts of a futures price" to="/basis" cta="See today’s breakdown"
        title="One price, split into the parts that explain it"
        lede="A futures price isn’t spot. We cut every contract-day into timing, carry and the settlement reference, so that what is left over is the small-lot premium and nothing else."
        facts={[
          [`${(f.peak.carry_pa * 100).toFixed(0)}% a year`, `implied carry at its ${monthYear(f.peak.month)} peak, against T-bills near ${f.peak.rf_pct.toFixed(1)}%`],
          ['±50 bp', 'swing from timing alone on half of all days: spot is polled at 5–6 pm, the close is an 11 pm average'],
          ['Not in the price', 'the making charge: GOLDTEN’s ₹30/g sits within a few bp of fair price'],
        ]} />

      <Stage id="converge" figure="branches" figLabel="A commit graph that branches off main and merges back, standing for the premium opening and closing" to="/convergence" cta="See the convergence"
        title="The premium shows up every cycle, then settlement removes it in one step"
        lede="We pair contracts with the same expiry and follow their gap per gram to the last trading day. GOLDGUINEA and GOLDTEN settle to the same price per gram, so the gap has to close, and it closes at settlement."
        facts={[
          [`${bp(gt.pooled_vwap_bp)} [${gt.ci_lo_bp.toFixed(0)}, ${gt.ci_hi_bp.toFixed(0)}]`, `GOLDGUINEA over GOLDTEN, positive in all ${gt.cycles} cycles`],
          [`${bp(pt.pooled_vwap_bp)} [${pt.ci_lo_bp.toFixed(0)}, ${pt.ci_hi_bp.toFixed(0)}]`, `GOLDPETAL over GOLDTEN, positive in all ${pt.cycles} cycles`],
          [`${perGram(gt.given_up_inr_g_mean)} · ${perGram(pt.given_up_inr_g_mean)}`, `what a holder gives up at settlement. Today: ${bp(f.nowLo)} to ${bp(f.nowHi)}, a fraction of the Jan–Mar 2026 peak`],
        ]} />

      <Stage id="test" flip figure="vault" figLabel="A vault door with a dial, standing for who can collect the premium" to="/verdict" cta="Read the verdict"
        title="Can anyone collect it? We tried three ways"
        lede="Holding into delivery, shorting the premium and exiting before tender, and trading its swings: each priced with real charges and next-day fills, and scored only on trades it had not trained on."
        lead={compare}
        facts={[
          ['+5 to +15 bp', 'a trade from the premium’s swings in the current contract era, mostly earned in one crisis quarter'],
          ['Only a coin maker', `can collect it. A forward test frozen for the ${FINALE} finale will keep checking`],
        ]} />

      <Stage id="decide" visual={<MiniQuotes rows={f.q100} />} to="/choose" cta="Open the chooser"
        title="From evidence to a decision: which contract, for how long"
        lede="Enter the grams, the holding period and whether you’ll take delivery. Tola ranks every contract by what you will actually pay per gram, and tells you the date to exit by."
        facts={[
          [`${inr(f.q100[0].total_inr_g)}/g`, `${f.q100[0].symbol} for 100 g held 20 days, against ${inr(smallMin)}–${inr(smallMax)}/g for the small contracts`],
          [`${inr(del8.total_inr_g)}/g`, `to get 8 g delivered through ${del8.symbol}, against about ${inr(del8.retail_coin_alt_inr_g)}/g to buy the coin`],
          ['Date to exit by', `shown for all ${calendar.contracts.length} live contracts`],
        ]} />

      <Stage id="watch" flip figure="slow" figLabel="Crates on a belt through a gate, standing for contracts approaching their tender window" to="/alerts" cta="See notices and calendar"
        title="Quiet by default: a notice only when something starts"
        lede="Most days nothing needs your attention, so Tola says nothing. It speaks when the premium moves beyond its normal range, when a contract nears its tender window, or when a pair that should agree doesn’t."
        facts={[
          [`${alerts.summary.quiet_days} of ${alerts.summary.trading_days}`, `trading days since ${date(alerts.summary.from)} had no notice`],
          [`${alerts.alerts.length} notices`, `in ${f.months} months: tender windows, premium swings, control-pair drifts, settlement gaps`],
        ]} />

      <section className="band" id="checks">
        <Reveal>
          <h2 className="band-h">What a gold-derivatives product has to get right, and where Tola does it</h2>
          <div className="board checks">
            <table className="rates">
              <thead><tr><th>The job</th><th className="hide-sm">How Tola does it</th><th className="n">See it</th></tr></thead>
              <tbody>
                {checks(f).map(([job, how, to, label]) => (
                  <tr key={job}>
                    <td className="job">{job}<span className="how-sm">{how}</span></td>
                    <td className="hide-sm">{how}</td>
                    <td className="n"><a href={`#${to}`}>{label}</a></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Reveal>
      </section>

      <section className="band close">
        <Reveal margin="0px">
          <h2>Which contract should you hold?</h2>
          <p className="lede">Answer it with your own quantity and holding period. Every figure links back to the evidence.</p>
          <div className="stage-cta">
            <a className="btn btn-primary" href="#/choose">Open the chooser<ArrowRight size={16} aria-hidden="true" /></a>
            <a className="btn btn-ghost" href="#/rates">Today’s rates</a>
            <a className="btn btn-ghost" href="#/method">Sources and limits</a>
          </div>
        </Reveal>
      </section>
    </main>
  )
}
