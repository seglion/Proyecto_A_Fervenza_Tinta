<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.admin.nav.payments') }}
    </h1>

    <AdminCard>
      <template #title>{{ t('adminPayments.view.title') }}</template>
      
      <nav class="flex flex-wrap border-b border-gray-700 mb-4">
        <button
          @click="activeTab = 'all'"
          :class="getTabClasses('all')"
        >
          {{ t('adminPayments.filter.allFees') }}
        </button>
        <button
          @click="activeTab = 'pending'"
          :class="getTabClasses('pending')"
        >
          {{ t('adminPayments.filter.pendingReport') }}
        </button>
      </nav>

      <div v-show="activeTab === 'all'">
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
          <div>
            <label for="seasonFilter" class="form-label">
              {{ t('adminPayments.filter.season') }}
            </label>
            <select 
              id="seasonFilter" 
              v-model="seasonFilter" 
              class="input"
              style="background-color: #000; color: white;"
            >
              <option value="all" style="background-color: #000;">
                {{ t('adminPayments.filter.allSeasons') }}
              </option>
              <option 
                v-for="season in adminStore.allSeasonsList" 
                :key="season.id" 
                :value="season.nombre_temporada"
                style="background-color: #000;"
              >
                {{ season.nombre_temporada }}
              </option>
            </select>
          </div>
          
          <div>
            <label for="paymentSearch" class="form-label">
              {{ t('adminPayments.search.label') }}
            </label>
            <input 
              id="paymentSearch"
              type="text" 
              v-model="searchTerm"
              :placeholder="t('adminPayments.search.placeholder')"
              class="input"
            />
          </div>
        </div>
        
        <div v-if="adminStore.isLoadingAllPayments || adminStore.isLoadingSeasons || adminStore.isLoadingUsers" class="text-gray-400 p-4 text-center">
          {{ t('dashboard.view.feeLoading') }}
        </div>
        <div v-else-if="adminStore.errorAllPayments" class="text-red-500 p-4 text-center">
          {{ t(adminStore.errorAllPayments) }}
        </div>
        
        <div v-else class="flex flex-col">
          <div class="hidden sm:grid grid-cols-6 gap-4 ...">
            </div>
          <div v-if="filteredPayments.length === 0" class="text-center text-gray-400 py-6">
            {{ t('adminUsers.search.noResults') }}
          </div>
          <div 
          v-for="pago in filteredPayments" 
          :key="pago.id"
          class="grid grid-cols-2 sm:grid-cols-6 gap-y-4 gap-x-2 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          <!-- Col 1: Socio -->
          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.member') }}: </span>
            <span class="font-bold">{{ pago.usuarioNombre }}</span>
          </div>

          <!-- Col 2: Temporada -->
          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.season') }}: </span>
            <span class="text-gray-400 text-sm">{{ pago.temporadaNombre }}</span>
          </div>

          <!-- Col 3: Plan -->
          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.plan') }}: </span>
            <span class="capitalize">{{ t(`dashboard.feeTypes.${pago.tipoCuotaNombre}`) }}</span>
          </div>

          <!-- Col 4: Estado -->
          <div class="sm:col-span-1 col-span-1">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.status') }}: </span>
            <CuotaStatusBadge :status="pago.estado_pago" />
          </div>

          <!-- Col 5: Importe -->
          <div class="sm:col-span-1 col-span-1 text-right">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPayments.table.amount') }}: </span>
            <span class="font-bold">€{{ pago.importe_pagado }}</span>
          </div>

          <!-- 2. NUEVA COLUMNA DE BOTÓN -->
          <div class="sm:col-span-1 col-span-2 text-right">
            <button 
              @click="adminStore.openPaymentDetailModal(pago.id)"
              class="btn btn-secondary !py-1 !px-3 !text-xs"
            >
              {{ t('adminPayments.table.viewDetail') }}
            </button>
          </div>
        </div>
        </div>
      </div> <div v-show="activeTab === 'pending'">
        <PendingPaymentsTable />
      </div>

    </AdminCard>
    
    <AdminPaymentDetailModal 
      v-if="adminStore.isPaymentDetailModalOpen"
      @close="adminStore.closePaymentDetailModal"
    />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import AdminCard from '@/components/Dashboard/shared/AdminCard.vue'
import CuotaStatusBadge from '@/components/Dashboard/shared/CuotaStatusBadge.vue'
// 4. IMPORTA EL NUEVO MODAL
import AdminPaymentDetailModal from '@/components/dashboard/sections/AdminPaymentDetailModal.vue'
import PendingPaymentsTable from '@/components/dashboard/sections/PendingPaymentsTable.vue'
const { t } = useI18n()
const adminStore = useAdminStore()
const activeTab = ref('all') // 'all' o 'pending'
// Carga inicial de datos
onMounted(() => {
  adminStore.fetchAllPayments()
  adminStore.fetchAllUsers()
  adminStore.fetchAllSeasons()
})

// --- Lógica de Filtro ---
const seasonFilter = ref('all')
const searchTerm = ref('') 

// 1. "JOIN" en el Frontend (Sin cambios)
const pagosConDetalle = computed(() => {
  if (!adminStore.allPaymentsList.length || !adminStore.userList.length || !adminStore.allSeasonsList.length) {
    return []
  }

  const userMap = new Map(adminStore.userList.map(u => [u.id, u]));
  
  const tipoCuotaMap = new Map();
  adminStore.allSeasonsList.forEach(season => {
    (season.tipos_cuota || []).forEach(tipo => {
      tipoCuotaMap.set(tipo.id, {
        nombre: tipo.nombre,
        temporadaNombre: season.nombre_temporada
      });
    });
  });

  return adminStore.allPaymentsList.map(pago => {
    const usuario = userMap.get(pago.usuario_id);
    const tipoCuotaInfo = tipoCuotaMap.get(pago.tipo_de_cuota_id);

    return {
      ...pago,
      usuarioNombre: usuario ? `${usuario.nombre} ${usuario.apellidos}` : 'Usuario no encontrado',
      tipoCuotaNombre: tipoCuotaInfo ? tipoCuotaInfo.nombre : 'Tipo desconocido',
      temporadaNombre: tipoCuotaInfo ? tipoCuotaInfo.temporadaNombre : 'Temporada desconocida'
    }
  });
});

// 2. FILTRADO (Sin cambios)
const filteredPayments = computed(() => {
  const season = seasonFilter.value
  const query = searchTerm.value.toLowerCase().trim()

  let payments = pagosConDetalle.value
  if (season !== 'all') {
    payments = payments.filter(pago => pago.temporadaNombre === season);
  }
  
  if (!query) {
    return payments;
  }

  return payments.filter(pago => {
    const memberName = (pago.usuarioNombre || '').toLowerCase()
    if (memberName.includes(query)) return true
    
    const planKey = (pago.tipoCuotaNombre || '').toLowerCase()
    const planName = t(`dashboard.feeTypes.${pago.tipoCuotaNombre}`).toLowerCase()
    if (planKey.includes(query) || planName.includes(query)) return true
    
    return false
  });
});



const getTabClasses = (tabName) => {
  const isActive = activeTab.value === tabName;
  let classes = [
    'py-2 px-3 sm:py-3 sm:px-4',
    'font-mono font-bold text-xs sm:text-sm',
    'uppercase tracking-wider transition-colors',
    'border-b-2 sm:border-b-4'
  ];
  if (isActive) {
    classes.push('border-brand-red', 'text-white');
  } else {
    classes.push('border-transparent', 'text-gray-500', 'hover:text-gray-300');
  }
  return classes;
};
</script>