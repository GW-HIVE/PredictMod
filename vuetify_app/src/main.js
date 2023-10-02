import { createApp } from 'vue'
// import VueRouter from 'vue-router'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

import 'vite/modulepreload-polyfill'

import router from './router'

loadFonts()

// S/O to the rescue: https://stackoverflow.com/a/74861436
router.onError((error, to) => {
    console.log('---> Router captured error!');
    if (error.message.includes('error loading dynamically imported module') ||
        error.message.includes('Failed to fetch dynamically imported module') || 
        error.message.includes('Importing a module script failed')) {
            window.location = to.fullPath;
        }
})

createApp(App)
.use(vuetify)
.use(router)
.mount('#app')
