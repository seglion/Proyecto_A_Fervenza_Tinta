<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('paymentStatus.successTitle') }}
    </h1>
    
    <InfoCard :title="t('paymentStatus.successCardTitle')">
      <div class="flex flex-col items-center text-center p-8 gap-4">
        <span class="material-symbols-outlined text-green-500 text-6xl">
          check_circle
        </span>
        <p class="text-gray-300">
          {{ t('paymentStatus.successMessage') }}
        </p>
        <RouterLink to="/dashboard" class="btn btn-primary mt-4">
          {{ t('paymentStatus.backButton') }}
        </RouterLink>
      </div>
    </InfoCard>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'
import InfoCard from '@/components/Dashboard/shared/InfoCard.vue'
const { t } = useI18n()
</script>