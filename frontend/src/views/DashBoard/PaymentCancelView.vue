<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('paymentStatus.cancelTitle') }}
    </h1>
    
    <InfoCard :title="t('paymentStatus.cancelCardTitle')">
      <div class="flex flex-col items-center text-center p-8 gap-4">
        <span class="material-symbols-outlined text-red-600 text-6xl">
          cancel
        </span>
        <p class="text-gray-300">
          {{ t('paymentStatus.cancelMessage') }}
        </p>
        <RouterLink to="/dashboard/store" class="btn btn-secondary mt-4">
          {{ t('paymentStatus.backToStoreButton') }}
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