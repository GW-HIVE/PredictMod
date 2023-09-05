import { createApp } from 'vue'
// import VueRouter from 'vue-router'
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'

import router from './router'

loadFonts()

// TBD : XXX? 
// const Home = { template: '<div>Home</div>'};
// const About = { template: '<div>About</div>'};
// const FAQ = { template: '<div>FAQ</div>'};
// const Contact = { template: '<div>foobar</div>'};

// const routes = [
//   { path: '/', component: Home },
//   { path: '/about', component: About },
//   { path: '/faq', component: FAQ },
//   { path: '/contact', component: Contact }
// ]

createApp(App)
.use(vuetify)
.use(router)
.mount('#app')
