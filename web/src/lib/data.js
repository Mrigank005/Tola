// Everything the app shows comes from data/export/, written by `python -m tola.export`.
import chooser from '@data/chooser.json'
import alerts from '@data/alerts.json'
import calendar from '@data/calendar.json'
import evidence from '@data/evidence.json'
import meta from '@data/meta.json'

export { chooser, alerts, calendar, evidence, meta }

// The board shows each symbol's most liquid live contract.
export function boardContracts() {
  const best = new Map()
  for (const c of chooser.contracts) {
    const cur = best.get(c.symbol)
    if (!cur || (c.value_lakh ?? 0) > (cur.value_lakh ?? 0)) best.set(c.symbol, c)
  }
  const order = ['GOLD', 'GOLDM', 'GOLDTEN', 'GOLDGUINEA', 'GOLDPETAL']
  return order.map((s) => best.get(s)).filter(Boolean)
}
