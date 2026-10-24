import { useEffect, useRef, useState } from 'react'

// Fades a block up the first time it scrolls into view. Without IntersectionObserver, or under
// prefers-reduced-motion (CSS), content is simply visible.
export function useInView(margin = '0px 0px -12% 0px') {
  const ref = useRef(null)
  const [inView, setInView] = useState(false)
  useEffect(() => {
    const el = ref.current
    if (!el || typeof IntersectionObserver === 'undefined') { setInView(true); return }
    const io = new IntersectionObserver(([e]) => { if (e.isIntersecting) { setInView(true); io.disconnect() } }, { rootMargin: margin })
    io.observe(el)
    return () => io.disconnect()
  }, [margin])
  return [ref, inView]
}

export default function Reveal({ as: Tag = 'div', className = '', margin, children, ...rest }) {
  const [ref, inView] = useInView(margin)
  return <Tag ref={ref} className={`rv${inView ? ' in' : ''} ${className}`} {...rest}>{children}</Tag>
}
