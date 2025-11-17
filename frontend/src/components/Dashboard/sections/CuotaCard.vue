<template>
  <InfoCard :title="t('dashboard.view.feeTitle')">
    
    <div v-if="store.isLoading && !store.cuotaActiva" class="text-center text-gray-400 p-4">
      {{ t('dashboard.view.feeLoading') }}
    </div>

    <div v-else-if="store.error && !store.cuotaActiva" class="text-center text-red-500 p-4">
      {{ t(store.error, 'apiErrors.genericError') }}
    </div>

    <div v-else-if="store.cuotaActiva" class="flex flex-col sm:flex-row justify-between items-center gap-4 p-4">
      
      <div class="flex flex-col items-center sm:items-start text-lg">
        
        
        <div class="mt-2 text-sm text-gray-400 text-center sm:text-left">
          <p class="font-bold text-3xl text-white">
            {{ store.cuotaActiva.importe_pagado }} €
            <CuotaStatusBadge :status="store.cuotaActiva.estado_pago" />
          </p>
          <p v-if="store.cuotaActiva.estado_pago === 'completado'">
            {{ t('dashboard.view.feePaidOn') }}: {{ formattedDate }}
          </p>

        </div>
      </div>
      
      <button 
        v-if="store.cuotaActiva.estado_pago === 'pendiente' || store.cuotaActiva.estado_pago === 'fallido'"
        @click="handlePayment"
        :disabled="store.isLoading"
        class="w-full sm:w-auto btn btn-primary"
      >
        <span v-if="store.isLoading">{{ t('dashboard.view.feeProcessing') }}</span>
        <span v-else-if="store.cuotaActiva.estado_pago === 'fallido'">{{ t('dashboard.view.feeRetry') }}</span>
        <span v-else>{{ t('dashboard.view.feeButton') }}</span>
      </button>

      <button 
        v-else-if="store.cuotaActiva.estado_pago === 'completado'"
        disabled
        class="w-full sm:w-auto btn btn-primary bg-green-700 hover:bg-green-700 opacity-70 cursor-not-allowed"
      >
        {{ t('dashboard.view.feePaid') }}
      </button>
      
    </div>

    <div v-else class="text-center text-gray-400 p-4">
       {{ t('dashboard.view.feeNone') }}
    </div>

  </InfoCard>
</template>

<script setup>
import { onMounted, computed } from 'vue'
import { useCuotasStore } from '@/stores/cuotas'
import { useI18n } from 'vue-i18n'
import InfoCard from '@/components/Dashboard/shared/InfoCard.vue'
import CuotaStatusBadge from '@/components/Dashboard/shared/CuotaStatusBadge.vue'

const store = useCuotasStore()
const { t, d } = useI18n() 

onMounted(() => {
  if (!store.cuotaActiva) { 
    store.fetchCuotaActiva()
  }
})

const formattedDate = computed(() => {
  if (store.cuotaActiva?.fecha_pago) {
    return d(new Date(store.cuotaActiva.fecha_pago), 'short')
  }
  return ''
})

const handlePayment = async () => {
  await store.createPaymentIntent()
}
</script>