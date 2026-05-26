import * as React from 'react'
import { cn } from '../../lib/utils'

interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
}

const variants: Record<NonNullable<BadgeProps['variant']>, string> = {
  default: 'bg-white/5 text-slate-100',
  success: 'bg-emerald-500/15 text-emerald-300',
  warning: 'bg-amber-500/15 text-amber-300',
  danger: 'bg-rose-500/15 text-rose-300',
  info: 'bg-sky-500/15 text-sky-300',
}

export function Badge({ className, variant = 'default', ...props }: BadgeProps) {
  return (
    <span
      className={cn(
        'inline-flex rounded-full px-3 py-1 text-xs font-semibold uppercase tracking-[0.24em] ring-1 ring-white/10',
        variants[variant],
        className,
      )}
      {...props}
    />
  )
}
