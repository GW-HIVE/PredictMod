// Composables
import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue';

const routes = [
  {
    path: '/predictmod',
    component: Home,
  },
  {
    // TBD: How does the default View work? Poses an interesting question
    // path: '/about',
    // component: () => import('@/layouts/default/Default.vue'),
    // children: [
    //   {
    //     path: '',
    //     name: 'Home',
    //     // route level code-splitting
    //     // this generates a separate chunk (about.[hash].js) for this route
    //     // which is lazy-loaded when the route is visited.
    //     component: () => import(/* webpackChunkName: "home" */ '@/views/Home.vue'),
    //   },
    // ],
    // Following the example at `https://stackblitz.com/edit/vue3-vite-router-starter?file=src%2Frouter.js`
    // ...
    path: '/predictmod/about',
    component: () => import('../views/About.vue'),
  },
  {
    path: '/predictmod/faq',
    component: () => import('../views/FAQ.vue'),
  }, {
    path: '/predictmod/contact',
    component: () => import('../views/Contact.vue'),
  },
    {
      path: '/predictmod/ehr-home', 
      component: () => import('../views/EHRHome.vue'),
    },
    {
      path: '/predictmod/mg-home', 
      component: () => import('../views/MGHome.vue'),
    },
    {
      path: '/predictmod/login', 
      component: () => import('../views/Login.vue'),
    },
]

const router = createRouter({
  base: 'predictmod',
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
