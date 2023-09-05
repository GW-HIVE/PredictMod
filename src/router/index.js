// Composables
import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue';

const routes = [
  {
    path: '/',
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
    path: '/about',
    component: () => import('../views/NotFound.vue'),
  },
  {
    path: '/faqs',
    component: () => import('../views/NotFound.vue'),
  }, {
    path: '/contact',
    component: () => import('../views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
