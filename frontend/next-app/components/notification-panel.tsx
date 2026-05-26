'use client'

import { Bell, AlertTriangle, CalendarDays } from 'lucide-react'
import { Card } from './ui/card'
import { Badge } from './ui/badge'

interface NotificationItem {
  title: string
  description: string
  type: 'new' | 'deadline' | 'risk'
  time: string
}

interface NotificationPanelProps {
  items: NotificationItem[]
  compact?: boolean
}

const mapType = {
  new: { label: 'New Tender', icon: Bell, variant: 'info' },
  deadline: { label: 'Deadline', icon: CalendarDays, variant: 'warning' },
  risk: { label: 'Risk', icon: AlertTriangle, variant: 'danger' },
} as const

export function NotificationPanel({ items, compact = false }: NotificationPanelProps) {
  return (
    <Card className={compact ? 'space-y-4' : 'space-y-6'}>
      <div>
        <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Notification panel</p>
        <h2 className="mt-2 text-2xl font-semibold text-white">Latest alerts</h2>
      </div>

      <div className="space-y-4">
        {items.map((item) => {
          const meta = mapType[item.type]
          const Icon = meta.icon
          return (
            <div key={item.title} className="rounded-3xl border border-white/10 bg-slate-950/70 p-4 transition hover:border-blue-400/20 hover:bg-slate-900/80">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white/5 text-blue-400">
                    <Icon className="h-5 w-5" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-white">{item.title}</p>
                    <p className="mt-1 text-sm text-slate-400">{item.description}</p>
                  </div>
                </div>
                <Badge variant={meta.variant}>{meta.label}</Badge>
              </div>
              <p className="mt-4 text-xs uppercase tracking-[0.24em] text-slate-500">{item.time}</p>
            </div>
          )
        })}
      </div>
    </Card>
  )
}
