<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-4xl font-bold text-gray-900 font-display">
        Your Profile ⚙️
      </h1>
      <p class="text-gray-600 mt-2">Manage your account and preferences</p>
    </div>

    <!-- Profile Info -->
    <Card>
      <h2 class="text-2xl font-bold text-gray-900 mb-6 font-display">Account Information</h2>
      <form @submit.prevent="handleUpdateProfile" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Full Name
          </label>
          <input
            v-model="profileData.full_name"
            type="text"
            class="input"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Email
          </label>
          <input
            :value="authStore.user?.email"
            type="email"
            class="input"
            disabled
          />
          <p class="text-xs text-gray-500 mt-1">Email cannot be changed</p>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Region
          </label>
          <select
            v-model="profileData.region"
            class="input"
          >
            <option value="Global">Global</option>
            <option value="North America">North America</option>
            <option value="Europe">Europe</option>
            <option value="Asia">Asia</option>
            <option value="South America">South America</option>
            <option value="Africa">Africa</option>
            <option value="Oceania">Oceania</option>
          </select>
          <p class="text-xs text-gray-500 mt-1">Used for regional carbon factors (future)</p>
        </div>

        <Button
          type="submit"
          variant="primary"
          :disabled="isSaving"
        >
          {{ isSaving ? 'Saving...' : 'Save Changes' }}
        </Button>
      </form>
    </Card>

    <!-- Preferences -->
    <Card>
      <h2 class="text-2xl font-bold text-gray-900 mb-6 font-display">Preferences</h2>
      <form @submit.prevent="handleUpdateProfile" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Household Size
          </label>
          <select
            v-model.number="profileData.household_size"
            class="input"
          >
            <option :value="1">1 Person</option>
            <option :value="2">2 People</option>
            <option :value="3">3 People</option>
            <option :value="4">4 People</option>
            <option :value="5">5+ People</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Primary Vehicle Type
          </label>
          <select
            v-model="profileData.vehicle_type"
            class="input"
          >
            <option value="car">Car</option>
            <option value="electric_car">Electric Car</option>
            <option value="bus">Bus / Public Transit</option>
            <option value="train">Train</option>
            <option value="motorcycle">Motorcycle</option>
            <option value="none">No Vehicle</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Energy Source
          </label>
          <select
            v-model="profileData.energy_source"
            class="input"
          >
            <option value="grid">Grid Power</option>
            <option value="renewable">100% Renewable</option>
            <option value="mixed">Mixed</option>
          </select>
        </div>

        <Button
          type="submit"
          variant="primary"
          :disabled="isSaving"
        >
          {{ isSaving ? 'Saving...' : 'Save Changes' }}
        </Button>
      </form>
    </Card>

    <!-- Account Actions -->
    <Card>
      <h2 class="text-2xl font-bold text-gray-900 mb-6 font-display">Account Actions</h2>
      <Button
        variant="ghost"
        @click="handleLogout"
        class="w-full border-2 border-red-300"
      >
        🚪 Logout
      </Button>
    </Card>

    <!-- Success Message -->
    <div
      v-if="successMessage"
      class="p-4 bg-green-50 border border-green-200 rounded-lg"
    >
      <p class="text-green-800 text-sm">✓ {{ successMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Card from '@/components/Card.vue'
import Button from '@/components/Button.vue'

const router = useRouter()
const authStore = useAuthStore()

const profileData = ref({
  full_name: '',
  region: 'Global',
  household_size: 1,
  vehicle_type: 'car',
  energy_source: 'grid',
})

const isSaving = ref(false)
const successMessage = ref('')

const handleUpdateProfile = async () => {
  isSaving.value = true
  try {
    await api.updateProfile(profileData.value)
    successMessage.value = 'Profile updated successfully!'
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (error) {
    alert('Failed to update profile')
  } finally {
    isSaving.value = false
  }
}

const handleLogout = () => {
  if (confirm('Are you sure you want to logout?')) {
    authStore.logout()
    router.push('/login')
  }
}

const loadProfile = async () => {
  try {
    const response = await api.getProfile()
    profileData.value = {
      full_name: response.data.user.full_name,
      region: response.data.user.region,
      household_size: response.data.household_size,
      vehicle_type: response.data.vehicle_type,
      energy_source: response.data.energy_source,
    }
  } catch (error) {
    console.error('Failed to load profile:', error)
  }
}

onMounted(() => {
  loadProfile()
})
</script>
