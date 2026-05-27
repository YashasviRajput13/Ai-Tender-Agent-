import { notFound } from "next/navigation"

import { fetcher } from "../../../lib/api"
import AnalysisAction from "../../../components/analysis-action"

interface TenderDocument {
  id: number
  tender_id: number
  url: string
  filename?: string
  raw_text?: string
  parsed_sections?: Record<string, unknown>
  created_at: string
}

interface TenderAnalysis {
  summary?: string
  eligibility?: string[]
  required_documents?: string[]
  technical_requirements?: string[]
  risk_factors?: string[]
  risk_level?: string
  risk_reasons?: string[]
  category?: string
  deadline?: string
  budget?: string
  confidence_score?: number
  match_score?: number
  relevance_score?: number
  success_probability?: number
  raw_response?: Record<string, unknown>
}

interface Tender {
  id: number
  source: string
  source_tender_id?: string
  title: string
  description?: string
  authority?: string
  deadline?: string
  estimated_value?: number
  category?: string
  region?: string
  tender_url?: string
  status?: string
  raw_metadata?: Record<string, unknown>
  created_at: string
  updated_at: string
  documents?: TenderDocument[]
  analysis?: TenderAnalysis
}

async function getTender(id: string) {
  return fetcher<Tender>(`/tenders/${id}`)
}

export default async function TenderPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = await params
  const tender = await getTender(resolvedParams.id)
  if (!tender) return notFound()

  const analysis = tender.analysis

  return (
    <main className="mx-auto max-w-4xl p-6 sm:p-8">
      <div className="rounded-[32px] border border-white/10 bg-slate-950/80 p-8 shadow-card backdrop-blur-xl">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
          <div>
            <h1 className="text-3xl font-semibold text-white">{tender.title}</h1>
            <p className="mt-3 text-slate-400">{tender.description || "No description available."}</p>
          </div>
          <AnalysisAction tenderId={String(tender.id)} />
        </div>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          <div className="rounded-3xl bg-white/5 p-5 text-sm text-slate-300">
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Region</p>
            <p className="mt-2 text-base font-semibold text-white">{tender.region || "Unknown"}</p>
          </div>
          <div className="rounded-3xl bg-white/5 p-5 text-sm text-slate-300">
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Budget</p>
            <p className="mt-2 text-base font-semibold text-white">{analysis?.budget || tender.estimated_value?.toString() || "N/A"}</p>
          </div>
          <div className="rounded-3xl bg-white/5 p-5 text-sm text-slate-300">
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Deadline</p>
            <p className="mt-2 text-base font-semibold text-white">{analysis?.deadline || tender.deadline || "Unknown"}</p>
          </div>
        </div>

        <section className="mt-10 grid gap-6 lg:grid-cols-2">
          {analysis?.summary ? (
            <div className="rounded-3xl bg-slate-900/80 p-6 text-slate-200">
              <h2 className="text-xl font-semibold text-white">AI Summary</h2>
              <p className="mt-4 text-sm leading-7 text-slate-300">{analysis.summary}</p>
            </div>
          ) : null}

          <div className="rounded-3xl bg-slate-900/80 p-6 text-slate-200">
            <h2 className="text-xl font-semibold text-white">Tender Details</h2>
            <dl className="mt-4 space-y-3 text-sm text-slate-300">
              <div>
                <dt className="font-medium text-slate-400">Authority</dt>
                <dd>{tender.authority || "N/A"}</dd>
              </div>
              <div>
                <dt className="font-medium text-slate-400">Source</dt>
                <dd>{tender.source}</dd>
              </div>
              <div>
                <dt className="font-medium text-slate-400">Tender URL</dt>
                <dd>
                  {tender.tender_url ? (
                    <a className="text-sky-300 hover:text-sky-200" href={tender.tender_url} target="_blank" rel="noreferrer">
                      View tender posting
                    </a>
                  ) : (
                    "N/A"
                  )}
                </dd>
              </div>
            </dl>
          </div>
        </section>

        {analysis ? (
          <section className="mt-10 grid gap-6 lg:grid-cols-2">
            {analysis.eligibility?.length ? (
              <div className="rounded-3xl bg-slate-900/80 p-6 text-slate-200">
                <h2 className="text-xl font-semibold text-white">Eligibility</h2>
                <ul className="mt-4 space-y-2 text-sm text-slate-300">
                  {analysis.eligibility.map((item) => (
                    <li key={item} className="rounded-2xl bg-slate-950/70 px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}

            {analysis.required_documents?.length ? (
              <div className="rounded-3xl bg-slate-900/80 p-6 text-slate-200">
                <h2 className="text-xl font-semibold text-white">Required Documents</h2>
                <ul className="mt-4 space-y-2 text-sm text-slate-300">
                  {analysis.required_documents.map((item) => (
                    <li key={item} className="rounded-2xl bg-slate-950/70 px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}

            {analysis.technical_requirements?.length ? (
              <div className="rounded-3xl bg-slate-900/80 p-6 text-slate-200">
                <h2 className="text-xl font-semibold text-white">Technical Requirements</h2>
                <ul className="mt-4 space-y-2 text-sm text-slate-300">
                  {analysis.technical_requirements.map((item) => (
                    <li key={item} className="rounded-2xl bg-slate-950/70 px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}

            {analysis.risk_factors?.length ? (
              <div className="rounded-3xl bg-slate-900/80 p-6 text-slate-200">
                <h2 className="text-xl font-semibold text-white">Risk Factors</h2>
                <ul className="mt-4 space-y-2 text-sm text-slate-300">
                  {analysis.risk_factors.map((item) => (
                    <li key={item} className="rounded-2xl bg-slate-950/70 px-4 py-3">
                      {item}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
          </section>
        ) : (
          <section className="mt-10 rounded-3xl bg-slate-900/80 p-6 text-slate-200">
            <h2 className="text-xl font-semibold text-white">No analysis yet</h2>
            <p className="mt-4 text-sm text-slate-300">Run AI analysis to extract tenders insights, risks, and required documents.</p>
          </section>
        )}
      </div>
    </main>
  )
}
