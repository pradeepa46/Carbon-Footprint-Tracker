<template>
  <div class="max-w-3xl mx-auto">
    <div>
      <h1 class="text-4xl font-bold text-gray-900 font-display">
        Log Your Emission 📝
      </h1>
      <p class="text-gray-600 mt-2">
        Track any activity that produces carbon emissions
      </p>
    </div>

    <div class="mt-8">
      <EmissionForm />
    </div>

    <!-- Info Box -->
    <Card class="mt-8">
      <h3 class="font-bold text-gray-900 mb-4">💡 Tips for Accurate Logging</h3>
      <ul class="space-y-2 text-gray-600 text-sm">
        <li>✓ Log activities the day you do them for accuracy</li>
        <li>✓ Use actual distances/amounts - round to nearest 0.1</li>
        <li>✓ For multiple passengers (carpool), we count the full emissions</li>
        <li>✓ All factors are global averages - updated quarterly</li>
        <li>✓ Your emissions data is private and never shared</li>
      </ul>
    </Card>
  </div>
</template>

<script setup lang="ts">
import EmissionForm from '@/components/EmissionForm.vue'
import Card from '@/components/Card.vue'
</script>
