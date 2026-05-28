"use client"

import { useState } from "react"
import { API_BASE } from "../lib/api"

interface AnalysisActionProps {
  tenderId: string
}

export default function AnalysisAction({ tenderId }: AnalysisActionProps) {
  const [status, setStatus] = useState("idle")
  const [error, setError] = useState<string | null>(null)

  const startAnalysis = async () => {
    setStatus("starting")
    setError(null)

    try {
      const response = await fetch(`${API_BASE}/analysis/start/${tenderId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        throw new Error(`Failed to start analysis: ${response.status}`)
      }

      setStatus("started")
    } catch (err) {
      setStatus("error")
      setError(err instanceof Error ? err.message : String(err))
    }
  }

  return (
    <div className="mt-6 flex flex-col gap-3">
      <button
        type="button"
        onClick={startAnalysis}
        className="inline-flex items-center justify-center rounded-3xl bg-sky-500 px-5 py-3 text-sm font-semibold text-white transition hover:bg-sky-400"
      >
        {status === "starting" ? "Starting analysis..." : status === "started" ? "Analysis started" : "Run tender analysis"}
      </button>
      {error ? <p className="text-sm text-rose-400">{error}</p> : null}
    </div>
  )
}
