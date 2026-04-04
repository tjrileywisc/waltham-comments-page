import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [
    react({
      include: '**/*.{jsx,js}',
    }),
  ],
  server: {
    proxy: {
      '/api': 'http://localhost:8001',
      '/transcript': 'http://localhost:8001',
      '/search': 'http://localhost:8001',
    },
  },
})
