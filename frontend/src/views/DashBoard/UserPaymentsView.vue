<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.nav.paymentshistory') }}
    </h1>

    <InfoCard :title="t('userPayments.view.title')">
      
      <div v-if="store.isLoadingHistorial" class="text-gray-400 p-4 text-center">
        {{ t('dashboard.view.feeLoading') }}
      </div>
      <div v-else-if="store.errorHistorial" class="text-red-500 p-4 text-center">
        {{ t(store.errorHistorial) }}
      </div>
      
      <div v-else class="flex flex-col">
        
        <div class="hidden sm:grid grid-cols-4 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
          <span>{{ t('userPayments.table.season') }}</span>
          <span>{{ t('userPayments.table.plan') }}</span>
          <span>{{ t('userPayments.table.paymentDate') }}</span>
          <span class="text-right">{{ t('userPayments.table.amount') }}</span>
        </div>

        <div v-if="store.historialPagos.length === 0" class="text-center text-gray-400 py-6">
          {{ t('userPayments.view.noHistory') }}
        </div>

        <div 
          v-for="pago in sortedHistorial" 
          :key="pago.id"
          class="grid grid-cols-2 sm:grid-cols-4 gap-y-2 gap-x-4 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('userPayments.table.season') }}: </span>
          <span class="sm:col-span-1 font-bold text-left sm:text-left">{{ pago.temporada_nombre }}</span>

          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('userPayments.table.plan') }}: </span>
          <span class="sm:col-span-1 capitalize text-left sm:text-left">{{ t(`dashboard.feeTypes.${pago.tipo_cuota_nombre}`) }}</span>

          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('userPayments.table.paymentDate') }}: </span>
          <span class="sm:col-span-1 text-gray-400 text-sm text-left sm:text-left">{{ d(new Date(pago.fecha_pago), 'short') }}</span>

          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('userPayments.table.amount') }}: </span>
          <span class="sm:col-span-1 text-right font-bold">€{{ pago.importe_pagado }}</span>
        </div>
      </div>
    </InfoCard>
  </div>
</template>
<script setup>
import { onMounted,computed } from 'vue'
import { useCuotasStore } from '@/stores/cuotas' // ¡El store del USUARIO!
import { useI18n } from 'vue-i18n'
import InfoCard from '@/components/Dashboard/shared/InfoCard.vue'

const { t, d } = useI18n()
const store = useCuotasStore()

// Carga inicial de datos
onMounted(() => {
  store.fetchHistorialPagos()
})

const sortedHistorial = computed(() => {
  // Si la lista no existe o está vacía, devuelve un array vacío
  if (!store.historialPagos || store.historialPagos.length === 0) {
    return []
  }
  // 1. Clona el array (para no modificar el store original)
  const list = [...store.historialPagos]
  
  // 2. Ordena por 'temporada_nombre' en orden descendente
  //    (para que 2025-2026 aparezca antes que 2024-2025)
  return list.sort((a, b) => {
    return b.temporada_nombre.localeCompare(a.temporada_nombre)
  })
   })
</script>