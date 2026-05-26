import { notFound } from 'next/navigation'

const tenders = [
  { id: 1, title: 'Infrastructure Maintenance Contract', region: 'North America', value: 750000, description: 'Maintenance and repairs for state-owned facilities.', requirements: ['ISO 9001', '5 years experience', 'local partner'] },
]

export default async function TenderPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = await params
  const tender = tenders.find((item) => item.id === Number(resolvedParams.id))
  if (!tender) return notFound()

  return (
    <main className="mx-auto max-w-4xl p-6 sm:p-8">
      <div className="rounded-[32px] border border-white/10 bg-slate-950/80 p-8 shadow-card backdrop-blur-xl">
        <h1 className="text-3xl font-semibold text-white">{tender.title}</h1>
        <p className="mt-3 text-slate-400">{tender.description}</p>

        <div className="mt-8 grid gap-4 md:grid-cols-3">
          <div className="rounded-3xl bg-white/5 p-5 text-sm text-slate-300">
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Region</p>
            <p className="mt-2 text-base font-semibold text-white">{tender.region}</p>
          </div>
          <div className="rounded-3xl bg-white/5 p-5 text-sm text-slate-300">
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Budget</p>
            <p className="mt-2 text-base font-semibold text-white">${tender.value.toLocaleString()}</p>
          </div>
          <div className="rounded-3xl bg-white/5 p-5 text-sm text-slate-300">
            <p className="text-xs uppercase tracking-[0.28em] text-slate-500">Requirements</p>
            <p className="mt-2 text-base font-semibold text-white">{tender.requirements.length}</p>
          </div>
        </div>

        <section className="mt-10">
          <h2 className="text-xl font-semibold text-white">Requirements</h2>
          <ul className="mt-4 space-y-3">
            {tender.requirements.map((req) => (
              <li key={req} className="rounded-3xl bg-slate-900/80 px-4 py-3 text-slate-300">
                {req}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </main>
  )
}
