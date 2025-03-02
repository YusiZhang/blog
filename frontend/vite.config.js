import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000, // development server port
    proxy: {
      '/api': { // proxy to backend
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
});