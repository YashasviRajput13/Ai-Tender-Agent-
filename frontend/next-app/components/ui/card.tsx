import * as React from 'react'
import { cn } from '../../lib/utils'

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {}

export function Card({ className, ...props }: CardProps) {
  return (
    <div
      className={cn(
        'rounded-[32px] border border-white/10 bg-white/5 p-6 shadow-card backdrop-blur-xl',
        className,
      )}
      {...props}
    />
  )
}
