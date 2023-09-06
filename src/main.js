import { createApp } from 'vue'
// import VueRouter from 'vue-router'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

import router from './router'

loadFonts()

createApp(App)
.use(vuetify)
.use(router)
.mount('#app')
