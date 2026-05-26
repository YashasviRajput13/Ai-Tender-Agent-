export default function NotificationsPage() {
  return (
    <main style={{ fontFamily: 'system-ui, sans-serif', padding: '2rem', maxWidth: 900, margin: '0 auto' }}>
      <h1>Notifications</h1>
      <p>This page will display alerts and recommendation notifications from the notification service.</p>
      <pre style={{ background: '#f5f5f5', padding: 16, borderRadius: 8 }}>
{`GET /notifications/alerts
POST /notifications/send
{
  "recipient": "team@example.com",
  "subject": "New tender recommendation",
  "message": "A strong opportunity has been identified.",
  "channels": ["email"]
}`}
      </pre>
    </main>
  )
}
