import { Navbar } from "../../components/navbar"
import { Sidebar } from "../../components/sidebar"
import { DashboardClient } from "../../components/dashboard-client"
import { ReactQueryProvider } from "../../components/react-query-provider"

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <div className="grid min-h-screen grid-cols-[280px_1fr] gap-6 px-6 py-6 lg:px-8">
        <Sidebar />
        <div className="flex flex-col gap-6">
          <Navbar />
          <ReactQueryProvider>
            <DashboardClient />
          </ReactQueryProvider>
        </div>
      </div>
    </div>
  )
}
