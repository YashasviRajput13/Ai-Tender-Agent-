import { Card } from "./ui/card"

const features = [
  {
    title: "Submission Evaluation",
    description:
      "Ensure accurate and objective scoring with AI-driven evaluation of submissions.",
  },
  {
    title: "Compliance Verification",
    description:
      "Automate compliance checks to meet legal and regulatory standards.",
  },
  {
    title: "Dynamic Scoring & Ranking",
    description:
      "Automatically rank submissions by cost, quality, and timelines for better decisions.",
  },
]

export function LandingFeatures() {
  return (
    <section className="space-y-8 rounded-[32px] border border-white/10 bg-slate-900/70 p-6 shadow-xl backdrop-blur-xl">
      <div className="space-y-4">
        <p className="text-sm font-medium uppercase tracking-[0.24em] text-emerald-300">
          Procurement intelligence
        </p>
        <h2 className="text-3xl font-semibold text-white sm:text-4xl">
          Smarter tender decisions with AI-assisted evaluation and routing
        </h2>
        <p className="max-w-3xl text-slate-300">
          Bring submission scoring, compliance checks, and ranking into a single
          workflow. Our interface makes it easy to understand which bids are
          ready for approval and which require extra scrutiny.
        </p>
      </div>

      <div className="grid gap-4 lg:grid-cols-3">
        {features.map((feature) => (
          <Card
            key={feature.title}
            className="border-emerald-400/10 bg-emerald-50/5 p-6 text-slate-100"
          >
            <div className="space-y-3">
              <p className="text-lg font-semibold text-white">{feature.title}</p>
              <p className="text-sm leading-6 text-slate-300">{feature.description}</p>
            </div>
          </Card>
        ))}
      </div>

      <Card className="overflow-hidden border-emerald-400/20 bg-gradient-to-r from-emerald-900/20 via-slate-950/70 to-slate-950/80 p-6">
        <div className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-4">
            <span className="inline-flex rounded-full bg-emerald-500/10 px-3 py-1 text-sm font-medium text-emerald-200">
              AI procurement agent
            </span>
            <h3 className="text-2xl font-semibold text-white">
              Conversational decision support for procurement approvals
            </h3>
            <p className="max-w-xl text-slate-300">
              See an agent-style workflow that tracks bid evaluation, compliance checks,
              and final routing through approval.
            </p>

            <div className="space-y-4 rounded-[32px] border border-white/10 bg-slate-950/80 p-5 shadow-2xl">
              <div className="space-y-4">
                <div className="flex items-center gap-3 rounded-[28px] border border-white/10 bg-slate-100/10 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-700 text-sm font-semibold text-white">
                    P
                  </div>
                  <div>
                    <p className="text-sm font-semibold text-slate-100">Procurement Head</p>
                    <p className="text-sm text-slate-400">
                      Can the system integrate bid evaluations with our approval workflow?
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-[32px] border border-emerald-400/20 bg-emerald-500/10 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-sm font-semibold text-slate-950">
                    A
                  </div>
                  <div className="space-y-2">
                    <span className="inline-flex rounded-full bg-slate-950/80 px-3 py-1 text-xs uppercase tracking-[0.24em] text-slate-300">
                      Processing
                    </span>
                    <p className="text-sm font-semibold text-white">
                      Yes! I’ve mapped vendor rankings to your approval chain.
                    </p>
                  </div>
                </div>

                <div className="flex justify-end">
                  <div className="flex items-center gap-3 rounded-[28px] border border-white/10 bg-slate-900/80 p-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-700 text-sm font-semibold text-emerald-300">
                      P
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-white">Procurement Head</p>
                      <p className="text-sm text-slate-400">Any bids needing extra scrutiny?</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-[32px] border border-white/10 bg-slate-100/5 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-sm font-semibold text-slate-950">
                    A
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm font-semibold text-white">Two bids exceed the budget threshold.</p>
                    <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-200">
                      <span className="h-2.5 w-2.5 rounded-full bg-emerald-300" />
                      Flagged for Review
                    </div>
                  </div>
                </div>

                <div className="flex justify-end">
                  <div className="flex items-center gap-3 rounded-[28px] border border-white/10 bg-slate-900/80 p-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-700 text-sm font-semibold text-emerald-300">
                      P
                    </div>
                    <div>
                      <p className="text-sm font-semibold text-white">Route top bids for final approval.</p>
                    </div>
                  </div>
                </div>

                <div className="flex items-start gap-3 rounded-[32px] border border-emerald-400/20 bg-emerald-500/10 p-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-sm font-semibold text-slate-950">
                    A
                  </div>
                  <div className="space-y-2">
                    <p className="text-sm font-semibold text-white">Done! Decision-ready report sent to stakeholders.</p>
                    <div className="inline-flex rounded-full bg-slate-950/80 px-3 py-1 text-xs text-slate-400">
                      Routing approved
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-col justify-between rounded-[32px] border border-white/10 bg-slate-950/90 p-6 text-slate-200">
            <div className="space-y-3">
              <p className="text-sm uppercase tracking-[0.24em] text-emerald-300">Agent summary</p>
              <h4 className="text-xl font-semibold text-white">Workflow at a glance</h4>
              <p className="text-sm text-slate-400">
                Intelligent screening, compliance flags, and approval routing all in one
                agent-driven view.
              </p>
            </div>
            <div className="grid gap-4">
              <div className="rounded-3xl bg-slate-900/80 p-4">
                <p className="text-sm font-medium text-emerald-200">Budget-exceeded bids flagged</p>
              </div>
              <div className="rounded-3xl bg-slate-900/80 p-4">
                <p className="text-sm text-slate-300">Approval workflow integrated with vendor scoring</p>
              </div>
              <div className="rounded-3xl bg-slate-900/80 p-4">
                <p className="text-sm text-slate-300">Final report ready for stakeholders</p>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </section>
  )
}
