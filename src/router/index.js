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
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/RegisterView.vue'),
    },
    {
      path: '/reset-password',
      name: 'reset-password',
      component: () => import('../views/ResetPasswordView.vue'),
    },
    {
      path: '/privacy',
      name: 'privacy',
      component: () => import('../views/PrivacyView.vue'),
    },
    {
      path: '/terms',
      name: 'terms',
      component: () => import('../views/TermsView.vue'),
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/ContactView.vue'),
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
      path: '/admin-panel',
      name: 'admin-panel',
      component: () => import('../views/AdminPanelView.vue'),
      meta: { requiresAuth: true, role: 'admin' },
    },
    {
      path: '/forgot-password',
      name: 'forgot-password',
      component: () => import('../views/ForgotPasswordView.vue'),
    },
    {
      path: '/:catchAll(.*)',
      name: 'NotFound',
      component: () => import('../views/NotFoundView.vue'),
    },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.meta.requiresAuth
  const requiredRole = to.meta.role

  if (authStore.isLoggedIn && (to.name === 'login' || to.name === 'register')) {
    if (authStore.userRole === 'admin') {
      next({ name: 'admin-panel' })
    } else if (authStore.userRole === 'owner') {
      next({ name: 'owner-profile' })
    } else if (authStore.userRole === 'walker') {
      next({ name: 'walker-profile' })
    } else {
      next('/')
    }
  } else if (requiresAuth && !authStore.isLoggedIn) {
    next('/login')
  } else if (requiresAuth && authStore.isLoggedIn) {
    if (requiredRole && authStore.userRole !== requiredRole) {
      alert('No tienes permiso para acceder a esta página.')
      if (authStore.userRole === 'admin') {
        next({ name: 'admin-panel' })
      } else if (authStore.userRole === 'owner') {
        next({ name: 'owner-profile' })
      } else if (authStore.userRole === 'walker') {
        next({ name: 'walker-profile' })
      } else {
        next('/')
      }
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router
