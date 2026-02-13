import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import type { User } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  const initializeFromStorage = () => {
    const storedToken = localStorage.getItem('access_token')
    const storedUserId = localStorage.getItem('user_id')

    if (storedToken && storedUserId) {
      token.value = storedToken
      // Load full user data from API
      loadCurrentUser()
    }
  }

  const register = async (email: string, password: string, fullName: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.register(email, password, fullName)
      user.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Registration failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const login = async (email: string, password: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.login(email, password)
      token.value = response.data.access_token
      localStorage.setItem('access_token', response.data.access_token)
      localStorage.setItem('user_id', response.data.user_id)

      // Load full user data
      await loadCurrentUser()
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Login failed'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const loadCurrentUser = async () => {
    try {
      const response = await api.getCurrentUser()
      user.value = response.data
    } catch (err) {
      console.error('Failed to load current user', err)
    }
  }

  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('user_id')
    error.value = null
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    register,
    login,
    logout,
    initializeFromStorage,
    loadCurrentUser,
  }
})
