<template>
  <span
    :class="[
      'badge',
      typeClasses,
      { 'opacity-50': locked },
    ]"
  >
    <span class="flex items-center gap-2">
      <span v-if="icon" class="text-lg">{{ icon }}</span>
      {{ label }}
    </span>
  </span>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  label: string
  type?: 'success' | 'warning' | 'error' | 'info'
  icon?: string
  locked?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  locked: false,
})

const typeClasses = computed(() => {
  const types = {
    success: 'badge-success',
    warning: 'badge-warning',
    error: 'badge-error',
    info: 'badge-info',
  }
  return types[props.type]
})
</script>
