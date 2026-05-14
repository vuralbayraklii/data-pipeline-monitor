"""Router configuration."""
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../pages/HomePage.vue')
  },
  {
    path: '/datasets',
    name: 'Datasets',
    component: () => import('../pages/DatasetsPage.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
