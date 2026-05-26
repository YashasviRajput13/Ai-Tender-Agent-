'use client'

import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import { Card } from '../ui/card'

const colors = ['#6d28d9', '#0ea5e9', '#f97316', '#22c55e', '#ec4899']

interface ChartProps {
  data: { name: string; value: number }[]
}

export function CategoryDistributionChart({ data }: ChartProps) {
  return (
    <Card className="h-[320px]">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-slate-400">Category Distribution</p>
          <h3 className="mt-2 text-lg font-semibold text-white">Tender categories</h3>
        </div>
      </div>
      <div className="h-[250px]">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} innerRadius={40} paddingAngle={4}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
              ))}
            </Pie>
            <Tooltip wrapperStyle={{ backgroundColor: '#0f172a', borderRadius: 18, border: 'none' }} contentStyle={{ backgroundColor: '#020617', color: '#fff' }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </Card>
  )
}
