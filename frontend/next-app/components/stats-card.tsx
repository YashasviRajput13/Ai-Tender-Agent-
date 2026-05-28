'use client'

import { Card } from './ui/card'
import { cn } from '../lib/utils'
import { ArrowUpRight } from 'lucide-react'

interface StatsCardProps {
  title: string
  value: string
  change?: string
  accent?: string
  detail?: string
}

export function StatsCard({ title, value, change = "", accent = "from-slate-500 to-slate-700", detail = "" }: StatsCardProps) {
  return (
    <Card className="group overflow-hidden">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm uppercase tracking-[0.32em] text-slate-500">{title}</p>
          <p className="mt-3 text-3xl font-semibold text-slate-900">{value}</p>
        </div>
        <div className={cn('rounded-3xl px-4 py-3 text-sm font-semibold text-white', `bg-gradient-to-br ${accent}`)}>
          <div className="flex items-center gap-2">
            <span>{change}</span>
            <ArrowUpRight className="h-4 w-4" />
          </div>
        </div>
      </div>
      <p className="mt-4 text-sm leading-6 text-slate-500">{detail || 'Powered by AI recommendation models and in-depth tender analytics.'}</p>
    </Card>
  )
}
