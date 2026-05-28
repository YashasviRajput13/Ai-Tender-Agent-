"use client"

import { useMemo, useState } from "react"
import { Button } from "./ui/button"
import { Card } from "./ui/card"

interface ChatMessage {
  id: string
  sender: "user" | "agent"
  text: string
  tag?: string
}

const initialMessages: ChatMessage[] = [
  {
    id: "1",
    sender: "user",
    text: "Can the system integrate bid evaluations with our approval workflow?",
  },
  {
    id: "2",
    sender: "agent",
    text: "Yes — I’ve mapped vendor rankings to your approval chain, including budget thresholds and risk flags.",
    tag: "Processing",
  },
  {
    id: "3",
    sender: "user",
    text: "Any bids needing extra scrutiny?",
  },
  {
    id: "4",
    sender: "agent",
    text: "Two bids exceed the budget threshold. I’ve flagged them for review and recommended routing them to senior approval.",
  },
  {
    id: "5",
    sender: "agent",
    text: "Done! Decision-ready report sent to stakeholders.",
    tag: "Routing approved",
  },
]

function getBotResponse(input: string) {
  const normalized = input.trim().toLowerCase()

  if (normalized.includes("approval") || normalized.includes("route")) {
    return "I can integrate approval routing and surface the top bids for final sign-off. I’ll also track budget compliance and decision status."
  }

  if (normalized.includes("compliance") || normalized.includes("legal") || normalized.includes("regulatory")) {
    return "I’ll run compliance checks across all submissions and highlight any legal or regulatory gaps before approval."
  }

  if (normalized.includes("budget") || normalized.includes("threshold") || normalized.includes("cost")) {
    return "Two bids currently exceed your budget threshold. I’m flagging them and recommending a review path with risk scoring."
  }

  if (normalized.includes("risk") || normalized.includes("flag")) {
    return "I’m flagging high-risk tenders and will provide a risk-grade with a compliance recommendation for your team."
  }

  if (normalized.includes("tender") || normalized.includes("bid")) {
    return "I’m screening the latest tenders and matching them against your supplier profile, cost limits, and timeline requirements."
  }

  return "I’m reviewing your request now. I can help with approval workflows, compliance checks, budget flags, and decision-ready scoring."
}

export function AgentChat() {
  const [messages, setMessages] = useState<ChatMessage[]>(initialMessages)
  const [input, setInput] = useState("")
  const [isSending, setIsSending] = useState(false)

  const sendMessage = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!input.trim()) return

    const newMessage: ChatMessage = {
      id: `${Date.now()}-user`,
      sender: "user",
      text: input.trim(),
    }

    setMessages((current) => [...current, newMessage])
    setInput("")
    setIsSending(true)

    setTimeout(() => {
      const agentMessage: ChatMessage = {
        id: `${Date.now()}-agent`,
        sender: "agent",
        text: getBotResponse(input),
      }
      setMessages((current) => [...current, agentMessage])
      setIsSending(false)
    }, 650)
  }

  const agentAvatar = useMemo(() => "A", [])
  const userAvatar = useMemo(() => "P", [])

  return (
    <Card className="rounded-[32px] border border-white/10 bg-slate-950/80 p-6 shadow-card backdrop-blur-xl">
      <div className="mb-6 space-y-3">
        <span className="inline-flex rounded-full bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-200">
          AI procurement agent
        </span>
        <h2 className="text-2xl font-semibold text-white">Live procurement assistant</h2>
        <p className="max-w-3xl text-slate-400">
          Ask the agent about approvals, compliance, budget flags, and tender routing.
        </p>
      </div>

      <div className="space-y-4 rounded-[32px] border border-white/10 bg-slate-900/90 p-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex gap-3 rounded-[28px] p-4 ${
              message.sender === "agent" ? "bg-slate-950/80" : "ml-auto w-full max-w-xl bg-slate-800/80"
            }`}
          >
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-700 text-sm font-semibold text-emerald-200">
              {message.sender === "agent" ? agentAvatar : userAvatar}
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-2 text-sm font-semibold text-slate-100">
                <span>{message.sender === "agent" ? "Agent" : "Procurement Head"}</span>
                {message.tag ? (
                  <span className="rounded-full bg-emerald-500/10 px-2 py-1 text-xs text-emerald-200">
                    {message.tag}
                  </span>
                ) : null}
              </div>
              <p className="mt-2 text-sm leading-6 text-slate-300">{message.text}</p>
            </div>
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage} className="mt-6 flex flex-col gap-3 sm:flex-row">
        <input
          type="text"
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Type your procurement question..."
          className="min-w-0 flex-1 rounded-full border border-white/10 bg-slate-950/90 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20"
        />
        <Button type="submit" disabled={isSending || !input.trim()}>
          {isSending ? "Thinking..." : "Send"}
        </Button>
      </form>
    </Card>
  )
}
