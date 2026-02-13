<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-4xl font-bold text-gray-900 font-display">
        Analytics & Insights 📊
      </h1>
      <p class="text-gray-600 mt-2">Track your progress and see where your emissions come from</p>
    </div>

    <!-- Period Selector -->
    <Card>
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Year
          </label>
          <select
            v-model.number="selectedYear"
            @change="loadData"
            class="input"
          >
            <option v-for="year in yearOptions" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
        <div class="flex-1">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Month
          </label>
          <select
            v-model.number="selectedMonth"
            @change="loadData"
            class="input"
          >
            <option
              v-for="(name, idx) in monthNames"
              :key="idx"
              :value="idx + 1"
            >
              {{ name }}
            </option>
          </select>
        </div>
      </div>
    </Card>

    <!-- Breakdown Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <Card>
        <h3 class="text-sm text-gray-600 uppercase tracking-wide mb-2">
          🚗 Transport
        </h3>
        <p class="text-3xl font-bold text-blue-600 font-display">
          {{ breakdown?.breakdown.transport.toFixed(1) || 0 }} kg
        </p>
        <p class="text-sm text-gray-500 mt-2">
          {{ ((breakdown?.breakdown.transport || 0) / (breakdown?.breakdown.total || 1) * 100).toFixed(0) }}%
          of total
        </p>
      </Card>

      <Card>
        <h3 class="text-sm text-gray-600 uppercase tracking-wide mb-2">
          ⚡ Energy
        </h3>
        <p class="text-3xl font-bold text-orange-600 font-display">
          {{ breakdown?.breakdown.energy.toFixed(1) || 0 }} kg
        </p>
        <p class="text-sm text-gray-500 mt-2">
          {{ ((breakdown?.breakdown.energy || 0) / (breakdown?.breakdown.total || 1) * 100).toFixed(0) }}%
          of total
        </p>
      </Card>

      <Card>
        <h3 class="text-sm text-gray-600 uppercase tracking-wide mb-2">
          🍽️ Food
        </h3>
        <p class="text-3xl font-bold text-green-600 font-display">
          {{ breakdown?.breakdown.food.toFixed(1) || 0 }} kg
        </p>
        <p class="text-sm text-gray-500 mt-2">
          {{ ((breakdown?.breakdown.food || 0) / (breakdown?.breakdown.total || 1) * 100).toFixed(0) }}%
          of total
        </p>
      </Card>
    </div>

    <!-- Pie Chart -->
    <Card v-if="breakdown">
      <h3 class="text-xl font-bold text-gray-900 mb-6 font-display">
        Emissions Breakdown
      </h3>
      <Pie
        :data="chartData"
        :options="chartOptions"
        class="h-80"
      />
    </Card>

    <!-- Monthly Trend -->
    <Card>
      <h3 class="text-xl font-bold text-gray-900 mb-6 font-display">
        Last 12 Months
      </h3>
      <div class="space-y-4">
        <div
          v-for="(month, idx) in monthlyData"
          :key="idx"
          class="flex items-center gap-4"
        >
          <div class="w-24 text-sm font-medium text-gray-700">
            {{ monthNames[idx] }}
          </div>
          <div class="flex-1">
            <div class="bg-gray-200 rounded-full h-8 overflow-hidden flex items-center">
              <div
                :style="{ width: `${(month / maxMonthlyValue) * 100}%` }"
                :class="[
                  'h-full rounded-full transition-all',
                  idx === selectedMonth - 1 ? 'bg-primary-600' : 'bg-blue-400',
                ]"
              ></div>
            </div>
          </div>
          <div class="w-16 text-right text-sm font-medium">
            {{ month.toFixed(0) }} kg
          </div>
        </div>
      </div>
    </Card>

    <!-- Daily Average -->
    <Card>
      <h3 class="text-sm text-gray-600 uppercase tracking-wide mb-4">
        Daily Average
      </h3>
      <p class="text-4xl font-bold text-primary-600 font-display">
        {{ breakdown?.summary.daily_average.toFixed(2) || 0 }} kg
      </p>
      <p class="text-gray-600 mt-2">
        per day in {{ monthNames[selectedMonth - 1] }}
      </p>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useEmissionsStore } from '@/stores/emissions'
import Card from '@/components/Card.vue'
import { Pie } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js'
import type { EmissionBreakdownResponse } from '@/types'

ChartJS.register(Title, Tooltip, Legend, ArcElement)

const emissionsStore = useEmissionsStore()

const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December',
]

const now = new Date()
const selectedYear = ref(now.getFullYear())
const selectedMonth = ref(now.getMonth() + 1)

const yearOptions = computed(() => {
  const years = []
  for (let i = now.getFullYear(); i >= 2020; i--) {
    years.push(i)
  }
  return years
})

const breakdown = ref<EmissionBreakdownResponse | null>(null)
const monthlyData = ref<number[]>(Array(12).fill(0))

const maxMonthlyValue = computed(() => Math.max(...monthlyData.value, 1))

const chartData = computed(() => ({
  labels: ['Transport', 'Energy', 'Food'],
  datasets: [
    {
      data: [
        breakdown.value?.breakdown.transport || 0,
        breakdown.value?.breakdown.energy || 0,
        breakdown.value?.breakdown.food || 0,
      ],
      backgroundColor: ['#0ea5e9', '#f97316', '#10b981'],
      borderColor: ['#0284c7', '#c2410c', '#059669'],
      borderWidth: 2,
    },
  ],
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: { padding: 20, font: { size: 14 } },
    },
  },
}

const loadData = async () => {
  const result = await emissionsStore.getBreakdown(selectedYear.value, selectedMonth.value)
  breakdown.value = result

  // Load all months for the year
  for (let month = 1; month <= 12; month++) {
    const monthBreakdown = await emissionsStore.getBreakdown(selectedYear.value, month)
    monthlyData.value[month - 1] = monthBreakdown.breakdown.total
  }
}

onMounted(() => {
  loadData()
})
</script>
