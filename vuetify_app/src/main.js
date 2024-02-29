import { createApp } from 'vue';
import App from './App.vue';
import vuetify from './plugins/vuetify';
import { loadFonts } from './plugins/webfontloader';

import { createPinia } from 'pinia';

import 'vite/modulepreload-polyfill'

import router from './router'

const pinia = createPinia();

loadFonts()
// XXX
// console.log("===> Process ENV: %s", JSON.stringify(import.meta.env));
// console.log("=>>> PROD?%s \nDEV? %s\nMODE? %s", import.meta.env.PROD, import.meta.env.DEV, import.meta.env.MODE);

// S/O to the rescue: https://stackoverflow.com/a/74861436
router.onError((error, to) => {
    console.log('---> Router captured error!');
    if (error.message.includes('error loading dynamically imported module') ||
        error.message.includes('Failed to fetch dynamically imported module') || 
        error.message.includes('Importing a module script failed')) {
            window.location = to.fullPath;
    } else {
        console.log('--> Error was %s', error);
    }
})

createApp(App)
.use(vuetify)
.use(router)
.use(pinia)
.mount('#app')
