import { Bell, Search, Sparkles, User } from 'lucide-react'
import { Button } from './ui/button'

export function Navbar() {
  return (
    <header className="flex flex-col gap-4 rounded-[32px] border border-slate-200 bg-white p-5 shadow-sm sm:flex-row sm:items-center sm:justify-between">
      <div className="space-y-2">
        <p className="text-sm uppercase tracking-[0.32em] text-slate-500">Overview</p>
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-500 to-emerald-400 text-white shadow-sm">
            <svg viewBox="0 0 64 64" className="h-6 w-6" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 24C12 12 25 6 32 8C39 6 52 12 56 24C48 20 40 18 32 26C24 18 16 20 8 24Z" fill="white" />
              <path d="M16 40C20 32 28 26 32 28C36 26 44 32 48 40C40 36 34 34 32 38C30 34 24 36 16 40Z" fill="white" />
              <path d="M28 46C30 42 34 42 36 46C38 50 34 58 32 62C30 58 26 50 28 46Z" fill="white" />
            </svg>
          </div>
          <div>
            <h1 className="text-3xl font-semibold text-slate-900">TenderIQ</h1>
            <span className="rounded-full bg-slate-100 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-600 ring-1 ring-slate-200">
              SaaS AI Suite
            </span>
          </div>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-3">
        <label className="relative block w-full max-w-sm text-slate-500 sm:max-w-xs">
          <Search className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-slate-400" />
          <input
            placeholder="Search tenders"
            className="w-full rounded-full border border-slate-200 bg-slate-50 py-3 pl-11 pr-4 text-sm text-slate-900 outline-none transition focus:border-blue-400/50 focus:ring-2 focus:ring-blue-400/15"
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
