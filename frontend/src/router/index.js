import { createRouter, createWebHistory } from 'vue-router'
//import { Role } from '@/constants/roles'
import { useAuthStore } from '@/stores/auth'

import LandingView from '@/views/Landing/LandingView.vue'
import LoginView from '@/components/Auth/LoginView.vue'
import RegisterView from '@/components/Auth/RegisterView.vue'
import DashboardView from '@/views/DashBoard/DashboardView.vue'
import VerifyEmailView from '@/components/Auth/VerifyEmailView.vue'
import RequestPasswordResetView from '@/components/Auth/RequestPasswordResetView.vue'
import ResetPasswordView from '@/components/Auth/ResetPasswordView.vue'
import PendingApprovalView from '@/components/Auth/PendingApprovalView.vue'
import DashboardLayout from '@/components/Dashboard/layouts/DashboardLayout.vue'
import ProfileView from '@/views/DashBoard/ProfileView.vue'
import ResendVerificationView from '@/components/Auth/ResendVerificationView.vue'
import AdminDashboardView from '@/views/Admin/AdminDashboardView.vue'

import { Role } from '@/constants/roles'
import AdminUsersView from '@/views/Admin/AdminUsersView.vue'
import AdminPaymentsView from '@/views/Admin/AdminPaymentsView.vue' 
import UserPaymentsView from '@/views/Dashboard/UserPaymentsView.vue'
import AdminSeasonsView from '@/views/Admin/AdminSeasonsView.vue'
import AdminPrendasView from '@/views/Admin/AdminPrendasView.vue'
import UserMerchandiseView from '@/views/Dashboard/UserMerchandiseView.vue'


import PaymentSuccessView from '@/views/Dashboard/PaymentSuccessView.vue'
import PaymentCancelView from '@/views/Dashboard/PaymentCancelView.vue'
import OrderCommissionedView from '@/views/Dashboard/OrderCommissionedView.vue'

import UserOrdersView from '@/views/Dashboard/UserOrdersView.vue'
import AdminOrdersView from '@/views/Admin/AdminOrdersView.vue'
import AdminOrderSeasonsView from '@/views/Admin/AdminOrderSeasonsView.vue'


import AboutView from '@/views/Public/AboutView.vue'
import ContactView from '@/views/Public/ContactView.vue'
import PrivacyView from '@/views/Public/PrivacyView.vue'
import TermsView from '@/views/Public/TermsView.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: LandingView,
    meta: { requiresAuth: false }
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView,
    meta: { requiresAuth: false }
  },
  {
    path: '/contact',
    name: 'contact',
    component: ContactView,
    meta: { requiresAuth: false }
  },
  {
    path: '/privacy',
    name: 'privacy',
    component: PrivacyView,
    meta: { requiresAuth: false }
  },
  {
    path: '/terms',
    name: 'terms',
    component: TermsView,
    meta: { requiresAuth: false }
  },
  {
    path: '/resend-verification',
    name: 'resend-verification',
    component: ResendVerificationView,
    meta: { requiresAuth: false }
  },
{
    path: '/dashboard',
    component: DashboardLayout, // El layout con el sidebar
    meta: { requiresAuth: true }, // Protege todo el layout
    children: [
      {
        path: '', // Ruta por defecto (ej. /dashboard)
        name: 'dashboard',
        component: DashboardView,
      },
       {
         path: 'profile', // ej. /dashboard/profile
         name: 'profile',
         component: ProfileView,
       },
      {
        path: 'payments', // La URL es /dashboard/orders
        name: 'payments-history',
        component: UserPaymentsView // ¡Apunta a la nueva vista de CUOTAS!
      },
      {
        path: 'pedidos', // URL: /dashboard/pedidos
        name: 'user-orders-history', 
        component: UserOrdersView,
        meta: { requiresAuth: true }
      },
      {
        path: 'store', 
        name: 'merchandise-store', 
        component: UserMerchandiseView 
      },{
        path: 'payment/success', 
        name: 'payment-success', 
        component: PaymentSuccessView,
        meta: { requiresAuth: true }
      },
      
      // A esta ruta redirige Stripe si el PAGO (Cuota O Pedido) se CANCELA
      {
        path: 'payment/cancel', 
        name: 'payment-cancel', 
        component: PaymentCancelView,
        meta: { requiresAuth: true }
      },
      
      // A esta ruta redirigimos nosotros tras un ENCARGO manual
      {
        path: 'order/commissioned', 
        name: 'order-commissioned', 
        component: OrderCommissionedView,
        meta: { requiresAuth: true }
      },
      //   component: OrderHistoryView,
      // },
      // // --- Ruta solo para ADMIN ---
      {
        path: 'admin', // Ruta: /dashboard/admin
        name: 'admin-dashboard',
        component: AdminDashboardView,
        meta: { roles: [Role.ADMIN] }
      },
      {
        path: 'admin/users', // Ruta: /dashboard/admin/users
        name: 'admin-users',
        component: AdminUsersView,
        meta: { roles: [Role.ADMIN] }
      },
      {
        path: 'admin/orders', // Ruta: /dashboard/admin/orders
        name: 'admin-orders',
        component: AdminOrdersView,
        meta: { roles: [Role.ADMIN] }
      },
      {
        path: 'admin/payments', // Ruta: /dashboard/admin/payments
        name: 'admin-payments',
        component: AdminPaymentsView,
        meta: { roles: [Role.ADMIN] }
      },
      {
        path: 'admin/seasons',
        name: 'admin-seasons',
        component: AdminSeasonsView,
        meta: { roles: [Role.ADMIN] }
      },
        {
        path: 'admin/clothes',
        name: 'admin-clothes',
        component: AdminPrendasView,
        meta: { roles: [Role.ADMIN] }
      },
      {
        path: 'admin/orders/seasons', 
        name: 'admin-order-seasons',
        component: AdminOrderSeasonsView,
        meta: { roles: [Role.ADMIN] }
      }
    ]
  },
  {
    path: '/verify-email',
    name: 'verify-email',
    component: VerifyEmailView,
    meta: { requiresAuth: false } // Es una ruta pública
  },
  {
    path: '/request-password-reset',
    name: 'request-password-reset',
    component: RequestPasswordResetView,
    meta: { requiresAuth: false }
  },
  {

    path: '/reset-password',
    name: 'reset-password',
    component: ResetPasswordView,
    meta: { requiresAuth: false }
  },
  {
    path: '/pending-approval',
    name: 'pending-approval',
    component: PendingApprovalView,
    meta: { 
      requiresAuth: true // Importante: solo usuarios logueados pueden verla
    }
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



router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const { requiresAuth, roles } = to.meta

  const isAuthenticated = authStore.isAuthenticated // Simple boolean

  // --- 1. RUTAS PÚBLICAS (requiresAuth = false) ---
  if (!requiresAuth) {
    // Si intentas ir a Login/Register pero YA estás logueado
    if ((to.name === 'login' || to.name === 'register') && isAuthenticated) {
      // Mándalo al dashboard, porque si está logueado, ya está aprobado
      return next({ name: 'dashboard' }) 
    }
    // Si no, déjalo pasar (a Landing, etc.)
    return next()
  }

  // --- 2. RUTAS PROTEGIDAS (requiresAuth = true) ---
  
  // 2a. Si no está autenticado
  if (!isAuthenticated) {
    return next({ name: 'login' })
  }

  // 2b. Si ESTÁ autenticado (y por lo tanto, aprobado)
  // Comprobamos los roles
  if (roles && roles.length > 0) {
    if (authStore.user && roles.includes(authStore.user.rol)) {
      return next() // Rol coincide
    } else {
      return next({ name: 'home' }) // Rol NO coincide
    }
  }

  // Ruta protegida sin roles (ej. /perfil)
  return next()
})

export default router