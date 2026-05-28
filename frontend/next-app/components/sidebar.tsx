import Link from 'next/link'
import { Briefcase, Bell, Cpu, LayoutDashboard, Settings, Sparkles } from 'lucide-react'

const navItems = [
  { label: 'Dashboard', icon: LayoutDashboard, href: '#dashboard' },
  { label: 'Tenders', icon: Briefcase, href: '#tenders' },
  { label: 'AI Analysis', icon: Cpu, href: '#analysis' },
  { label: 'Recommendations', icon: Sparkles, href: '#recommendations' },
  { label: 'Notifications', icon: Bell, href: '#notifications' },
  { label: 'Settings', icon: Settings, href: '#settings' },
]

export function Sidebar() {
  return (
    <aside className="sticky top-6 flex h-[calc(100vh-3rem)] flex-col gap-6 rounded-[32px] border border-slate-200 bg-white p-6 shadow-sm">
      <div className="space-y-3">
        <div className="inline-flex items-center gap-3 rounded-3xl bg-blue-50 px-4 py-3 text-slate-900 ring-1 ring-slate-200">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-500 to-emerald-400 text-white shadow-sm">
            <svg viewBox="0 0 64 64" className="h-6 w-6" xmlns="http://www.w3.org/2000/svg">
              <path d="M8 24C12 12 25 6 32 8C39 6 52 12 56 24C48 20 40 18 32 26C24 18 16 20 8 24Z" fill="white" />
              <path d="M16 40C20 32 28 26 32 28C36 26 44 32 48 40C40 36 34 34 32 38C30 34 24 36 16 40Z" fill="white" />
              <path d="M28 46C30 42 34 42 36 46C38 50 34 58 32 62C30 58 26 50 28 46Z" fill="white" />
            </svg>
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.32em] text-slate-500">AI Tender Intel</p>
            <p className="font-semibold text-slate-900">TenderIQ</p>
          </div>
        </div>
        <p className="text-sm leading-6 text-slate-600">
          Centralize your tender discovery and recommendation engine with AI-driven insights.
        </p>
      </div>

      <nav className="flex flex-1 flex-col gap-2">
        {navItems.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className="group flex items-center gap-3 rounded-3xl border border-slate-200 bg-slate-50 px-4 py-3 text-sm text-slate-700 transition hover:border-blue-200 hover:bg-blue-50"
          >
            <item.icon className="h-5 w-5 text-slate-500 group-hover:text-blue-600" />
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="rounded-[28px] border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Tip</p>
        <p className="mt-3 leading-6">
          Use the AI Analysis section to validate eligibility and risk before preparing your response.
        </p>
      </div>
    </aside>
  )
}
