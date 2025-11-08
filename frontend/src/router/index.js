import { createRouter, createWebHistory } from 'vue-router'

import LandingView from '@/views/Landing/LandingView.vue'
import LoginView from '@/components/Auth/LoginView.vue'
import RegisterView from '@/components/Auth/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: LandingView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  // Si quieres una redirección por defecto:
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
]




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    // Para que al navegar siempre vuelva arriba
    return { top: 0 }
  }
})

export default router
