import * as React from 'react'
import { cn } from '../../lib/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-[32px] border border-slate-200 bg-white p-6 shadow-sm',
        className,
      )}
      {...props}
    />
  )
}
