<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-4xl font-bold text-gray-900 font-display">
        Recommended Actions 💡
      </h1>
      <p class="text-gray-600 mt-2">
        Personalized tips to reduce your carbon footprint
      </p>
    </div>

    <!-- Total Savings -->
    <Card>
      <div class="text-center">
        <p class="text-sm text-gray-600 uppercase tracking-wide mb-2">
          Total Potential Savings
        </p>
        <p class="text-4xl font-bold text-green-600 font-display">
          {{ totalSavings.toFixed(1) }} kg CO₂
        </p>
        <p class="text-gray-600 mt-2">per week if you adopt all recommendations</p>
      </div>
    </Card>

    <!-- Recommendations by Priority -->
    <div v-if="recommendations.length > 0" class="space-y-6">
      <div v-for="priority in ['high', 'medium', 'low']" :key="priority">
        <h3
          v-if="recommendationsByPriority[priority].length > 0"
          class="text-lg font-bold text-gray-900 mb-4 capitalize font-display"
        >
          {{ priority === 'high' ? '🔴' : priority === 'medium' ? '🟡' : '🟢' }}
          {{ priority }} Priority
        </h3>

        <div
          v-for="rec in recommendationsByPriority[priority]"
          :key="rec.id"
          class="card group cursor-pointer hover:shadow-lg transition-all"
        >
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <h4 class="text-xl font-bold text-gray-900 mb-2">{{ rec.action }}</h4>
              <p class="text-gray-600 mb-3">{{ rec.description }}</p>

              <!-- Stats -->
              <div class="flex flex-wrap gap-4 mb-4">
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Savings</p>
                  <p class="text-lg font-bold text-green-600">
                    {{ rec.potential_savings }} kg CO₂/week
                  </p>
                </div>
                <div>
                  <p class="text-xs text-gray-500 uppercase tracking-wide">Difficulty</p>
                  <Badge
                    :label="rec.difficulty"
                    :type="
                      rec.difficulty === 'easy'
                        ? 'success'
                        : rec.difficulty === 'medium'
                          ? 'warning'
                          : 'error'
                    "
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Progress (mockup) -->
          <div class="pt-4 border-t border-gray-200">
            <div class="flex items-center justify-between mb-2">
              <p class="text-xs font-medium text-gray-600">Your progress</p>
              <p class="text-xs font-bold text-gray-900">2/4 steps completed</p>
            </div>
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class="h-full bg-green-500 rounded-full"
                :style="{ width: '50%' }"
              ></div>
            </div>
          </div>

          <!-- Action Button -->
          <Button variant="ghost" class="w-full mt-4 justify-center">
            ✓ Mark as Adopted
          </Button>
        </div>
      </div>
    </div>

    <!-- No Recommendations -->
    <div v-else class="text-center py-12">
      <p class="text-lg text-gray-600 mb-4">
        You're doing great! Keep tracking your emissions to get recommendations.
      </p>
      <router-link to="/log">
        <Button variant="primary">Log Your First Emission</Button>
      </router-link>
    </div>

    <!-- Achievements Section -->
    <Card>
      <h3 class="text-xl font-bold text-gray-900 mb-6 font-display">
        🏆 Achievements
      </h3>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div
          v-for="badge in availableBadges"
          :key="badge.id"
          :class="[
            'p-4 rounded-lg border-2 text-center transition',
            badge.earned
              ? 'bg-yellow-50 border-yellow-300'
              : 'bg-gray-50 border-gray-300 opacity-50',
          ]"
        >
          <div class="text-3xl mb-2">{{ badge.icon }}</div>
          <p class="font-semibold text-gray-900 text-sm">{{ badge.name }}</p>
          <p class="text-xs text-gray-600 mt-1">{{ badge.description }}</p>
        </div>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'
import Badge from '@/components/Badge.vue'
import type { Recommendation } from '@/types'

const recommendations = ref<Recommendation[]>([])
const totalSavings = ref(0)

const availableBadges = [
  {
    id: 'green_warrior',
    name: 'Green Warrior',
    description: '100 kg CO₂ prevented',
    icon: '🌱',
    earned: false,
  },
  {
    id: 'transit_master',
    name: 'Transit Master',
    description: 'Use transit 10 times',
    icon: '🚌',
    earned: false,
  },
  {
    id: 'plant_power',
    name: 'Plant Power',
    description: '10 plant-based meals',
    icon: '🥗',
    earned: false,
  },
  {
    id: 'energy_saver',
    name: 'Energy Saver',
    description: 'Reduce energy by 50%',
    icon: '⚡',
    earned: false,
  },
]

const recommendationsByPriority = computed(() => {
  return {
    high: recommendations.value.filter((r) => r.priority === 'high'),
    medium: recommendations.value.filter((r) => r.priority === 'medium'),
    low: recommendations.value.filter((r) => r.priority === 'low'),
  }
})

const loadRecommendations = async () => {
  try {
    const response = await api.getRecommendations(20)
    recommendations.value = response.data.recommendations
    totalSavings.value = response.data.total_potential_savings
  } catch (error) {
    console.error('Failed to load recommendations:', error)
  }
}

onMounted(() => {
  loadRecommendations()
})
</script>
