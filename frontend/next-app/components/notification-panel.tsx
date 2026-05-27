'use client'

import { Bell, AlertTriangle, CalendarDays, Sparkles, type LucideIcon } from 'lucide-react'
import { Card } from './ui/card'
import { Badge } from './ui/badge'

type NotificationType = 'new' | 'deadline' | 'risk' | 'high_match'

interface NotificationItem {
  title?: string
  description?: string
  type?: NotificationType | string
  time?: string
}

interface NotificationPanelProps {
  items: NotificationItem[]
  compact?: boolean
}

interface NotificationMeta {
  label: string
  icon: LucideIcon
  variant: 'default' | 'info' | 'warning' | 'danger'
}

const notificationMeta: Record<NotificationType, NotificationMeta> = {
  new: { label: 'New Tender', icon: Bell, variant: 'info' },
  deadline: { label: 'Deadline', icon: CalendarDays, variant: 'warning' },
  risk: { label: 'Risk', icon: AlertTriangle, variant: 'danger' },
  high_match: { label: 'High Match', icon: Sparkles, variant: 'info' },
}

const fallbackNotificationMeta: NotificationMeta = {
  label: 'Notification',
  icon: Bell,
  variant: 'default',
}

export function NotificationPanel({ items, compact = false }: NotificationPanelProps) {
  return (
    <Card className={compact ? 'space-y-4' : 'space-y-6'}>
      <div>
        <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Notification panel</p>
        <h2 className="mt-2 text-2xl font-semibold text-white">Latest alerts</h2>
      </div>

      <div className="space-y-4">
        {items.map((item, index) => {
          const safeType = typeof item?.type === 'string' && item.type in notificationMeta ? (item.type as NotificationType) : undefined
          const meta = (safeType ? notificationMeta[safeType] : undefined) ?? fallbackNotificationMeta
          const title = item?.title ?? 'Notification'
          const description = item?.description ?? 'New notification'
          const time = item?.time ?? 'Now'

          if (process.env.NODE_ENV === 'development' && item?.type && !safeType) {
            console.warn('Unknown notification type received:', item.type, item)
          }

          const Icon = meta.icon
          const badgeText = meta.label
          const badgeVariant = meta.variant

          return (
            <div key={`${title}-${index}`} className="rounded-3xl border border-white/10 bg-slate-950/70 p-4 transition hover:border-blue-400/20 hover:bg-slate-900/80">
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-3">
                  <span className="flex h-10 w-10 items-center justify-center rounded-2xl bg-white/5 text-blue-400">
                    <Icon className="h-5 w-5" />
                  </span>
                  <div>
                    <p className="text-sm font-semibold text-white">{title}</p>
                    <p className="mt-1 text-sm text-slate-400">{description}</p>
                  </div>
                </div>
                <Badge variant={badgeVariant}>{badgeText}</Badge>
              </div>
              <p className="mt-4 text-xs uppercase tracking-[0.24em] text-slate-500">{time}</p>
            </div>
          )
        })}
      </div>
    </Card>
  )
}
