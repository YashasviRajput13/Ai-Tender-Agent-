import { dirname } from 'path'
import { fileURLToPath } from 'url'

const __dirname = dirname(fileURLToPath(import.meta.url))

const nextConfig = {
  typedRoutes: false,
  reactStrictMode: true,
  outputFileTracingRoot: __dirname,
}

export default nextConfig
