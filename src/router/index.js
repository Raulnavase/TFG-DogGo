import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'index',
      component: () => import('../views/IndexView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/owner-profile',
      name: 'owner-profile',
      component: () => import('../views/OwnerProfileView.vue'),
      meta: { requiresAuth: true, role: 'owner' },
    },
    {
      path: '/walker-profile',
      name: 'walker-profile',
      component: () => import('../views/WalkerProfileView.vue'),
      meta: { requiresAuth: true, role: 'walker' },
    },
    {
      path: '/active-walks',
      name: 'active-walks',
      component: () => import('../views/ActiveWalksView.vue'),
      meta: { requiresAuth: true, role: 'owner' },
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/ForgotPasswordView.vue'),
      meta: { requiresGuest: true },
    },
    {
      path: '/reset-password/:token',
      name: 'reset-password',
      component: () => import('../views/ResetPasswordView.vue'),
      meta: { requiresGuest: true },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  authStore.initializeAuth()

  const isAuthenticated = authStore.isLoggedIn
  const userRole = authStore.userRole

  if (to.meta.requiresGuest && isAuthenticated) {
    return next({ name: 'index' })
  }

  if (to.meta.requiresAuth && !isAuthenticated) {
    return next({ name: 'login' })
  }

  if (to.meta.role && to.meta.role !== userRole) {
    return next({ name: 'index' })
  }

  next()
})

export default router
