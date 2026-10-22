import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 开发期：Vue 5173 -> 代理 Django 8000 的 /api 接口
// 演示期：npm run build 产出 dist，由 Django 托管，同源无需代理
export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: '127.0.0.1',
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
