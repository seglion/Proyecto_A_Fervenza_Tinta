<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-2xl p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ t('adminPayments.detail.title') }}
        </h2>
        <button @click="handleClose" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div v-if="adminStore.isLoadingPaymentDetail" class="text-gray-400 text-center p-8">
        <span class="material-symbols-outlined animate-spin text-red-600 text-4xl">
          progress_activity
        </span>
      </div>

      <div v-else-if="adminStore.errorPaymentDetail" class="text-red-500 text-center p-8">
        <p>{{ t(adminStore.errorPaymentDetail) }}</p>
      </div>
      
      <div v-else-if="adminStore.paymentDetail" class="space-y-6">
        
        <div>
          <h3 class="font-bold text-lg text-red-600 mb-2">{{ t('adminPayments.detail.userSection') }}</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <InfoRow :label="t('adminPayments.table.member')" :value="`${adminStore.paymentDetail.usuario_detalle.nombre} ${adminStore.paymentDetail.usuario_detalle.apellidos}`" />
            <InfoRow :label="t('register.emailLabel')" :value="adminStore.paymentDetail.usuario_detalle.email" />
          </div>
        </div>

        <hr class="border-gray-700">

        <div>
          <h3 class="font-bold text-lg text-red-600 mb-2">{{ t('adminPayments.detail.feeSection') }}</h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <InfoRow :label="t('adminPayments.table.season')" :value="adminStore.paymentDetail.temporada.nombre_temporada" />
            <InfoRow :label="t('adminPayments.table.plan')" :value="t(`dashboard.feeTypes.${adminStore.paymentDetail.tipo_cuota_detalle.nombre}`)" />
            <InfoRow :label="t('adminPayments.table.amount')" :value="`€${adminStore.paymentDetail.cuota.importe_pagado}`" />
          </div>
        </div>
        
        <hr class="border-gray-700">

        <div>
          <h3 class="font-bold text-lg text-red-600 mb-2">{{ t('adminPayments.detail.paymentSection') }}</h3>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div class="py-2">
              <label class="block text-sm font-medium text-gray-400">{{ t('adminPayments.table.status') }}</label>
              <CuotaStatusBadge class="mt-1" :status="adminStore.paymentDetail.cuota.estado_pago" />
            </div>
            
            <InfoRow 
              :label="t('adminPayments.detail.paymentDate')" 
              :value="d(new Date(adminStore.paymentDetail.cuota.fecha_pago), 'short')" 
              v-if="adminStore.paymentDetail.cuota.fecha_pago" 
            />
            
            <InfoRow 
              :label="t('adminPayments.detail.transactionId')" 
              :value="adminStore.paymentDetail.cuota.id_transaccion_externa"
              v-if="adminStore.paymentDetail.cuota.id_transaccion_externa" 
            />
            
            <InfoRow 
              :label="t('adminPayments.detail.adminNotes')" 
              :value="adminStore.paymentDetail.cuota.notas_admin" 
              class="sm:col-span-3"
              v-if="adminStore.paymentDetail.cuota.notas_admin" />







            <InfoRow :label="t('adminPayments.detail.paymentMethod')" :value="adminStore.paymentDetail.cuota.metodo_pago" />
                      <InfoRow 
              :label="t('adminPayments.detail.transactionId')" 
              :value="adminStore.paymentDetail.cuota.id_transaccion_externa"
              v-if="adminStore.paymentDetail.cuota.id_transaccion_externa" 
            />
            
            <InfoRow 
              :label="t('adminPayments.detail.adminNotes')" 
              :value="adminStore.paymentDetail.cuota.notas_admin" 
              class="sm:col-span-3"
              v-if="adminStore.paymentDetail.cuota.notas_admin" />
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAdminStore } from '@/stores/adminStore';
import { useI18n } from 'vue-i18n';
import InfoRow from '../shared/InfoRow.vue'; 
import CuotaStatusBadge from '../shared/CuotaStatusBadge.vue';
const emit = defineEmits(['close']);
const { t, d } = useI18n();
const adminStore = useAdminStore();

function handleClose() {
  emit('close');
}
</script>