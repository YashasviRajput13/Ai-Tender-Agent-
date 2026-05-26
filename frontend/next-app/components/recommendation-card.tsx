'use client'

import { Badge } from './ui/badge'
import { Button } from './ui/button'

interface RecommendationCardProps {
  name: string
  value: string
  matchScore: string
  risk: string
  deadline: string
}

export function RecommendationCard({ name, value, matchScore, risk, deadline }: RecommendationCardProps) {
  return (
    <div className="rounded-[28px] border border-white/10 bg-slate-950/70 p-5 shadow-card transition hover:-translate-y-0.5 hover:bg-slate-900/80">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-white">{name}</p>
          <p className="mt-1 text-xs text-slate-400">Estimated revenue {value}</p>
        </div>
        <Badge variant="info">{matchScore}</Badge>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-slate-300">
        <span className="rounded-2xl bg-white/5 px-3 py-2">Risk: {risk}</span>
        <span className="rounded-2xl bg-white/5 px-3 py-2">Deadline: {deadline}</span>
      </div>

      <div className="mt-5 flex items-center justify-between gap-4">
        <Button variant="ghost" className="px-4 py-2 text-sm">
          Details
        </Button>
        <Button className="px-4 py-2 text-sm">Track</Button>
      </div>
    </div>
  )
}
