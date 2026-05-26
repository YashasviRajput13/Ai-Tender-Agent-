export const statsCards = [
  {
    title: 'Total Tenders',
    value: '148',
    change: '+14.2%',
    icon: 'Briefcase',
    accent: 'from-blue-500 to-indigo-500',
  },
  {
    title: 'Active Tenders',
    value: '72',
    change: '+8.7%',
    icon: 'Layers',
    accent: 'from-cyan-500 to-sky-500',
  },
  {
    title: 'High Match Opportunities',
    value: '19',
    change: '+26.9%',
    icon: 'Sparkles',
    accent: 'from-violet-500 to-fuchsia-500',
  },
  {
    title: 'Upcoming Deadlines',
    value: '11',
    change: '-3.2%',
    icon: 'Clock',
    accent: 'from-amber-400 to-orange-500',
  },
  {
    title: 'Risk Alerts',
    value: '7',
    change: '+2.4%',
    icon: 'ShieldAlert',
    accent: 'from-rose-500 to-pink-500',
  },
]

export const categoryDistribution = [
  { name: 'Construction', value: 34 },
  { name: 'IT Services', value: 22 },
  { name: 'Healthcare', value: 15 },
  { name: 'Energy', value: 13 },
  { name: 'Logistics', value: 16 },
]

export const monthlyTrendData = [
  { month: 'Jan', tenders: 20 },
  { month: 'Feb', tenders: 25 },
  { month: 'Mar', tenders: 42 },
  { month: 'Apr', tenders: 38 },
  { month: 'May', tenders: 51 },
  { month: 'Jun', tenders: 48 },
  { month: 'Jul', tenders: 62 },
  { month: 'Aug', tenders: 55 },
  { month: 'Sep', tenders: 68 },
  { month: 'Oct', tenders: 74 },
  { month: 'Nov', tenders: 81 },
  { month: 'Dec', tenders: 94 },
]

export const matchScoreData = [
  { name: '0-40%', score: 18 },
  { name: '40-60%', score: 34 },
  { name: '60-80%', score: 46 },
  { name: '80-100%', score: 82 },
]

export type TenderRiskLevel = 'Low' | 'Medium' | 'High'

export type TenderRow = {
  name: string
  organization: string
  budget: string
  deadline: string
  matchScore: string
  riskLevel: TenderRiskLevel
}

export const tenderRows: TenderRow[] = [
  {
    name: 'Metro Rail Expansion',
    organization: 'Praxis Infrastructure',
    budget: '$4.2M',
    deadline: '2026-06-14',
    matchScore: '89%',
    riskLevel: 'Medium',
  },
  {
    name: 'Healthcare ERP Deployment',
    organization: 'Healthline Systems',
    budget: '$1.3M',
    deadline: '2026-06-22',
    matchScore: '75%',
    riskLevel: 'Low',
  },
  {
    name: 'Solar Farm Rollout',
    organization: 'Bright Energy',
    budget: '$2.7M',
    deadline: '2026-07-08',
    matchScore: '93%',
    riskLevel: 'High',
  },
  {
    name: 'State Tax Portal',
    organization: 'UrbanTech Labs',
    budget: '$890K',
    deadline: '2026-07-19',
    matchScore: '81%',
    riskLevel: 'Medium',
  },
]

export const recommendations = [
  {
    name: 'Digital Hospital Network',
    value: '$1.8M',
    matchScore: '92%',
    risk: 'Low',
    deadline: '2026-06-28',
  },
  {
    name: 'Statewide Data Center',
    value: '$3.4M',
    matchScore: '88%',
    risk: 'Medium',
    deadline: '2026-07-12',
  },
  {
    name: 'Smart Transit Audit',
    value: '$710K',
    matchScore: '83%',
    risk: 'Low',
    deadline: '2026-08-03',
  },
]

export type NotificationType = 'new' | 'deadline' | 'risk'

export const notifications: Array<{
  title: string
  description: string
  type: NotificationType
  time: string
}> = [
  {
    title: 'New tender added: Smart City Planning',
    description: 'A high-value infrastructure opportunity was discovered today.',
    type: 'new',
    time: '2m ago',
  },
  {
    title: 'Deadline warning: Metro Rail Expansion',
    description: 'Submission deadline is in 4 days. Review proposal assets.',
    type: 'deadline',
    time: '22m ago',
  },
  {
    title: 'AI risk alert: Solar Farm Rollout',
    description: 'Projected delivery risk has increased due to labor constraints.',
    type: 'risk',
    time: '1h ago',
  },
]
