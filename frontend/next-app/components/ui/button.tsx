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
          ? 'bg-blue-600 text-white shadow-sm hover:bg-blue-700'
          : 'bg-slate-100 text-slate-900 hover:bg-slate-200',
        className,
      )}
      {...props}
    />
  )
}
