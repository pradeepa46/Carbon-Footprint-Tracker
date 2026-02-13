<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Header -->
    <header class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <router-link to="/dashboard" class="flex items-center gap-2">
          <span class="text-2xl">🌱</span>
          <span class="text-xl font-bold text-gray-900 hidden sm:inline">
            Carbon Tracker
          </span>
        </router-link>

        <nav class="hidden md:flex items-center gap-6">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            :class="[
              'px-3 py-2 rounded-lg text-sm font-medium transition-colors',
              isActive(item.path)
                ? 'bg-primary-100 text-primary-700'
                : 'text-gray-600 hover:text-gray-900',
            ]"
          >
            {{ item.label }}
          </router-link>
        </nav>

        <!-- User Menu -->
        <div v-if="authStore.isAuthenticated" class="flex items-center gap-4">
          <router-link
            to="/profile"
            class="w-10 h-10 rounded-full bg-primary-200 text-primary-700 flex items-center justify-center font-bold hover:bg-primary-300 transition"
          >
            {{ authStore.user?.full_name?.[0] || 'U' }}
          </router-link>
        </div>
      </div>

      <!-- Mobile Navigation -->
      <div class="md:hidden border-t border-gray-200 px-4 py-3 flex justify-around">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          :class="[
            'flex flex-col items-center gap-1 px-3 py-2 text-xs font-medium transition-colors rounded',
            isActive(item.path)
              ? 'bg-primary-100 text-primary-700'
              : 'text-gray-600',
          ]"
        >
          <span class="text-lg">{{ item.icon }}</span>
          {{ item.label }}
        </router-link>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <router-view />
    </main>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-400 py-8 mt-16">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
        <p class="text-sm">
          🌍 Carbon Footprint Tracker - Making climate action accessible to everyone
        </p>
        <p class="text-xs mt-2">
          © 2026 All rights reserved. Data is encrypted and never sold.
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const navItems = [
  { path: '/dashboard', label: 'Dashboard', icon: '📊' },
  { path: '/log', label: 'Log', icon: '➕' },
  { path: '/history', label: 'History', icon: '📋' },
  { path: '/analytics', label: 'Analytics', icon: '📈' },
  { path: '/recommendations', label: 'Tips', icon: '💡' },
  { path: '/profile', label: 'Profile', icon: '⚙️' },
]

const isActive = (path: string) => {
  return router.currentRoute.value.path === path
}
</script>
