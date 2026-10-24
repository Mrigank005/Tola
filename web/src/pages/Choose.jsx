import { ChooserForm, QuoteBoard, readParams } from '../components/Chooser.jsx'
import { Board, Posted } from '../components/ui.jsx'
import { chooser } from '../lib/data.js'

export default function Choose({ query, go }) {
  const p = readParams(query)
  const deliver = p.m === 'deliver'
  const title = deliver ? `Cheapest way to get ${p.g} g delivered` : `Cheapest way to hold ${p.g} g for ${p.d} trading days`
  return (
    <main className="page" id="main">
      <div className="split">
        <Board as="h1" title="Which contract should you hold?" posted="Whole lots only">
          <div className="board-body" style={{ padding: '20px 28px 26px' }}>
            <ChooserForm key={query} initial={p} onSubmit={({ g, d, m }) => go(`/choose?g=${g}&d=${d}&m=${m}`)} />
          </div>
        </Board>
        <Board title={title} posted={<Posted asof={chooser.asof} label="Prices" />}
          note={deliver
            ? 'Delivery cost: the premium you pay is lost at settlement, plus the making charge (₹30/g GOLDTEN, ₹25/g GOLDGUINEA, ₹100/g GOLDPETAL), 3% GST, margin funding and an assumed ₹10/g for vault, assay and transport.'
            : 'Exit before the tender window opens, or you may be marked for compulsory delivery. Some brokers close positions earlier; check yours. Exit-by dates do not know future MCX holidays.'}>
          <QuoteBoard key={query} params={p} />
        </Board>
      </div>
      <section className="prose">
        <h2 className="section-h">How the cost is worked out</h2>
        <p><strong>Trading:</strong> CTT, stamp duty, MCX and SEBI fees, GST, and brokerage at 0.03% or ₹20 per order, plus one tick of slippage. Charges follow Zerodha's published schedule, not yet checked against a contract note.</p>
        <p><strong>Premium change:</strong> the small contracts' premium over GOLDTEN drifts while you hold. We charge its average change over your holding period since April 2025, and show one standard deviation as risk. GOLDTEN, GOLDM and GOLD are the reference, so they carry none.</p>
        <p><strong>Carry:</strong> futures price in the cost of holding gold until settlement. Only carry above the T-bill rate is a cost, because your cash keeps earning until then.</p>
      </section>
    </main>
  )
}
