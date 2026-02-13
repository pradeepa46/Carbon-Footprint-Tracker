<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 to-blue-50 flex items-center justify-center p-4">
    <div class="w-full max-w-md">
      <Card>
        <div class="text-center mb-8">
          <h1 class="text-3xl font-bold text-gray-900 font-display mb-2">
            🌱 Carbon Tracker
          </h1>
          <p class="text-gray-600">Login to your account</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Email
            </label>
            <input
              v-model="formData.email"
              type="email"
              class="input"
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              v-model="formData.password"
              type="password"
              class="input"
              placeholder="••••••••"
              required
            />
          </div>

          <Button
            type="submit"
            variant="primary"
            :disabled="isLoading"
            class="w-full"
          >
            {{ isLoading ? 'Signing in...' : 'Sign In' }}
          </Button>
        </form>

        <div class="mt-6 text-center">
          <p class="text-gray-600">
            Don't have an account?
            <router-link
              to="/register"
              class="text-primary-600 hover:text-primary-700 font-medium"
            >
              Sign up
            </router-link>
          </p>
        </div>

        <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p class="text-red-800 text-sm">{{ error }}</p>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Button from '@/components/Button.vue'
import Card from '@/components/Card.vue'

const router = useRouter()
const authStore = useAuthStore()

const formData = ref({
  email: '',
  password: '',
})

const isLoading = ref(false)
const error = ref('')

const handleLogin = async () => {
  isLoading.value = true
  error.value = ''

  try {
    await authStore.login(formData.value.email, formData.value.password)
    router.push('/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}
</script>
