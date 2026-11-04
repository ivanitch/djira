import './styles.css'
import { createApp } from 'vue'
import App from './App.vue'

// Находим контейнер. Если он есть на странице Django — монтируем Vue!
const el = document.getElementById('vue-app')
if (el) {
    createApp(App).mount('#vue-app')
}
