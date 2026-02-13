<template>
  <Card>
    <div class="max-w-2xl mx-auto">
      <h2 class="text-2xl font-bold text-gray-900 mb-6 font-display">
        Log Your Emission
      </h2>

      <!-- Tabs -->
      <div class="flex gap-2 mb-8 border-b border-gray-200">
        <button
          v-for="tab in tabs"
          :key="tab"
          @click="activeTab = tab"
          :class="[
            'pb-3 px-4 font-medium transition-colors border-b-2',
            activeTab === tab
              ? 'border-primary-600 text-primary-600'
              : 'border-transparent text-gray-500 hover:text-gray-700',
          ]"
        >
          {{ tab.charAt(0).toUpperCase() + tab.slice(1) }}
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="submitForm" class="space-y-6">
        <!-- Category Selection (Hidden, set by tab) -->
        <input type="hidden" v-model="formData.category" />

        <!-- Subcategory Selection -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            {{ subcategoryLabel }}
          </label>
          <select
            v-model="formData.subcategory"
            class="input"
            required
          >
            <option value="">Select {{ activeTab }}</option>
            <option
              v-for="sub in subcategoryOptions"
              :key="sub.value"
              :value="sub.value"
            >
              {{ sub.label }} ({{ sub.factor }} kg CO₂/{{ unitForCategory }})
            </option>
          </select>
        </div>

        <!-- Quantity Input -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Quantity ({{ unitForCategory }})
          </label>
          <input
            v-model.number="formData.quantity"
            type="number"
            step="0.1"
            class="input"
            placeholder="0"
            required
            @input="calculateCO2"
          />
          <p
            v-if="calculatedCO2 > 0"
            class="mt-2 text-sm font-semibold text-primary-600"
          >
            💨 This produces {{ calculatedCO2 }} kg CO₂
          </p>
        </div>

        <!-- Date --> 
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Date
          </label>
          <input
            v-model="formData.date"
            type="date"
            class="input"
            required
          />
        </div>

        <!-- Notes -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Notes (Optional)
          </label>
          <textarea
            v-model="formData.notes"
            class="input min-h-20 resize-none"
            placeholder="Add any notes..."
          ></textarea>
        </div>

        <!-- Submit Button -->
        <Button
          type="submit"
          variant="primary"
          :disabled="isLoading"
          class="w-full"
        >
          {{ isLoading ? 'Logging...' : 'Log Emission' }}
        </Button>
      </form>
    </div>
  </Card>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import Button from './Button.vue'
import Card from './Card.vue'
import { useEmissionsStore } from '@/stores/emissions'

const emissionsStore = useEmissionsStore()
const isLoading = ref(false)

const tabs = ['transport', 'energy', 'food']
const activeTab = ref('transport')

const formData = ref({
  category: 'transport',
  subcategory: '',
  quantity: 0,
  unit: 'km',
  date: new Date().toISOString().split('T')[0],
  notes: '',
})

const calculatedCO2 = ref(0)

const subcategoryOptions = computed(() => {
  const options: Record<string, Array<{ value: string; label: string; factor: number }>> = {
    transport: [
      { value: 'car', label: '🚗 Car', factor: 0.21 },
      { value: 'electric_car', label: '⚡ Electric Car', factor: 0.08 },
      { value: 'bus', label: '🚌 Bus', factor: 0.06 },
      { value: 'train', label: '🚂 Train', factor: 0.04 },
      { value: 'flight', label: '✈️ Flight', factor: 0.25 },
      { value: 'motorcycle', label: '🏍️ Motorcycle', factor: 0.09 },
    ],
    energy: [
      { value: 'electricity', label: '💡 Electricity', factor: 0.385 },
      { value: 'natural_gas', label: '🔥 Natural Gas', factor: 0.2 },
      { value: 'heating_oil', label: '🪣 Heating Oil', factor: 0.268 },
    ],
    food: [
      { value: 'beef', label: '🥩 Beef', factor: 27 },
      { value: 'pork', label: '🐖 Pork', factor: 4 },
      { value: 'chicken', label: '🍗 Chicken', factor: 2.5 },
      { value: 'fish', label: '🐟 Fish', factor: 3.5 },
      { value: 'dairy', label: '🧀 Dairy/Cheese', factor: 5 },
      { value: 'plant_based', label: '🥗 Plant-based', factor: 1 },
    ],
  }
  return options[activeTab.value] || []
})

const subcategoryLabel = computed(() => {
  const labels: Record<string, string> = {
    transport: 'Vehicle Type',
    energy: 'Energy Type',
    food: 'Food Type',
  }
  return labels[activeTab.value]
})

const unitForCategory = computed(() => {
  const units: Record<string, string> = {
    transport: 'km',
    energy: 'kWh',
    food: 'meal',
  }
  formData.value.unit = units[activeTab.value]
  return units[activeTab.value]
})

const calculateCO2 = () => {
  const factors: Record<string, Record<string, number>> = {
    transport: {
      car: 0.21,
      electric_car: 0.08,
      bus: 0.06,
      train: 0.04,
      flight: 0.25,
      motorcycle: 0.09,
    },
    energy: {
      electricity: 0.385,
      natural_gas: 0.2,
      heating_oil: 0.268,
    },
    food: {
      beef: 27,
      pork: 4,
      chicken: 2.5,
      fish: 3.5,
      dairy: 5,
      plant_based: 1,
    },
  }

  const factor =
    factors[activeTab.value]?.[formData.value.subcategory] || 0
  calculatedCO2.value = Math.round(factor * (formData.value.quantity || 0) * 100) / 100
}

const submitForm = async () => {
  isLoading.value = true
  try {
    await emissionsStore.addEmission({
      category: activeTab.value,
      subcategory: formData.value.subcategory,
      quantity: formData.value.quantity,
      unit: formData.value.unit,
      date: formData.value.date,
      notes: formData.value.notes,
    })

    // Reset form
    formData.value = {
      category: activeTab.value,
      subcategory: '',
      quantity: 0,
      unit: unitForCategory.value,
      date: new Date().toISOString().split('T')[0],
      notes: '',
    }
    calculatedCO2.value = 0

    // Show success toast
    alert('✅ Emission logged successfully!')
  } catch (error) {
    alert('❌ Failed to log emission: ' + (error as any).message)
  } finally {
    isLoading.value = false
  }
}
</script>
