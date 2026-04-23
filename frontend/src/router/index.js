import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Consult from '../views/Consult.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/consult',
    name: 'Consult',
    component: Consult
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
