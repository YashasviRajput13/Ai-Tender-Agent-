"use client"

import { useEffect, useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { StatsCard } from "./stats-card"
import { Card } from "./ui/card"
import { Badge } from "./ui/badge"
import { Button } from "./ui/button"
import { CategoryDistributionChart } from "./charts/category-distribution"
import { MonthlyTrendsChart } from "./charts/monthly-trends"
import { MatchScoreChart } from "./charts/match-score"
import { TenderTable } from "./tender-table"
import { RecommendationCard } from "./recommendation-card"
import { NotificationPanel } from "./notification-panel"
import { fetcher, postData } from "../lib/api"

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
  const scrapeStatusQuery = useQuery<any>(["scrape-status"], () => fetcher<any>("/scrape/status"), {
    refetchInterval: 15000,
    staleTime: 10000,
    retry: false,
  })

  const [isScrapeStarting, setIsScrapeStarting] = useState(false)
  const [scrapeMessage, setScrapeMessage] = useState<string | null>(null)
  const [seedMessage, setSeedMessage] = useState<string | null>(null)

  const startLiveScrape = async () => {
    setIsScrapeStarting(true)
    setScrapeMessage(null)
    setSeedMessage(null)

    try {
      await postData<{ status: string; source_url: string }>("/scrape/start", {})
      setScrapeMessage("Live scrape started. Waiting for results...")
      scrapeStatusQuery.refetch()
      tendersQuery.refetch()
      notificationsQuery.refetch()
    } catch (error) {
      setScrapeMessage(`Unable to start live scrape: ${error instanceof Error ? error.message : "Unknown error"}`)
    } finally {
      setIsScrapeStarting(false)
    }
  }

  const seedDemoData = () => {
    setSeedMessage("Seed demo data is not configured in this environment yet.")
    setScrapeMessage(null)
  }

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
      id: tender.id,
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

  const totalValue = formatMoney(tenders.reduce((sum: number, tender: any) => sum + (Number(tender.estimated_value) || 0), 0))
  const closingSoonCount = tenders.filter((item: any) => {
    if (!item.deadline) return false
    const deadline = new Date(item.deadline)
    const diff = Math.ceil((deadline.getTime() - Date.now()) / (1000 * 60 * 60 * 24))
    return diff >= 0 && diff <= 7
  }).length

  const latestTenders = useMemo(() => {
    return tenders.slice(0, 6).map((tender: any) => {
      const daysRemaining = tender.deadline
        ? Math.max(0, Math.ceil((new Date(tender.deadline).getTime() - Date.now()) / (1000 * 60 * 60 * 24)))
        : null
      return {
        id: tender.id,
        title: tender.title,
        organization: tender.authority || "Unknown authority",
        category: tender.category || "General",
        deadline: tender.deadline ? new Date(tender.deadline).toLocaleDateString() : "TBD",
        daysRemaining,
        value: formatMoney(tender.estimated_value),
        status: tender.analysis?.match_score ? `${Math.round(tender.analysis.match_score)}% match` : "Not scored",
      }
    })
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

  function LatestTenderCard({ tender }: { tender: any }) {
    return (
      <Card className="flex flex-col gap-4 rounded-[28px] border border-slate-200 bg-slate-50 p-5 transition hover:-translate-y-1 hover:shadow-md">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-sm uppercase tracking-[0.28em] text-slate-500">{tender.category}</p>
            <h3 className="mt-2 text-lg font-semibold text-slate-900">{tender.title}</h3>
            <p className="mt-2 text-sm text-slate-600">{tender.organization}</p>
          </div>
          <div className="text-right">
            <p className="text-sm text-slate-500">Value</p>
            <p className="mt-1 text-lg font-semibold text-slate-900">{tender.value}</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-sm text-slate-600">
          <span className="rounded-full bg-slate-100 px-3 py-2">Deadline: {tender.deadline}</span>
          {tender.daysRemaining !== null ? (
            <span className="rounded-full bg-sky-50 px-3 py-2 text-sky-700">{tender.daysRemaining} days left</span>
          ) : null}
          <span className="rounded-full bg-emerald-50 px-3 py-2 text-emerald-700">{tender.status}</span>
        </div>
      </Card>
    )
  }

  return (
    <div className="flex flex-col gap-6">
      <section className="space-y-6">
        <div className="rounded-[32px] border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div className="space-y-3">
              <p className="text-sm uppercase tracking-[0.32em] text-slate-500">Dashboard</p>
              <div className="flex flex-col gap-2 sm:flex-row sm:items-end sm:gap-4">
                <h1 className="text-3xl font-semibold text-slate-900">Your tender intelligence at a glance</h1>
                <span className="rounded-full bg-slate-100 px-3 py-1 text-xs uppercase tracking-[0.32em] text-slate-600 ring-1 ring-slate-200">AI-powered insights</span>
              </div>
              <p className="max-w-2xl text-sm leading-6 text-slate-600">
                Monitor active opportunities, closing deadlines, and high-value tenders with a single intelligent dashboard.
              </p>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <Button variant="ghost" onClick={seedDemoData} className="px-4 py-3 text-sm">
                Seed demo data
              </Button>
              <Button onClick={startLiveScrape} disabled={isScrapeStarting} className="px-4 py-3 text-sm">
                {isScrapeStarting ? "Starting fetch..." : "Scrape now"}
              </Button>
            </div>
          </div>
          {(seedMessage || scrapeMessage) && (
            <div className="mt-4 rounded-3xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
              {seedMessage || scrapeMessage}
            </div>
          )}
        </div>

        <div className="grid gap-6 sm:grid-cols-2 xl:grid-cols-4">
          <StatsCard title="Total Tenders" value={stats ? `${stats.total_tenders}` : "..."} detail="All tenders currently tracked" />
          <StatsCard title="Open" value={stats ? `${stats.active_tenders}` : "..."} detail="Currently open opportunities" accent="from-sky-500 to-blue-500" />
          <StatsCard title="Closing in 7 days" value={`${closingSoonCount}`} detail="Tenders that need action soon" accent="from-emerald-500 to-emerald-700" />
          <StatsCard title="Total value" value={totalValue} detail="Aggregate estimated tender amount" accent="from-fuchsia-500 to-rose-500" />
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.4fr_0.6fr]">
        <div className="space-y-4">
          <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm uppercase tracking-[0.32em] text-slate-500">Latest tenders</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-900">Recent active opportunities</h2>
            </div>
            <Button variant="ghost" className="px-4 py-3 text-sm">View all</Button>
          </div>
          <div className="space-y-4">
            {latestTenders.length > 0 ? (
              latestTenders.map((tender) => <LatestTenderCard key={tender.id} tender={tender} />)
            ) : (
              <Card className="rounded-[28px] border border-slate-200 bg-slate-50 p-8 text-center text-slate-500">
                Loading tenders or no tenders available yet.
              </Card>
            )}
          </div>
        </div>

        <div className="space-y-6">
          <Card className="rounded-[32px] border border-slate-200 bg-white p-6 shadow-sm">
            <div className="flex items-center justify-between gap-3">
              <div>
                <p className="text-sm uppercase tracking-[0.32em] text-slate-500">Key summary</p>
                <h3 className="mt-2 text-2xl font-semibold text-slate-900">Action-ready highlights</h3>
              </div>
              <div className="rounded-full bg-blue-50 px-3 py-2 text-sm text-blue-700">Live</div>
            </div>
            <div className="mt-6 space-y-4">
              <div className="rounded-3xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Open tenders</p>
                <p className="mt-2 text-3xl font-semibold text-slate-900">{stats ? `${stats.active_tenders}` : "..."}</p>
              </div>
              <div className="rounded-3xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">High match opportunities</p>
                <p className="mt-2 text-3xl font-semibold text-slate-900">{stats ? `${stats.high_match_opportunities}` : "..."}</p>
              </div>
              <div className="rounded-3xl bg-slate-50 p-4">
                <p className="text-sm text-slate-500">Estimated value</p>
                <p className="mt-2 text-3xl font-semibold text-slate-900">{totalValue}</p>
              </div>
            </div>
          </Card>

          <NotificationPanel items={notifications} compact />
        </div>
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.3fr_0.7fr]">
        <div className="space-y-6">
          <Card>
            <div className="mb-6 flex items-center justify-between">
              <div>
                <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Tender trends</p>
                <h2 className="mt-2 text-2xl font-semibold text-slate-900">Submission volume & category mix</h2>
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
          <Card>
            <div className="mb-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">High match tenders</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-900">Top potential wins</h2>
            </div>
            <div className="space-y-4">
              {highMatchTenders.map((item) => (
                <RecommendationCard key={item.name} {...item} />
              ))}
            </div>
          </Card>

          <Card>
            <div className="mb-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Risk alerts</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-900">Active risk signals</h2>
            </div>
            <div className="space-y-4">
              {riskAlerts.map((alert) => (
                <div key={alert.issue} className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                  <div className="flex items-center justify-between gap-3">
                    <div>
                      <p className="text-base font-semibold text-slate-900">{alert.issue}</p>
                      <p className="mt-2 text-sm text-slate-600">{alert.flag}</p>
                    </div>
                    <Badge variant="danger">{alert.status}</Badge>
                  </div>
                </div>
              ))}
            </div>
          </Card>

          <Card>
            <div className="mb-6">
              <p className="text-sm uppercase tracking-[0.24em] text-slate-500">Upcoming deadlines</p>
              <h2 className="mt-2 text-2xl font-semibold text-slate-900">Priority submission dates</h2>
            </div>
            <div className="space-y-3">
              {upcomingDeadlines.map((item) => (
                <div key={item.name} className="flex items-center justify-between rounded-3xl border border-slate-200 bg-slate-50 p-4">
                  <div>
                    <p className="font-semibold text-slate-900">{item.name}</p>
                    <p className="text-sm text-slate-600">{item.deadline}</p>
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
