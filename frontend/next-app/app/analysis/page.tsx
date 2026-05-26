export default function AnalysisPage() {
  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: 900, margin: '0 auto' }}>
      <h1>Analysis Service</h1>
      <p>Use this page to integrate API evaluation and scoring for new tenders.</p>
      <pre style={{ background: '#f5f5f5', padding: 16, borderRadius: 8 }}>
{`POST /analysis/score
{
  "title": "...",
  "description": "...",
  "requirements": ["..."],
  "value": 400000,
  "region": "Europe"
}`}
      </pre>
    </main>
  )
}
