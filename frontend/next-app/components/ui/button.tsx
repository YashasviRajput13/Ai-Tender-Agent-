import * as React from 'react'
import { cn } from '../../lib/utils'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'ghost'
}

export function Button({ className, variant = 'primary', ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-full px-5 py-2.5 text-sm font-semibold transition focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-400/50',
        variant === 'primary'
          ? 'bg-gradient-to-r from-blue-500 via-violet-500 to-fuchsia-500 text-white shadow-glow hover:brightness-110'
          : 'bg-white/5 text-slate-100 hover:bg-white/10',
        className,
      )}
      {...props}
    />
  )
}
