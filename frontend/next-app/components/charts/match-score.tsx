'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from 'recharts'
import { Card } from '../ui/card'

interface ChartProps {
  data: { name: string; score: number }[]
}

export function MatchScoreChart({ data }: ChartProps) {
  return (
    <Card className="h-[320px]">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Match Score Analytics</p>
          <h3 className="mt-2 text-lg font-semibold text-white">Opportunity fit</h3>
        </div>
      </div>
      <div className="h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={data} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
            <CartesianGrid stroke="#334155" strokeDasharray="3 3" vertical={false} />
            <XAxis dataKey="name" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <Tooltip wrapperStyle={{ backgroundColor: '#0f172a', borderRadius: 18, border: 'none' }} contentStyle={{ backgroundColor: '#020617', color: '#fff' }} />
            <Bar dataKey="score" fill="#8b5cf6" radius={[12, 12, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}
