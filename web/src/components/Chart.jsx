import { useEffect, useRef, useState } from 'react'
import * as echarts from 'echarts/core'
import { LineChart, BarChart } from 'echarts/charts'
import { GridComponent, TooltipComponent, MarkLineComponent, MarkAreaComponent } from 'echarts/components'
import { SVGRenderer } from 'echarts/renderers'

echarts.use([LineChart, BarChart, GridComponent, TooltipComponent, MarkLineComponent, MarkAreaComponent, SVGRenderer])

const AXIS = { axisLine: { lineStyle: { color: '#3E4651' } }, axisTick: { show: false }, axisLabel: { color: '#848E9C', fontSize: 12, fontFamily: 'Archivo' } }
export const baseOption = {
  backgroundColor: 'transparent',
  textStyle: { fontFamily: 'Archivo', color: '#B7BDC6' },
  grid: { left: 56, right: 40, top: 16, bottom: 32, containLabel: false },
  tooltip: {
    trigger: 'axis', backgroundColor: '#1E2329', borderColor: '#3E4651', borderWidth: 1,
    textStyle: { color: '#EAECEF', fontSize: 13, fontFamily: 'Archivo' },
    axisPointer: { type: 'line', lineStyle: { color: '#848E9C', width: 1 } },
    extraCssText: 'box-shadow: 0 16px 48px rgba(0,0,0,.5); border-radius: 6px;',
  },
  xAxis: { ...AXIS, type: 'category', boundaryGap: false },
  yAxis: { ...AXIS, type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: '#2B3139' } } },
}

// A chart always ships with a table view: identity is never colour-only, and every value is readable.
export default function Chart({ option, label, table, height = 340 }) {
  const ref = useRef(null)
  const [view, setView] = useState('chart')
  useEffect(() => {
    if (view !== 'chart' || !ref.current) return
    const c = echarts.init(ref.current, null, { renderer: 'svg' })
    c.setOption({ ...baseOption, ...option, xAxis: { ...baseOption.xAxis, ...option.xAxis }, yAxis: { ...baseOption.yAxis, ...option.yAxis } })
    const ro = new ResizeObserver(() => c.resize())
    ro.observe(ref.current)
    return () => { ro.disconnect(); c.dispose() }
  }, [option, view])
  return (
    <div>
      <div className="chart-tools" style={{ marginBottom: 8 }}>
        <div>{table?.legend}</div>
        <div className="seg" role="group" aria-label={`${label}: view`}>
          <button type="button" aria-pressed={view === 'chart'} onClick={() => setView('chart')}>Chart</button>
          <button type="button" aria-pressed={view === 'table'} onClick={() => setView('table')}>Table</button>
        </div>
      </div>
      {view === 'chart'
        ? <div ref={ref} className="chart" style={{ height }} role="img" aria-label={label} />
        : <div className="scroll-x" style={{ maxHeight: height + 40, overflowY: 'auto' }}>{table?.body}</div>}
    </div>
  )
}

export const Legend = ({ items }) => (
  <div className="legend">
    {items.map(([name, color, dashed]) => (
      <span key={name}><i style={{ background: dashed ? 'none' : color, borderTop: dashed ? `2px dashed ${color}` : 0 }} />{name}</span>
    ))}
  </div>
)
