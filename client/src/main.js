import { createApp } from 'vue';
import App from './App.vue'
import router from './router'

// Vue.use(PiniaVuePlugin)
// const pinia = createPinia()

createApp(App).use(router).mount('#app')
