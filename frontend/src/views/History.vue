<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-4xl font-bold text-gray-900 font-display">
        Emission History 📋
      </h1>
      <p class="text-gray-600 mt-2">View and manage all your logged emissions</p>
    </div>

    <!-- Filters -->
    <Card>
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Category
          </label>
          <select
            v-model="selectedCategory"
            class="input"
          >
            <option value="">All Categories</option>
            <option value="transport">Transport</option>
            <option value="energy">Energy</option>
            <option value="food">Food</option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Date From
          </label>
          <input
            v-model="dateFrom"
            type="date"
            class="input"
          />
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Date To
          </label>
          <input
            v-model="dateTo"
            type="date"
            class="input"
          />
        </div>
      </div>
    </Card>

    <!-- Entries List -->
    <Card>
      <div
        v-if="filteredEntries.length > 0"
        class="space-y-3"
      >
        <div
          v-for="entry in filteredEntries"
          :key="entry.id"
          class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition group"
        >
          <div class="flex-1">
            <p class="font-medium text-gray-900">
              {{ getCategoryIcon(entry.category) }} {{ entry.subcategory }}
            </p>
            <p class="text-sm text-gray-600">
              {{ entry.quantity }} {{ entry.unit }} • {{ formatDate(entry.date) }}
            </p>
            <p v-if="entry.notes" class="text-sm text-gray-500 mt-1">
              {{ entry.notes }}
            </p>
          </div>
          <div class="flex items-center gap-4">
            <div class="text-right">
              <p class="font-bold text-lg text-primary-600">
                {{ entry.co2_equivalent }}
              </p>
              <p class="text-xs text-gray-500">kg CO₂</p>
            </div>
            <button
              @click="deleteEntry(entry.id)"
              class="opacity-0 group-hover:opacity-100 transition text-red-600 hover:text-red-700 p-2"
              title="Delete"
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
      <div v-else class="text-center py-12 text-gray-500">
        <p class="text-lg">No emissions found matching your filters</p>
        <router-link to="/log" class="text-primary-600 hover:text-primary-700 mt-2 inline-block">
          Log your first emission →
        </router-link>
      </div>
    </Card>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-center gap-2">
      <button
        v-for="page in totalPages"
        :key="page"
        @click="currentPage = page"
        :class="[
          'px-3 py-2 rounded border',
          page === currentPage
            ? 'bg-primary-600 text-white border-primary-600'
            : 'bg-white text-gray-700 border-gray-300 hover:border-primary-600',
        ]"
      >
        {{ page }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useEmissionsStore } from '@/stores/emissions'
import Card from '@/components/Card.vue'
import type { EmissionEntry } from '@/types'

const emissionsStore = useEmissionsStore()

const currentPage = ref(1)
const selectedCategory = ref('')
const dateFrom = ref('')
const dateTo = ref('')
const pageSize = 10

const allEntries = ref<EmissionEntry[]>([])

const filteredEntries = computed(() => {
  return allEntries.value
    .filter((entry) => !selectedCategory.value || entry.category === selectedCategory.value)
    .filter((entry) => !dateFrom.value || entry.date >= dateFrom.value)
    .filter((entry) => !dateTo.value || entry.date <= dateTo.value)
    .slice((currentPage.value - 1) * pageSize, currentPage.value * pageSize)
})

const totalPages = computed(() => {
  return Math.ceil(allEntries.value.length / pageSize)
})

const getCategoryIcon = (category: string) => {
  const icons: Record<string, string> = {
    transport: '🚗',
    energy: '💡',
    food: '🍽️',
  }
  return icons[category] || '📊'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

const deleteEntry = async (id: string) => {
  if (confirm('Are you sure you want to delete this emission?')) {
    await emissionsStore.deleteEmission(id)
    allEntries.value = allEntries.value.filter((e) => e.id !== id)
  }
}

const loadData = async () => {
  await emissionsStore.getEmissions(0, 1000)
  allEntries.value = emissionsStore.entries
}

onMounted(() => {
  loadData()
})
</script>
