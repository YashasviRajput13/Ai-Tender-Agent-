import { Navbar } from '../components/navbar'
import { Sidebar } from '../components/sidebar'
import { StatsCard } from '../components/stats-card'
import { CategoryDistributionChart } from '../components/charts/category-distribution'
import { MonthlyTrendsChart } from '../components/charts/monthly-trends'
import { MatchScoreChart } from '../components/charts/match-score'
import { TenderTable } from '../components/tender-table'
import { RecommendationCard } from '../components/recommendation-card'
import { NotificationPanel } from '../components/notification-panel'
import {
  statsCards,
  categoryDistribution,
  monthlyTrendData,
  matchScoreData,
  tenderRows,
  recommendations,
  notifications,
} from '../lib/mock-data'

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="grid min-h-screen grid-cols-[280px_1fr] gap-6 px-6 py-6 lg:px-8">
        <Sidebar />

        <div className="flex flex-col gap-6">
          <Navbar />

          <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
            <div className="grid gap-6 lg:grid-cols-2">
              {statsCards.map((stats) => (
                <StatsCard key={stats.title} {...stats} />
              ))}
            </div>

            <div className="grid gap-6">
              <div className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl">
                <div className="mb-4 flex items-center justify-between">
                  <div>
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-400">AI Recommendation</p>
                    <h2 className="mt-2 text-xl font-semibold text-white">Top Recommended Opportunities</h2>
                  </div>
                </div>

                <div className="space-y-4">
                  {recommendations.map((item) => (
                    <RecommendationCard key={item.name} {...item} />
                  ))}
                </div>
              </div>

              <NotificationPanel items={notifications} />
            </div>
          </section>

          <section className="grid gap-6 xl:grid-cols-[1.25fr_0.75fr]">
            <div className="space-y-6">
              <div className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl">
                <div className="mb-6 flex items-center justify-between">
                  <div>
                    <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Charts</p>
                    <h2 className="mt-2 text-2xl font-semibold text-white">Performance overview</h2>
                  </div>
                </div>
                <div className="grid gap-6 xl:grid-cols-3">
                  <CategoryDistributionChart data={categoryDistribution} />
                  <MonthlyTrendsChart data={monthlyTrendData} />
                  <MatchScoreChart data={matchScoreData} />
                </div>
              </div>

              <TenderTable rows={tenderRows} />
            </div>

            <div className="space-y-6">
              <div className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl">
                <div className="mb-4">
                  <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Notifications</p>
                  <h2 className="mt-2 text-2xl font-semibold text-white">Alerts & events</h2>
                </div>
                <NotificationPanel items={notifications} compact />
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>
  )
}
