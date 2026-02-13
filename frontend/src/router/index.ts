import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import MainLayout from '@/layouts/MainLayout.vue'
import Login from '@/views/Auth/Login.vue'
import Register from '@/views/Auth/Register.vue'
import Dashboard from '@/views/Dashboard.vue'
import LogEmission from '@/views/LogEmission.vue'
import History from '@/views/History.vue'
import Analytics from '@/views/Analytics.vue'
import Recommendations from '@/views/Recommendations.vue'
import Profile from '@/views/Profile.vue'

const routes = [
  {
    path: '/',
    redirect: '/dashboard',
  },
  {
    path: '/login',
    component: Login,
    meta: { requiresAuth: false },
  },
  {
    path: '/register',
    component: Register,
    meta: { requiresAuth: false },
  },
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'dashboard',
        component: Dashboard,
        meta: { title: 'Dashboard' },
      },
      {
        path: 'log',
        component: LogEmission,
        meta: { title: 'Log Emission' },
      },
      {
        path: 'history',
        component: History,
        meta: { title: 'History' },
      },
      {
        path: 'analytics',
        component: Analytics,
        meta: { title: 'Analytics' },
      },
      {
        path: 'recommendations',
        component: Recommendations,
        meta: { title: 'Recommendations' },
      },
      {
        path: 'profile',
        component: Profile,
        meta: { title: 'Profile' },
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  const requiresAuth = to.meta.requiresAuth !== false

  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (!requiresAuth && authStore.isAuthenticated && (to.path === '/login' || to.path === '/register')) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
