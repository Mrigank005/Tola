// Port of tola/chooser.py `quote()`: effective cost per gram of holding gold through each live MCX contract.
// Inputs come from data/export/chooser.json; data/export/golden.json holds reference answers this must reproduce.

// Python's round(): ties go to the even integer (12.5 -> 12), unlike Math.round.
export function roundHalfEven(x) {
  const f = Math.floor(x)
  const d = x - f
  if (Math.abs(d - 0.5) < 1e-12) return f % 2 === 0 ? f : f + 1
  return Math.round(x)
}

const DAY = 86400000
const toDate = (s) => new Date(`${s}T00:00:00Z`)
const iso = (d) => d.toISOString().slice(0, 10)

// numpy busday_offset(date, n, roll="forward") for Monday-Friday business days, n >= 0
export function addBusinessDays(isoDate, n) {
  let d = toDate(isoDate)
  const isWeekend = (x) => x.getUTCDay() === 0 || x.getUTCDay() === 6
  while (isWeekend(d)) d = new Date(d.getTime() + DAY)
  let left = n
  while (left > 0) {
    d = new Date(d.getTime() + DAY)
    if (!isWeekend(d)) left -= 1
  }
  return iso(d)
}

const daysBetween = (a, b) => Math.round((toDate(b) - toDate(a)) / DAY)

export function orderCost(costs, valueInr, side, units, broker = 'zerodha', slippageTicks = null) {
  const st = costs.statutory
  const br = costs.brokers[broker]
  const ticks = slippageTicks ?? costs.slippage_ticks_base
  const brokerage = Math.min((br.pct / 100) * valueInr, br.cap_inr)
  const exchange = (st.exchange_txn_pct / 100) * valueInr
  const sebi = (st.sebi_inr_per_crore * valueInr) / 1e7
  const gst = (st.gst_pct_on_fees / 100) * (brokerage + exchange + sebi)
  const tax = side === 'sell' ? (st.ctt_sell_pct / 100) * valueInr : (st.stamp_buy_pct / 100) * valueInr
  const slippage = ticks * costs.tick_inr_per_quote_unit * units
  return { brokerage, exchange, sebi, gst, tax, slippage, total: brokerage + exchange + sebi + gst + tax + slippage }
}

// np.interp over the measured horizons; 0 for symbols without premium history (the reference contracts)
function changeStats(changes, symbol, h) {
  const c = changes.filter((r) => r.symbol === symbol).sort((a, b) => a.horizon - b.horizon)
  if (!c.length) return [0, 0]
  const interp = (key) => {
    if (h <= c[0].horizon) return c[0][key]
    if (h >= c[c.length - 1].horizon) return c[c.length - 1][key]
    for (let i = 1; i < c.length; i++) {
      if (h <= c[i].horizon) {
        const t = (h - c[i - 1].horizon) / (c[i].horizon - c[i - 1].horizon)
        return c[i - 1][key] + t * (c[i][key] - c[i - 1][key])
      }
    }
    return 0
  }
  return [interp('mean_bp'), interp('sd_bp')]
}

/**
 * req: { grams, hold_days, take_delivery, broker = 'zerodha', slippage_ticks = null }
 * data: the parsed chooser.json
 * Returns feasible quotes ranked by total ₹/g, then the infeasible ones with a reason.
 */
export function quote(req, data) {
  const { contracts, premium_changes: changes, costs, delivery: dlv, constants, asof } = data
  const broker = req.broker ?? 'zerodha'
  const slip = req.slippage_ticks ?? null
  const bySymbol = new Map()
  for (const c of contracts) {
    if (!bySymbol.has(c.symbol)) bySymbol.set(c.symbol, [])
    bySymbol.get(c.symbol).push(c)
  }
  const symbols = [...bySymbol.keys()].sort()
  const rows = []
  for (const sym of symbols) {
    const g = bySymbol.get(sym)
    const need = req.take_delivery ? 'days_to_settle' : 'days_to_exit_by'
    const fits = g.filter((c) => c[need] >= req.hold_days).sort((a, b) => a.expiry.localeCompare(b.expiry))
    const base = { symbol: sym, lot_g: g[0].lot_g }
    if (!fits.length) {
      rows.push({ ...base, feasible: false, reason: 'no live expiry is far enough out for this holding period' })
      continue
    }
    const c = fits[0]
    const lots = roundHalfEven(req.grams / c.lot_g)
    const grams = lots * c.lot_g
    if (lots < 1 || Math.abs(grams - req.grams) / req.grams > constants.max_size_gap) {
      rows.push({ ...base, expiry: c.expiry, feasible: false, reason: `trades in ${c.lot_g} g lots; ${req.grams} g can't be matched within 10%` })
      continue
    }
    const price = c.close_g999
    const notional = grams * price
    const units = grams / c.quote_g
    const days = req.take_delivery ? c.days_to_settle : req.hold_days
    const end = req.take_delivery ? c.last_trading_day : addBusinessDays(asof, days)
    const calDays = daysBetween(asof, end)
    const netCarry = c.carry_pa - c.rf_pct / 100
    const lines = {
      trading: orderCost(costs, notional, 'buy', units, broker, slip).total,
      net_carry: (notional * netCarry * calDays) / 365,
    }
    let risk = 0
    if (req.take_delivery) {
      lines.premium = (notional * c.residual_bp) / 1e4
      lines.making_charge = (c.making_charge_inr_g ?? 0) * grams
      lines.gst = (constants.gst_pct / 100) * notional
      const tm = (c.tender_margin_pct ?? 8.34) / 100
      lines.margin_funding = (notional * (c.rf_pct / 100) * (tm * c.tender_days + (dlv.delivery_margin_pct / 100) * dlv.delivery_margin_days)) / 365
      lines.logistics = dlv.vault_assay_transport_inr_per_g * grams
    } else {
      lines.trading += orderCost(costs, notional, 'sell', units, broker, slip).total
      const [meanBp, sdBp] = changeStats(changes, sym, req.hold_days)
      lines.premium = (-notional * meanBp) / 1e4
      risk = (notional * sdBp) / 1e4
    }
    const total = Object.values(lines).reduce((a, b) => a + b, 0)
    const row = {
      ...base, expiry: c.expiry, feasible: true, reason: c.thin ? 'thin turnover today' : '',
      lots, grams, price_g999: price, notional_inr: notional, residual_bp: c.residual_bp,
      carry_pa: c.carry_pa, rf_pct: c.rf_pct, exit_by: req.take_delivery ? null : c.exit_by,
      tender_start: c.tender_start, settles: c.last_trading_day, days_held: days, calendar_days: calDays,
      lines, total_inr: total, total_inr_g: total / grams, total_bp: (1e4 * total) / notional,
      premium_risk_inr: risk, premium_risk_inr_g: risk / grams,
    }
    if (req.take_delivery) {
      const p = dlv.retail_coin_premium_pct[sym]
      row.retail_coin_alt_inr_g = p == null ? null : price * (p / 100 + constants.gst_pct / 100)
    }
    rows.push(row)
  }
  const ok = rows.filter((r) => r.feasible).sort((a, b) => a.total_inr_g - b.total_inr_g).map((r, i) => ({ ...r, rank: i + 1 }))
  return [...ok, ...rows.filter((r) => !r.feasible)]
}
