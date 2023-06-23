import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import installElementPlus from './plugins/element'
import './assets/css/dr-comm.css'
import '@/tools/global'

const app = createApp(App)
installElementPlus(app)
app.use(store).use(router).mount('#app')