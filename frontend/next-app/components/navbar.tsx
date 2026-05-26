import { Bell, Search, Sparkles, User } from 'lucide-react'
import { Button } from './ui/button'

export function Navbar() {
  return (
    <header className="flex flex-col gap-4 rounded-[32px] border border-white/10 bg-slate-950/75 p-5 shadow-card backdrop-blur-xl sm:flex-row sm:items-center sm:justify-between">
      <div className="space-y-2">
        <p className="text-sm uppercase tracking-[0.32em] text-slate-500">Overview</p>
        <div className="flex flex-wrap items-center gap-3">
          <h1 className="text-3xl font-semibold text-white">Tender Intelligence</h1>
          <span className="rounded-full bg-white/5 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-300 ring-1 ring-white/10">
            SaaS AI Suite
          </span>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <label className="relative block w-full max-w-sm text-slate-300 sm:max-w-xs">
          <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-500" />
          <input
            placeholder="Search tenders"
            className="w-full rounded-full border border-white/10 bg-slate-950/80 py-3 pl-11 pr-4 text-sm text-slate-100 outline-none transition focus:border-blue-400/50 focus:ring-2 focus:ring-blue-400/15"
          />
        </label>
        <Button variant="ghost" className="gap-2 px-4 py-3 text-sm">
          <Bell className="h-4 w-4" /> Alerts
        </Button>
        <Button variant="ghost" className="gap-2 px-4 py-3 text-sm">
          <User className="h-4 w-4" /> Admin
        </Button>
      </div>
    </header>
  )
}
