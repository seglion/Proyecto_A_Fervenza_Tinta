<template>
  <div> <div class="mb-4">
      <label for="pendingSearch" class="form-label">
        {{ t('adminPayments.search.label') }}
      </label>
      <input 
        id="pendingSearch"
        type="text" 
        v-model="searchTerm"
        :placeholder="t('adminPayments.search.placeholder')"
        class="input"
      />
    </div>

    <div v-if="adminStore.isLoadingPendingReport" class="text-gray-400 p-4 text-center">
      {{ t('dashboard.view.feeLoading') }}
    </div>
    <div v-else-if="adminStore.errorPendingReport" class="text-red-500 p-4 text-center">
      {{ t(adminStore.errorPendingReport) }}
    </div>

    <div v-else class="flex flex-col">
      
      <div class="hidden sm:grid grid-cols-5 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
        <span>{{ t('adminPayments.table.member') }}</span>
        <span>{{ t('adminPayments.table.email') }}</span>
        <span>{{ t('adminPayments.table.status') }}</span>
        <span class="text-right">{{ t('adminPayments.table.amount') }}</span>
        <span class="text-right">{{ t('adminPayments.table.actions') }}</span> 
      </div>

      <div v-if="filteredPendingReport.length === 0" class="text-center text-gray-400 py-6">
        {{ t('adminUsers.search.noResults') }}
      </div>

      <div 
        v-for="item in filteredPendingReport" 
        :key="item.usuario.id"
        class="grid grid-cols-2 sm:grid-cols-5 gap-y-4 gap-x-2 sm:gap-4 py-3 border-b border-gray-800 items-center"
      >
        <div class="sm:col-span-1 col-span-2">
          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.member') }}: </span>
          <span class="font-bold">{{ item.usuario.nombre }} {{ item.usuario.apellidos }}</span>
        </div>

        <div class="sm:col-span-1 col-span-2">
          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.email') }}: </span>
          <span class="text-gray-400 text-sm break-all">{{ item.usuario.email }}</span>
        </div>

        <div class="sm:col-span-1 col-span-1">
          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.status') }}: </span>
          <CuotaStatusBadge :status="item.cuota.estado_pago" />
        </div>

        <div class="sm:col-span-1 col-span-1 text-right">
          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.amount') }}: </span>
          <span class="font-bold">€{{ item.cuota.importe_pagado }}</span>
        </div>
        
        <div class="sm:col-span-1 col-span-2 text-right flex sm:justify-end gap-2">
          
          <span v-if="loadingPayment === item.cuota.id" class="material-symbols-outlined animate-spin text-red-600">
            progress_activity
          </span>
          
          <template v-else>
            <button 
              @click="adminStore.openPaymentDetailModal(item.cuota.id)"
              class="btn btn-secondary py-1! px-3! text-xs!"
              title="Ver Detalle"
            >
              {{ t('adminPayments.table.viewDetail') }}
            </button>
            
            <button 
              @click="handleOpenManualPayment(item)"
              class="btn btn-secondary py-1! px-3! text-xs! bg-red-600! hover:bg-red-900!"
              title="Registrar Pago Manual"
            >
              {{ t('adminPayments.table.registerManual') }}
            </button>
          </template>
        </div>
      </div>
    </div>
    
    <AdminManualPaymentModal
      v-if="adminStore.isManualPaymentModalOpen"
      @close="adminStore.closeManualPaymentModal"
    />
    
    <AdminPaymentDetailModal 
      v-if="adminStore.isPaymentDetailModalOpen"
      @close="adminStore.closeDetailModal"
    />

  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import CuotaStatusBadge from '@/components/Dashboard/shared/CuotaStatusBadge.vue'
import AdminManualPaymentModal from './AdminManualPaymentModal.vue'
// ¡Importa el modal de detalle que faltaba!
import AdminPaymentDetailModal from '@/components/Dashboard/sections/AdminPaymentDetailModal.vue'

const { t } = useI18n()
const adminStore = useAdminStore()

const loadingPayment = ref(null) 

onMounted(() => {
  adminStore.fetchPendingReport()
})

// --- Lógica de Búsqueda ---
const searchTerm = ref('')

const filteredPendingReport = computed(() => {
  if (!adminStore.pendingReport) {
    return []
  }
  
  const query = searchTerm.value.toLowerCase().trim()
  
  if (!query) {
    return adminStore.pendingReport
  }

  return adminStore.pendingReport.filter(item => {
    const fullName = `${item.usuario.nombre} ${item.usuario.apellidos}`.toLowerCase()
    if (fullName.includes(query)) return true
    
    const email = (item.usuario.email || '').toLowerCase()
    if (email.includes(query)) return true
    
    return false
  })
})

// --- Lógica de Acciones ---

// Esta función es necesaria para pasar el objeto 'item' completo
// (que incluye el nombre del usuario y el importe) al store.
function handleOpenManualPayment(item) {
  // El store guardará el objeto 'cuota'
  // pero le añadimos los detalles que el modal necesita
  const cuotaConDetalle = {
    ...item.cuota,
    usuarioNombre: `${item.usuario.nombre} ${item.usuario.apellidos}`
  }
  adminStore.openManualPaymentModal(cuotaConDetalle)
}

// (El 'openPaymentDetailModal' se llama directamente desde el template)
</script>