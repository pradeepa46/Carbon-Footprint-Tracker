<template>
  <div class="space-y-6">
    <!-- Header -->
    <div>
      <h1 class="text-4xl font-bold text-gray-900 font-display">
        Welcome, {{ authStore.user?.full_name }}! 👋
      </h1>
      <p class="text-gray-600 mt-2">Track and reduce your carbon footprint</p>
    </div>

    <!-- Main CTA -->
    <router-link to="/log" class="block">
      <Button variant="primary" class="w-full text-lg py-4">
        ➕ Log Your Emission
      </Button>
    </router-link>

    <!-- Monthly Summary Card -->
    <Card>
      <div class="text-center mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-6 font-display">
          Monthly CO₂ Summary
        </h2>
        <ProgressRing
          :current="breakdown?.breakdown.total || 0"
          :total="150"
          label="Monthly Budget"
          color="green"
        />
      </div>

      <div v-if="breakdown" class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-8 pt-8 border-t border-gray-200">
        <div class="text-center">
          <p class="text-sm text-gray-600">Daily Average</p>
          <p class="text-2xl font-bold text-gray-900 mt-1 font-display">
            {{ breakdown.summary.daily_average }} kg
          </p>
        </div>
        <div class="text-center">
          <p class="text-sm text-gray-600">Total This Month</p>
          <p class="text-2xl font-bold text-gray-900 mt-1 font-display">
            {{ breakdown.summary.total_co2_kg }} kg
          </p>
        </div>
        <div class="text-center">
          <p class="text-sm text-gray-600">Trend</p>
          <p
            :class="[
              'text-2xl font-bold mt-1 font-display',
              (breakdown.summary.trend || 0) > 0 ? 'text-red-600' : 'text-green-600',
            ]"
          >
            {{ (breakdown.summary.trend || 0) > 0 ? '🔴' : '🟢' }}
            {{ Math.abs(breakdown.summary.trend || 0) }}%
          </p>
        </div>
      </div>
    </Card>

    <!-- Stat Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <StatCard
        label="Transport"
        :value="breakdown?.breakdown.transport || 0"
        :icon="Zap"
        icon-color="blue"
        :trend="5"
      />
      <StatCard
        label="Energy"
        :value="breakdown?.breakdown.energy || 0"
        :icon="Lightbulb"
        icon-color="orange"
        :trend="-3"
      />
      <StatCard
        label="Food"
        :value="breakdown?.breakdown.food || 0"
        :icon="Utensils"
        icon-color="green"
        :trend="0"
      />
    </div>

    <!-- Breakdown Chart -->
    <Card v-if="breakdown">
      <h3 class="text-xl font-bold text-gray-900 mb-6 font-display">
        Emission Breakdown
      </h3>
      <Pie
        :data="chartData"
        :options="chartOptions"
        class="h-80"
      />
    </Card>

    <!-- Recent Emissions -->
    <Card>
      <h3 class="text-xl font-bold text-gray-900 mb-6 font-display">
        Recent Emissions
      </h3>
      <div
        v-if="recentEmissions.length > 0"
        class="space-y-4"
      >
        <div
          v-for="entry in recentEmissions.slice(0, 5)"
          :key="entry.id"
          class="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
        >
          <div>
            <p class="font-medium text-gray-900">
              {{ getCategoryIcon(entry.category) }} {{ entry.subcategory }}
            </p>
            <p class="text-sm text-gray-600">{{ formatDate(entry.date) }}</p>
          </div>
          <p class="font-bold text-primary-600">{{ entry.co2_equivalent }} kg</p>
        </div>
      </div>
      <div v-else class="text-center py-8 text-gray-500">
        <p>No emissions logged yet. Start by clicking "Log Your Emission"!</p>
      </div>
    </Card>

    <!-- Recommendations Preview -->
    <Card v-if="recommendations.length > 0">
      <h3 class="text-xl font-bold text-gray-900 mb-6 font-display">
        Recommended Actions
      </h3>
      <div class="space-y-3">
        <div
          v-for="rec in recommendations.slice(0, 3)"
          :key="rec.id"
          class="flex items-start gap-4 p-4 bg-gradient-to-r from-green-50 to-blue-50 rounded-lg border border-green-200"
        >
          <div class="flex-1">
            <p class="font-medium text-gray-900">{{ rec.action }}</p>
            <p class="text-sm text-gray-600 mt-1">{{ rec.description }}</p>
            <p class="text-sm font-semibold text-green-600 mt-2">
              💚 Save {{ rec.potential_savings }} kg CO₂/week
            </p>
          </div>
          <span
            :class="[
              'px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap',
              rec.difficulty === 'easy'
                ? 'bg-green-200 text-green-800'
                : rec.difficulty === 'medium'
                  ? 'bg-yellow-200 text-yellow-800'
                  : 'bg-red-200 text-red-800',
            ]"
          >
            {{ rec.difficulty }}
          </span>
        </div>
      </div>
      <router-link to="/recommendations" class="mt-4 block">
        <Button variant="ghost" class="w-full">
          View All Recommendations →
        </Button>
      </router-link>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useEmissionsStore } from '@/stores/emissions'
import api from '@/services/api'
import Card from '@/components/Card.vue'
import StatCard from '@/components/StatCard.vue'
import ProgressRing from '@/components/ProgressRing.vue'
import Button from '@/components/Button.vue'
import { Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import { Zap, Lightbulb, Utensils } from 'lucide-vue-next'
import type { EmissionBreakdownResponse, Recommendation } from '@/types'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const authStore = useAuthStore()
const emissionsStore = useEmissionsStore()

const breakdown = ref<EmissionBreakdownResponse | null>(null)
const recentEmissions = ref<any[]>([])
const recommendations = ref<Recommendation[]>([])
const isLoading = ref(true)

const chartData = ref({
  labels: ['Transport', 'Energy', 'Food'],
  datasets: [
    {
      data: [0, 0, 0],
      backgroundColor: ['#0ea5e9', '#f97316', '#10b981'],
      borderColor: ['#0284c7', '#c2410c', '#059669'],
      borderWidth: 2,
    },
  ],
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        padding: 20,
        font: { size: 14 },
      },
    },
  },
}

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

const loadData = async () => {
  try {
    const now = new Date()
    const [breakdownRes, historyRes, recsRes] = await Promise.all([
      emissionsStore.getBreakdown(now.getFullYear(), now.getMonth() + 1),
      emissionsStore.getEmissions(0, 10),
      api.getRecommendations(5),
    ])

    breakdown.value = breakdownRes
    recentEmissions.value = historyRes

    if (breakdown.value) {
      chartData.value.datasets[0].data = [
        breakdown.value.breakdown.transport,
        breakdown.value.breakdown.energy,
        breakdown.value.breakdown.food,
      ]
    }

    recommendations.value = recsRes.data.recommendations
  } catch (error) {
    console.error('Error loading data:', error)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
