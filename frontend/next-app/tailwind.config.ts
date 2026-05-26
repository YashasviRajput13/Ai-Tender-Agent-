import type { Config } from 'tailwindcss'

const config: Config = {
  content: ['./app/**/*.{js,ts,jsx,tsx}', './components/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        surface: '#0b1220',
        'surface-2': '#0f1a35',
        'surface-3': '#182440',
        glow: '#5d7cff',
        accent: '#7c3aed',
        muted: '#94a3b8',
      },
      boxShadow: {
        glow: '0 18px 80px rgba(92, 70, 255, 0.18)',
        card: '0 20px 70px rgba(3, 5, 18, 0.35)',
      },
      backgroundImage: {
        'dashboard-gradient': 'radial-gradient(circle at top left, rgba(124, 58, 237, 0.26), transparent 35%), radial-gradient(circle at bottom right, rgba(59, 130, 246, 0.2), transparent 30%)',
      },
    },
  },
  plugins: [],
}

export default config
