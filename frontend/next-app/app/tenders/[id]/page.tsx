import { notFound } from 'next/navigation'

const tenders = [
  { id: 1, title: 'Infrastructure Maintenance Contract', region: 'North America', value: 750000, description: 'Maintenance and repairs for state-owned facilities.', requirements: ['ISO 9001', '5 years experience', 'local partner'] },
]

export default function TenderPage({ params }: { params: { id: string } }) {
  const tender = tenders.find((item) => item.id === Number(params.id))
  if (!tender) return notFound()

  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: 900, margin: '0 auto' }}>
      <h1>{tender.title}</h1>
      <p>{tender.description}</p>
      <p><strong>Region:</strong> {tender.region}</p>
      <p><strong>Value:</strong> ${tender.value.toLocaleString()}</p>
      <h2>Requirements</h2>
      <ul>
        {tender.requirements.map((req) => <li key={req}>{req}</li>)}
      </ul>
    </main>
  )
}
