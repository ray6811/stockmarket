import React, {useEffect, useState} from 'react'
import Login from './Login'

export default function App(){
  const [authenticated, setAuthenticated] = useState(false)
  const [checking, setChecking] = useState(true)
  const [dark, setDark] = useState(true)

  useEffect(()=>{
    async function verify(){
      const token = localStorage.getItem('token')
      if(!token){ setChecking(false); return }
      try{
        const API = process.env.REACT_APP_AUTH_URL || 'http://localhost:8000'
        console.debug('Verifying token with', `${API}/verify`)
        const resp = await fetch(`${API}/verify`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({token})})
        if(resp.ok){ setAuthenticated(true) }
      }catch(e){ console.warn('verify failed', e) }
      setChecking(false)
    }
    verify()
  },[])

  function onLogin(){
    setAuthenticated(true)
  }

  function logout(){
    localStorage.removeItem('token')
    setAuthenticated(false)
  }

  if(checking) return <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-indigo-900 to-slate-800 text-white">Checking auth...</div>

  if(!authenticated) return <Login onLogin={onLogin} />

  return (
    <div className={`min-h-screen p-6 ${dark? 'bg-slate-900 text-white' : 'bg-white text-slate-900'}`}>
      <div className="max-w-6xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-indigo-500 to-emerald-400 flex items-center justify-center shadow-md">
              <span className="font-bold">SG</span>
            </div>
            <div>
              <h1 className="text-2xl font-extrabold">Stock Game Changer</h1>
              <p className="text-sm text-slate-400">Real-time signals • Multi-timeframe • Clean insights</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button onClick={()=>setDark(d=>!d)} className="px-3 py-1 rounded bg-gray-800">Toggle Theme</button>
            <button onClick={logout} className="px-3 py-1 rounded bg-rose-600">Logout</button>
          </div>
        </header>

        <main>
          <section className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
            <div className="lg:col-span-2 p-4 rounded-lg vibe-gradient bg-opacity-10 border border-slate-700">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h2 className="text-xl font-semibold">LIVE: RELIANCE</h2>
                  <p className="text-sm text-slate-400">5m • NSE</p>
                </div>
                <div className="signal-badge">
                  <div className="px-3 py-1 rounded bg-emerald-500 text-black font-bold">BUY</div>
                  <div className="text-sm text-slate-400">Confidence 78%</div>
                </div>
              </div>

              <div className="h-56 bg-gradient-to-b from-slate-800 to-slate-900 rounded-md flex items-center justify-center">
                <div className="text-slate-500">Chart placeholder (chart.js / tradingview)</div>
              </div>
            </div>

            <aside className="p-4 rounded-lg bg-gradient-to-br from-slate-800 to-slate-900 border border-slate-700">
              <h3 className="font-semibold mb-2">Indicators</h3>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>RSI(14): <span className="font-semibold">32.4</span></li>
                <li>MA50: <span className="font-semibold">3,420.6</span></li>
                <li>MA200: <span className="font-semibold">3,102.1</span></li>
                <li>Support: <span className="font-semibold">3,380</span></li>
                <li>Resistance: <span className="font-semibold">3,480</span></li>
              </ul>
            </aside>
          </section>

          <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 rounded-lg bg-gradient-to-br from-emerald-900 to-emerald-800">
              <h4 className="font-bold">Portfolio Impact</h4>
              <p className="text-sm text-slate-200">Projected +2.8% if signal follows</p>
            </div>
            <div className="p-4 rounded-lg bg-gradient-to-br from-indigo-900 to-indigo-800">
              <h4 className="font-bold">Backtest</h4>
              <p className="text-sm text-slate-200">Last 6 months: Profit 12.4%</p>
            </div>
            <div className="p-4 rounded-lg bg-gradient-to-br from-rose-900 to-rose-800">
              <h4 className="font-bold">Alerts</h4>
              <p className="text-sm text-slate-200">Telegram alerts active</p>
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}
