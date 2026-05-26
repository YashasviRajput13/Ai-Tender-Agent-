'use client'

import { AreaChart, Area, XAxis, YAxis, CartesianGrid, ResponsiveContainer, Tooltip } from 'recharts'
import { Card } from '../ui/card'

interface ChartProps {
  data: { month: string; tenders: number }[]
}

export function MonthlyTrendsChart({ data }: ChartProps) {
  return (
    <Card className="h-[320px]">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Monthly Tender Trends</p>
          <h3 className="mt-2 text-lg font-semibold text-white">Submission volume</h3>
        </div>
      </div>
      <div className="h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id="trendGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.85} />
                <stop offset="95%" stopColor="#818cf8" stopOpacity={0.08} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#334155" strokeDasharray="4 4" vertical={false} />
            <XAxis dataKey="month" tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fill: '#94a3b8' }} axisLine={false} tickLine={false} />
            <Tooltip wrapperStyle={{ backgroundColor: '#0f172a', borderRadius: 18, border: 'none' }} contentStyle={{ backgroundColor: '#020617', color: '#fff' }} />
            <Area type="monotone" dataKey="tenders" stroke="#38bdf8" strokeWidth={3} fill="url(#trendGradient)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}
