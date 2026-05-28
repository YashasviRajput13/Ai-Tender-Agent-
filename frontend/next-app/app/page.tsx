import Link from "next/link"
import { Button } from "../components/ui/button"
import { LandingFeatures } from "../components/landing-features"

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <main className="mx-auto flex min-h-screen max-w-7xl flex-col px-6 py-10 lg:px-8">
        <header className="flex flex-col gap-5 lg:flex-row lg:items-center lg:justify-between">
          <div className="space-y-4">
            <span className="inline-flex rounded-full bg-white px-4 py-2 text-xs font-semibold uppercase tracking-[0.32em] text-slate-700 shadow-sm ring-1 ring-slate-200">
              AI-powered tender intelligence
            </span>
            <div className="space-y-6">
              <h1 className="max-w-4xl text-6xl font-semibold tracking-tight text-slate-950 sm:text-7xl">
                Win more
              </h1>
              <p className="max-w-2xl text-lg leading-8 text-slate-600 sm:text-xl">
                Real-time tenders from eProcure, MP Tenders, and eTenders — analyzed by AI for eligibility, risk, and your win probability.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-4">
            <Link
              href="/dashboard"
              className="inline-flex min-w-[160px] items-center justify-center rounded-full bg-blue-600 px-8 py-3 text-sm font-semibold text-white shadow-sm transition hover:bg-blue-700"
            >
              Start free
            </Link>
            <Button variant="ghost" className="min-w-[160px]">Sign in</Button>
          </div>
        </header>

        <section className="mt-12 grid gap-10 lg:grid-cols-[1.3fr_0.9fr] lg:items-center">
          <div className="space-y-6 rounded-[40px] bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 p-10 text-white shadow-[0_25px_80px_rgba(15,23,42,0.12)]">
            <div className="grid gap-6 sm:grid-cols-2">
              <div className="rounded-[32px] border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
                <span className="text-sm uppercase tracking-[0.32em] text-slate-300">Total tenders</span>
                <p className="mt-4 text-4xl font-semibold">7</p>
              </div>
              <div className="rounded-[32px] border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
                <span className="text-sm uppercase tracking-[0.32em] text-slate-300">Closing soon</span>
                <p className="mt-4 text-4xl font-semibold">2</p>
              </div>
            </div>
            <div className="grid gap-6 sm:grid-cols-2">
              <div className="rounded-[32px] border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
                <span className="text-sm uppercase tracking-[0.32em] text-slate-300">Total value</span>
                <p className="mt-4 text-4xl font-semibold">₹13,75,00,000</p>
              </div>
              <div className="rounded-[32px] border border-white/10 bg-white/5 p-6 backdrop-blur-xl">
                <span className="text-sm uppercase tracking-[0.32em] text-slate-300">High match</span>
                <p className="mt-4 text-4xl font-semibold">3</p>
              </div>
            </div>
          </div>

          <div className="relative overflow-hidden rounded-[40px] bg-white p-8 shadow-xl ring-1 ring-slate-200">
            <div className="absolute inset-x-0 top-0 h-44 bg-gradient-to-r from-sky-500 to-blue-500 opacity-20" />
            <div className="relative space-y-8">
              <div className="rounded-[32px] border border-slate-200 bg-slate-50 p-6">
                <p className="text-sm uppercase tracking-[0.32em] text-slate-500">Smart insights</p>
                <h2 className="mt-3 text-2xl font-semibold text-slate-950">AI-assisted bid scoring across portals</h2>
                <p className="mt-4 text-sm leading-6 text-slate-600">
                  Monitor eligibility, cost, and risk in one unified dashboard powered by procurement AI.
                </p>
              </div>

              <div className="rounded-[32px] border border-slate-200 bg-white p-6 shadow-sm">
                <div className="flex items-center justify-between gap-4">
                  <div>
                    <p className="text-sm uppercase tracking-[0.32em] text-slate-500">Latest tenders</p>
                    <p className="mt-3 font-semibold text-slate-900">Search for Latest Active Tenders - Central</p>
                  </div>
                  <span className="rounded-full bg-slate-100 px-3 py-1 text-xs uppercase tracking-[0.3em] text-slate-700">
                    General
                  </span>
                </div>
                <div className="mt-6 space-y-4">
                  <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-900">Hospital Equipment Supply - Ventilators & Monitors</p>
                    <p className="mt-2 text-sm text-slate-600">AIIMS Bhopal • Healthcare • closes in 4 days</p>
                  </div>
                  <div className="rounded-3xl border border-slate-200 bg-slate-50 p-4">
                    <p className="font-semibold text-slate-900">Cloud Infrastructure & DevOps Services for State Portal</p>
                    <p className="mt-2 text-sm text-slate-600">Govt of Maharashtra IT Dept • IT • closes in 6 days</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className="mt-20">
          <LandingFeatures />
        </section>
      </main>
    </div>
  )
}
