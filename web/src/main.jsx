import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'
import './landing.css'

// Scroll reveals only when the visitor hasn't asked for reduced motion.
if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) document.documentElement.classList.add('motion-ok')
import App from './App.jsx'

createRoot(document.getElementById('root')).render(<StrictMode><App /></StrictMode>)
