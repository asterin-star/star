import React from 'react'
import ReactDOM from 'react-dom/client'
import { MiniKit } from '@worldcoin/minikit-js'
import App from './App.jsx'

// Inicializar MiniKit antes de renderizar
MiniKit.install()

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
