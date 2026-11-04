import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve, dirname } from 'path'
import { fileURLToPath } from 'url'

// В твоем package.json указан "type": "module".
// В ES-модулях переменная __dirname по умолчанию не существует,
// поэтому её нужно объявить вручную, иначе при запуске Vite выдаст ReferenceError.
const __dirname = dirname(fileURLToPath(import.meta.url))

export default defineConfig({
  plugins: [vue()],

  base: '/static/',

  server: {
    host: '0.0.0.0',
    port: 5173,
    cors: {
        origin: '*', // разрешаем запросы с любых источников
        methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    },
    strictPort: true,
    origin: 'http://localhost:5173',
    hmr: {
      host: 'localhost',
    },
  },

  build: {
    outDir: resolve(__dirname, '../static/dist'),
    // true или 'manifest.json' — оба варианта валидны, но true является стандартом для Vite
    manifest: true,
    rollupOptions: {
      input: {
        // Vite сам подхватит styles.css из-за import './styles.css' внутри main.js
        main: resolve(__dirname, 'src/main.js')
      }
    }
  }
})
