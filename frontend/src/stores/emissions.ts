import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'
import type { EmissionEntry, EmissionBreakdownResponse } from '@/types'

export const useEmissionsStore = defineStore('emissions', () => {
  const entries = ref<EmissionEntry[]>([])
  const breakdown = ref<EmissionBreakdownResponse | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const getEmissions = async (skip = 0, limit = 50, category?: string) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.getEmissionHistory(skip, limit, category)
      entries.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to load emissions'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const getBreakdown = async (year?: number, month?: number) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.getEmissionBreakdown(year, month)
      breakdown.value = response.data
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to load breakdown'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const addEmission = async (data: {
    category: string
    subcategory: string
    quantity: number
    unit: string
    date: string
    notes?: string
  }) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.createEmission(data)
      entries.value.unshift(response.data)
      // Refresh breakdown
      const now = new Date()
      await getBreakdown(now.getFullYear(), now.getMonth() + 1)
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to add emission'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const updateEmission = async (id: string, data: any) => {
    isLoading.value = true
    error.value = null

    try {
      const response = await api.updateEmission(id, data)
      const index = entries.value.findIndex((e) => e.id === id)
      if (index !== -1) {
        entries.value[index] = response.data
      }
      return response.data
    } catch (err: any) {
      error.value = err.message || 'Failed to update emission'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const deleteEmission = async (id: string) => {
    isLoading.value = true
    error.value = null

    try {
      await api.deleteEmission(id)
      entries.value = entries.value.filter((e) => e.id !== id)
    } catch (err: any) {
      error.value = err.message || 'Failed to delete emission'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    entries,
    breakdown,
    isLoading,
    error,
    getEmissions,
    getBreakdown,
    addEmission,
    updateEmission,
    deleteEmission,
  }
})
