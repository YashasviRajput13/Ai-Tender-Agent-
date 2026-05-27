'use client'

import { useRouter } from 'next/navigation'
import { Card } from './ui/card'
import { Button } from './ui/button'
import { Badge } from './ui/badge'

interface TenderRow {
  id: number
  name: string
  organization: string
  budget: string
  deadline: string
  matchScore: string
  riskLevel: 'Low' | 'Medium' | 'High'
}

interface TenderTableProps {
  rows: TenderRow[]
}

const riskColor: Record<'Low' | 'Medium' | 'High', 'success' | 'warning' | 'danger'> = {
  Low: 'success',
  Medium: 'warning',
  High: 'danger',
}

export function TenderTable({ rows }: TenderTableProps) {
  const router = useRouter()

  const onRowClick = (id: number) => {
    router.push(`/tenders/${id}`)
  }

  return (
    <Card>
      <div className="mb-6 flex items-center justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.24em] text-slate-400">Tender pipeline</p>
          <h2 className="mt-2 text-2xl font-semibold text-white">Recent tender activity</h2>
        </div>
        <Button variant="ghost">View all</Button>
      </div>

      <div className="overflow-hidden rounded-[28px] border border-white/10 bg-white/5">
        <table className="min-w-full border-collapse text-left text-sm text-slate-300">
          <thead>
            <tr className="border-b border-white/10 text-slate-400">
              <th className="px-6 py-4">Tender Name</th>
              <th className="px-6 py-4">Organization</th>
              <th className="px-6 py-4">Budget</th>
              <th className="px-6 py-4">Deadline</th>
              <th className="px-6 py-4">Match Score</th>
              <th className="px-6 py-4">Risk Level</th>
              <th className="px-6 py-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr
                key={row.id}
                className="border-b border-white/10 transition hover:bg-white/5 hover:cursor-pointer"
                onClick={() => onRowClick(row.id)}
              >
                <td className="px-6 py-4 font-semibold text-white">{row.name}</td>
                <td className="px-6 py-4">{row.organization}</td>
                <td className="px-6 py-4">{row.budget}</td>
                <td className="px-6 py-4">{row.deadline}</td>
                <td className="px-6 py-4">{row.matchScore}</td>
                <td className="px-6 py-4">
                  <Badge variant={riskColor[row.riskLevel] || 'default'}>{row.riskLevel}</Badge>
                </td>
                <td className="px-6 py-4">
                  <Button variant="ghost" className="px-3 py-2 text-xs" onClick={(event) => { event.stopPropagation(); onRowClick(row.id) }}>
                    Review
                  </Button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Card>
  )
}
