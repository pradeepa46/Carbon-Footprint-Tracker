<template>
  <div class="flex flex-col items-center gap-4">
    <div class="relative w-40 h-40">
      <svg class="w-full h-full" viewBox="0 0 100 100">
        <!-- Background circle -->
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          stroke="#e5e7eb"
          stroke-width="8"
        />
        <!-- Progress circle -->
        <circle
          cx="50"
          cy="50"
          r="45"
          fill="none"
          :stroke="colorClass"
          stroke-width="8"
          stroke-dasharray="282.74"
          :stroke-dashoffset="strokeDashOffset"
          transform="rotate(-90 50 50)"
          class="transition-all duration-300"
        />
      </svg>
      <div
        class="absolute inset-0 flex flex-col items-center justify-center"
      >
        <p class="text-4xl font-bold text-gray-900 font-display">
          {{ displayPercentage }}%
        </p>
        <p class="text-sm text-gray-500 mt-1">{{ label }}</p>
      </div>
    </div>
    <div class="text-center">
      <p class="text-gray-600">
        <span class="font-bold">{{ current }}</span>
        / {{ total }} kg CO₂
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  current: number
  total: number
  label?: string
  color?: 'green' | 'blue' | 'orange'
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Monthly Goal',
  color: 'green',
})

const percentage = computed(() => {
  return Math.min((props.current / props.total) * 100, 100)
})

const displayPercentage = computed(() => {
  return Math.round(percentage.value)
})

const strokeDashOffset = computed(() => {
  const circumference = 282.74
  return circumference - (percentage.value / 100) * circumference
})

const colorClass = computed(() => {
  const colors = {
    green: '#10b981',
    blue: '#0ea5e9',
    orange: '#f97316',
  }
  return colors[props.color]
})
</script>
