'use client'

import { Badge } from './ui/badge'
import { Button } from './ui/button'

interface RecommendationCardProps {
  name: string
  organization?: string
  value: string
  matchScore: string
  risk: string
  deadline: string
}

export function RecommendationCard({ name, organization, value, matchScore, risk, deadline }: RecommendationCardProps) {
  return (
    <div className="rounded-[28px] border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-sm font-semibold text-slate-900">{name}</p>
          {organization ? <p className="mt-1 text-xs text-slate-500">{organization}</p> : null}
          <p className="mt-1 text-xs text-slate-500">Estimated revenue {value}</p>
        </div>
        <Badge variant="info">{matchScore}</Badge>
      </div>

      <div className="mt-4 flex flex-wrap items-center gap-3 text-sm text-slate-600">
        <span className="rounded-2xl bg-slate-100 px-3 py-2">Risk: {risk}</span>
        <span className="rounded-2xl bg-slate-100 px-3 py-2">Deadline: {deadline}</span>
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
