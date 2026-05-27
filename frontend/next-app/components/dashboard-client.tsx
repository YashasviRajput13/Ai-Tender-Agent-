"use client"

import { useEffect, useMemo } from "react"
import { useQuery } from "@tanstack/react-query"
import { StatsCard } from "./stats-card"
import { Card } from "./ui/card"
import { Badge } from "./ui/badge"
import { CategoryDistributionChart } from "./charts/category-distribution"
import { MonthlyTrendsChart } from "./charts/monthly-trends"
import { MatchScoreChart } from "./charts/match-score"
import { TenderTable } from "./tender-table"
import { RecommendationCard } from "./recommendation-card"
import { NotificationPanel } from "./notification-panel"
import { fetcher } from "../lib/api"

const API_BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

function formatMoney(value?: number) {
  if (value == null) return "N/A"
  return new Intl.NumberFormat("en-IN", { style: "currency", currency: "INR", maximumFractionDigits: 0 }).format(value)
}

export function DashboardClient() {
  const statsQuery = useQuery<any>(["dashboard-stats"], () => fetcher<any>("/dashboard/stats"))
  const tendersQuery = useQuery<any[]>(["tenders"], () => fetcher<any[]>("/tenders"))
  const notificationsQuery = useQuery<any[]>(["notifications"], () => fetcher<any[]>("/notifications"))
  const recommendationsQuery = useQuery<any[]>(["recommendations"], () => fetcher<any[]>("/recommendations"))

  useEffect(() => {
    const socket = new WebSocket(`${API_BASE.replace(/^http/, "ws")}/ws/updates`)
    socket.addEventListener("open", () => console.log("WebSocket connected"))
    socket.addEventListener("message", (event) => {
      const payload = JSON.parse(event.data)
      if (payload.type === "scrape.completed" || payload.type === "analysis.completed") {
        statsQuery.refetch()
        tendersQuery.refetch()
        notificationsQuery.refetch()
      }
    })
    return () => socket.close()
  }, [statsQuery, tendersQuery, notificationsQuery])

  const stats = statsQuery.data
  const tenders = tendersQuery.data ?? []
  const notifications = notificationsQuery.data ?? []
  const recommendations = recommendationsQuery.data ?? []

  const notificationItems = useMemo(() => {
    return notifications.map((item: any) => ({
      title: item.title || "Tender update",
      description: item.message || item.description || "New notification",
      type: ["new", "deadline", "risk"].includes(item.notification_type) ? item.notification_type : "new",
      time: item.created_at ? new Date(item.created_at).toLocaleString() : "Now",
    }))
  }, [notifications])

  const tenderRows = useMemo(() => {
    return tenders.slice(0, 6).map((tender: any) => ({
      name: tender.title,
      organization: tender.authority || "",
      budget: formatMoney(tender.estimated_value),
      deadline: tender.deadline ? new Date(tender.deadline).toLocaleDateString() : "TBD",
      matchScore: tender.analysis ? `${Math.round(tender.analysis.match_score || 0)}%` : "0%",
      riskLevel: tender.analysis?.risk_level || "Low",
    }))
  }, [tenders])

  const topRecommendations = useMemo(() => {
    return (recommendations ?? []).slice(0, 3).map((item: any) => ({
      name: item.title,
      organization: item.authority || "",
      matchScore: `${Math.round(item.match_score || 0)}%`,
      risk: item.risk_level || "Low",
      value: item.budget || "N/A",
      deadline: item.deadline || "TBD",
    }))
  }, [recommendations])

  const highMatchTenders = useMemo(() => {
    return (recommendations ?? [])
      .slice(0, 3)
      .map((item: any) => ({
        name: item.title,
        organization: item.authority || "",
        matchScore: `${Math.round(item.match_score || 0)}%`,
        risk: item.risk_level || "Low",
        value: item.budget || "N/A",
        deadline: item.deadline || "TBD",
      }))
  }, [recommendations])

  const riskAlerts = useMemo(() => {
    return notificationItems
      .filter((note: any) => note.type === "risk")
      .slice(0, 3)
      .map((note: any) => ({ issue: note.title, status: "High risk", flag: note.description }))
  }, [notificationItems])

  const upcomingDeadlines = useMemo(() => {
    return tenders
      .filter((item: any) => item.deadline)
      .sort((a: any, b: any) => new Date(a.deadline).getTime() - new Date(b.deadline).getTime())
      .slice(0, 3)
      .map((item: any) => ({ name: item.title, deadline: new Date(item.deadline).toLocaleDateString(), days: "Upcoming" }))
  }, [tenders])

  const analyticsWidgets = [
    {
      label: "Total Tenders",
      value: stats ? `${stats.total_tenders}` : "...",
      detail: "All tenders currently tracked",
    },
    {
      label: "Active Tenders",
      value: stats ? `${stats.active_tenders}` : "...",
      detail: "Open opportunities in the system",
    },
    {
      label: "High Match Opportunities",
      value: stats ? `${stats.high_match_opportunities}` : "...",
      detail: "Tenders with strong match score",
    },
    {
      label: "Risk Alerts",
      value: stats ? `${stats.risk_alerts}` : "...",
      detail: "Active risk signals from analysis",
    },
  ]

  const categoryDistribution = tenders.reduce((acc: any, tender: any) => {
    const category = tender.category || "Other"
    const current = acc.find((item: any) => item.name === category)
    if (current) current.value += 1
    else acc.push({ name: category, value: 1 })
    return acc
  }, [])

  const monthlyTrendData = Array.from({ length: 12 }).map((_, index) => ({
    month: new Date(0, index).toLocaleString("en-US", { month: "short" }),
    tenders: tenders.filter((tender: any) => new Date(tender.created_at).getMonth() === index).length,
  }))

  const matchScoreData = [
    { name: "0-40%", score: tenders.filter((tender: any) => tender.analysis?.match_score <= 40).length },
    { name: "40-60%", score: tenders.filter((tender: any) => tender.analysis?.match_score > 40 && tender.analysis?.match_score <= 60).length },
    { name: "60-80%", score: tenders.filter((tender: any) => tender.analysis?.match_score > 60 && tender.analysis?.match_score <= 80).length },
    { name: "80-100%", score: tenders.filter((tender: any) => tender.analysis?.match_score > 80).length },
  ]

  return (
    <div className="flex flex-col gap-6">
      <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <div className="grid gap-6 lg:grid-cols-2">
          {analyticsWidgets.map((stats) => (
            <StatsCard key={stats.label} title={stats.label} value={stats.value} detail={stats.detail} />
          ))}
        </div>
        <div className="grid gap-6">
          <div className="space-y-4">
            {topRecommendations.length > 0 ? (
              topRecommendations.map((item) => (
                <RecommendationCard
                  key={item.name}
                  name={item.name}
                  organization={item.organization}
                  matchScore={item.matchScore}
                  risk={item.risk}
                  value={item.value}
                  deadline={item.deadline}
                />
              ))
            ) : (
              <div className="rounded-3xl border border-white/10 bg-slate-950/80 p-4 text-slate-300">
                Loading live recommendations...
              </div>
            )}
          </div>
          <NotificationPanel items={notifications} compact />
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <div className="space-y-6">
          <Card className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl">
            <div className="mb-6 flex items-center justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Tender trends</p>
                <h2 className="mt-2 text-2xl font-semibold text-white">Submission volume & category mix</h2>
              </div>
            </div>
            <div className="grid gap-6 xl:grid-cols-3">
              <CategoryDistributionChart data={categoryDistribution} />
              <MonthlyTrendsChart data={monthlyTrendData} />
              <MatchScoreChart data={matchScoreData} />
            </div>
          </Card>

          <TenderTable rows={tenderRows} />
        </div>

        <div className="space-y-6">
          <Card className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl">
            <div className="mb-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">High match tenders</p>
              <h2 className="mt-2 text-2xl font-semibold text-white">Top potential wins</h2>
            </div>
            <div className="space-y-4">
              {highMatchTenders.map((item) => (
                <RecommendationCard key={item.name} {...item} />
              ))}
            </div>
          </Card>

          <Card className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl">
            <div className="mb-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Risk alerts</p>
              <h2 className="mt-2 text-2xl font-semibold text-white">Active risk signals</h2>
            </div>
            <div className="space-y-4">
              {riskAlerts.map((alert) => (
                <div key={alert.issue} className="rounded-3xl border border-white/10 bg-slate-950/80 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-base font-semibold text-white">{alert.issue}</p>
                      <p className="mt-2 text-sm text-slate-400">{alert.flag}</p>
                    </div>
                    <Badge variant="danger">{alert.status}</Badge>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card className="rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl">
            <div className="mb-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-400">Upcoming deadlines</p>
              <h2 className="mt-2 text-2xl font-semibold text-white">Priority submission dates</h2>
            </div>
            <div className="space-y-3">
              {upcomingDeadlines.map((item) => (
                <div key={item.name} className="flex items-center justify-between rounded-3xl border border-white/10 bg-slate-950/80 p-4">
                  <div>
                    <p className="font-semibold text-white">{item.name}</p>
                    <p className="text-sm text-slate-400">{item.deadline}</p>
                  </div>
                  <Badge variant="warning">{item.days}</Badge>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </section>
    </div>
  )
}
