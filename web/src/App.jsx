import { lazy, Suspense, useEffect, useState } from 'react'
import { meta } from './lib/data.js'
import { date } from './lib/format.js'
import Landing from './pages/Landing.jsx'
import Rates from './pages/Rates.jsx'
import Choose from './pages/Choose.jsx'
// Chart pages load ECharts, so they load on demand.
const Basis = lazy(() => import('./pages/Basis.jsx'))
const Convergence = lazy(() => import('./pages/Convergence.jsx'))
import Verdict from './pages/Verdict.jsx'
import Alerts from './pages/Alerts.jsx'
import Method from './pages/Method.jsx'

const ROUTES = [
  ['/', 'Home', Landing], ['/choose', 'Choose', Choose], ['/rates', 'Rates', Rates], ['/basis', 'Why prices differ', Basis],
  ['/convergence', 'Convergence', Convergence], ['/verdict', 'Verdict', Verdict],
  ['/alerts', 'Notices', Alerts], ['/method', 'Method', Method],
]

function parse() {
  const h = window.location.hash.replace(/^#/, '') || '/'
  const [path, query = ''] = h.split('?')
  return { path: ROUTES.some(([p]) => p === path) ? path : '/', query }
}

export default function App() {
  const [route, setRoute] = useState(parse)
  useEffect(() => {
    const on = () => { setRoute(parse()); window.scrollTo(0, 0) }
    window.addEventListener('hashchange', on)
    return () => window.removeEventListener('hashchange', on)
  }, [])
  const go = (to) => { window.location.hash = to }
  const [, , Page] = ROUTES.find(([p]) => p === route.path)
  useEffect(() => {
    document.querySelector('.tab[aria-current="page"]')?.scrollIntoView({ block: 'nearest', inline: 'center' })
  }, [route.path])
  useEffect(() => {
    const name = ROUTES.find(([p]) => p === route.path)[1]
    document.title = route.path === '/' ? 'Tola · one gram of gold, five prices' : `${name} · Tola`
  }, [route.path])
  return (
    <>
      <a className="sr-only" href="#main">Skip to content</a>
      <header className="nav">
        <div className="nav-in">
          <a className="brand" href="#/">Tola <small>fair-price desk for MCX gold</small></a>
          <nav className="tabs" aria-label="Pages">
            {ROUTES.slice(1).map(([p, label]) => (
              <a key={p} className="tab" href={`#${p}`} aria-current={route.path === p ? 'page' : undefined}>{label}</a>
            ))}
          </nav>
          <span className="stamp">MCX data to <b>{date(meta.data_asof)}</b></span>
        </div>
      </header>
      <Suspense fallback={<main className="page" id="main" aria-busy="true"><div className="board" style={{ padding: 28 }}><div className="skeleton" style={{ width: '40%', height: 22 }} /><div className="skeleton" style={{ marginTop: 24, height: 260 }} /></div></main>}>
        <Page query={route.query} go={go} />
      </Suspense>
      <footer className={`foot${route.path === '/' ? ' foot-landing' : ''}`}>
        <span>Tola · team Numero Uno · Hack in Hills ’26, PS03</span>
        <span>Research prototype from public MCX data. Not investment advice.</span>
      </footer>
    </>
  )
}
