import Link from 'next/link'

const tenders = [
  { id: 1, title: 'Infrastructure Maintenance Contract', region: 'North America', value: 750000 },
]

export default function Home() {
  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: 960, margin: '0 auto' }}>
      <header>
        <h1>Agentic AI Tender</h1>
        <p>Dashboard for discovery, analysis, and tender recommendation.</p>
      </header>

      <section style={{ marginTop: '2rem' }}>
        <h2>Active Tenders</h2>
        <div style={{ display: 'grid', gap: '1rem' }}>
          {tenders.map((tender) => (
            <article key={tender.id} style={{ border: '1px solid #ddd', borderRadius: 12, padding: 16 }}>
              <h3>{tender.title}</h3>
              <p>Region: {tender.region}</p>
              <p>Value: ${tender.value.toLocaleString()}</p>
              <Link href={`/tenders/${tender.id}`}>View details</Link>
            </article>
          ))}
        </div>
      </section>

      <section style={{ marginTop: '2rem' }}>
        <h2>Quick Actions</h2>
        <ul>
          <li><Link href="/analysis">Run analysis</Link></li>
          <li><Link href="/notifications">View notifications</Link></li>
        </ul>
      </section>
    </main>
  )
}
