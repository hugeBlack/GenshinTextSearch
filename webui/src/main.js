import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import '@flaticon/flaticon-uicons/css/all/all.css'
import "@/assets/main.css";
import '@/assets/misans.css'

import App from './App.vue'
import router from './router'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'

const app = createApp(App)
app.use(ElementPlus, {
    locale: zhCn
})

app.use(router)

app.mount('#app')


