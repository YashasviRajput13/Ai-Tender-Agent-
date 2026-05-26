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
    <aside className="sticky top-6 flex h-[calc(100vh-3rem)] flex-col gap-6 rounded-[32px] border border-white/10 bg-slate-950/80 p-6 shadow-card backdrop-blur-xl">
      <div className="space-y-3">
        <div className="inline-flex items-center gap-3 rounded-3xl bg-gradient-to-r from-blue-500/20 to-violet-500/10 px-4 py-3 text-white ring-1 ring-white/10">
          <div className="rounded-2xl bg-white/10 p-2">
            <Sparkles className="h-5 w-5 text-white" />
          </div>
          <div>
            <p className="text-xs uppercase tracking-[0.32em] text-slate-400">Agentic AI</p>
            <p className="font-semibold">Tender Intelligence</p>
          </div>
        </div>
        <p className="text-sm leading-6 text-slate-400">
          Centralize your tender discovery and recommendation engine with AI-driven insights.
        </p>
      </div>

      <nav className="flex flex-1 flex-col gap-2">
        {navItems.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className="group flex items-center gap-3 rounded-3xl border border-white/5 bg-white/5 px-4 py-3 text-sm text-slate-200 transition hover:border-blue-400/30 hover:bg-blue-500/10"
          >
            <item.icon className="h-5 w-5 text-slate-300 group-hover:text-white" />
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      <div className="rounded-[28px] border border-white/10 bg-slate-900/80 p-4 text-sm text-slate-400">
        <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Tip</p>
        <p className="mt-3 leading-6">
          Use the AI Analysis section to validate eligibility and risk before preparing your response.
        </p>
      </div>
    </aside>
  )
}
