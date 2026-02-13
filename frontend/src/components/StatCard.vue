<template>
  <div class="bg-white rounded-xl shadow-md p-6 border border-gray-100 hover:shadow-lg transition-all">
    <div class="flex items-start justify-between mb-4">
      <div>
        <p class="text-sm text-gray-500 uppercase tracking-wide">{{ label }}</p>
        <h3
          class="text-3xl font-bold text-gray-900 mt-2 font-display animate-pulse-slow"
        >
          {{ formattedValue }}
        </h3>
      </div>
      <div
        class="p-3 rounded-lg"
        :class="iconBgClass"
      >
        <component :is="icon" :size="24" />
      </div>
    </div>

    <div v-if="trend !== undefined" class="flex items-center gap-2">
      <span
        class="text-sm font-medium"
        :class="trend > 0 ? 'text-red-600' : 'text-green-600'"
      >
        {{ trend > 0 ? '+' : '' }}{{ trend }}%
      </span>
      <span class="text-xs text-gray-500">vs last month</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { TrendingUp, TrendingDown } from 'lucide-vue-next'

interface Props {
  label: string
  value: number
  icon: any
  iconColor?: 'green' | 'blue' | 'orange' | 'red'
  trend?: number
  decimals?: number
}

const props = withDefaults(defineProps<Props>(), {
  iconColor: 'green',
  decimals: 1,
})

const formattedValue = computed(() => {
  return props.value.toFixed(props.decimals)
})

const iconBgClass = computed(() => {
  const colors = {
    green: 'bg-green-100 text-green-600',
    blue: 'bg-blue-100 text-blue-600',
    orange: 'bg-orange-100 text-orange-600',
    red: 'bg-red-100 text-red-600',
  }
  return colors[props.iconColor]
})
</script>
