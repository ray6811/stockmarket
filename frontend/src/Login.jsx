import React, {useState} from 'react'

export default function Login({onLogin}){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  async function submit(e){
    e.preventDefault()
    setError(null)
    try{
      const API = process.env.REACT_APP_AUTH_URL || 'http://localhost:8000'
      console.debug('Auth request to', `${API}/login`)
      const resp = await fetch(`${API}/login`, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify({username, password})
      })
      if(!resp.ok){
        const text = await resp.text().catch(()=>null)
        let message = 'Authentication failed'
        try{
          const j = text ? JSON.parse(text) : null
          message = j?.detail || j?.message || text || message
        }catch(_){
          message = text || message
        }
        throw new Error(message)
      }
      const data = await resp.json()
      localStorage.setItem('token', data.access_token)
      onLogin()
    }catch(err){
      setError(err.message || 'network error')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 to-indigo-900 text-white">
      <form onSubmit={submit} className="bg-gradient-to-b from-slate-800 to-slate-900 p-8 rounded-xl w-full max-w-md shadow-xl border border-slate-700" action="#">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-full bg-emerald-400 flex items-center justify-center text-black font-bold">SG</div>
          <h2 className="text-2xl font-extrabold">Stock Game Changer</h2>
        </div>
        {error && <div className="bg-red-600 p-2 mb-2 rounded">{error}</div>}
        <label className="block mb-2 text-sm text-slate-300">Username</label>
        <input value={username} onChange={e=>setUsername(e.target.value)} className="w-full p-3 mb-3 rounded bg-slate-800 border border-slate-700" />
        <label className="block mb-2 text-sm text-slate-300">Password</label>
        <input type="password" value={password} onChange={e=>setPassword(e.target.value)} className="w-full p-3 mb-4 rounded bg-slate-800 border border-slate-700" />
        <button type="submit" className="w-full bg-emerald-400 text-black font-semibold p-3 rounded">Sign in</button>
        <p className="text-xs text-slate-400 mt-3">Demo: <strong>admin</strong> / <strong>password</strong></p>
      </form>
    </div>
  )
}
