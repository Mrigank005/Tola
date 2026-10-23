import { describe, expect, it } from 'vitest'
import data from '@data/chooser.json'
import golden from '@data/golden.json'
import { addBusinessDays, quote, roundHalfEven } from './chooser.js'

describe('chooser port matches tola/chooser.py', () => {
  for (const c of golden.cases) {
    const r = c.request
    it(`${r.grams} g, ${r.hold_days} days, ${r.take_delivery ? 'delivery' : 'exit'}`, () => {
      const got = quote(r, data)
      const want = c.quotes
      expect(got.map((q) => [q.symbol, q.feasible, q.rank ?? null])).toEqual(want.map((q) => [q.symbol, q.feasible, q.rank ?? null]))
      for (const w of want.filter((q) => q.feasible)) {
        const g = got.find((q) => q.symbol === w.symbol)
        expect(g.lots).toBe(w.lots)
        expect(g.expiry).toBe(w.expiry)
        expect(g.total_inr_g).toBeCloseTo(w.total_inr_g, 4)
        expect(g.premium_risk_inr_g).toBeCloseTo(w.premium_risk_inr_g, 4)
        if (r.take_delivery && w.retail_coin_alt_inr_g != null) expect(g.retail_coin_alt_inr_g).toBeCloseTo(w.retail_coin_alt_inr_g, 4)
      }
    })
  }

  it('rounds lot ties to even like Python', () => {
    expect(roundHalfEven(12.5)).toBe(12)
    expect(roundHalfEven(13.5)).toBe(14)
    expect(roundHalfEven(2.4)).toBe(2)
  })

  it('counts business days like numpy busday_offset', () => {
    expect(addBusinessDays('2026-10-22', 20)).toBe('2026-11-19')
    expect(addBusinessDays('2026-10-24', 0)).toBe('2026-10-26')
  })
})
