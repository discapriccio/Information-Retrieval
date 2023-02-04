import router from './router'
import { createApp } from 'vue'

import App from './App.vue'

const app = createApp(App)
app.use(router)
app.mount('#app')

// 跳转界面后到顶部
router.beforeEach((to, from, next) => {
    // chrome
    document.body.scrollTop = 0
    // firefox
    document.documentElement.scrollTop = 0
    // safari
    window.pageYOffset = 0
    next()
  })