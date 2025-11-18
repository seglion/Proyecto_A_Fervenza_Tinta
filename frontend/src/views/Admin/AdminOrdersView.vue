<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.admin.nav.orders') }}
    </h1>


    <AdminCard>
      <template #title>        <div class="flex justify-between items-center">
          <span>{{ t('adminOrders.view.title') }}</span>
<button 
            @click="openSummaryModal" 
            :disabled="adminStore.isLoadingOrders"
            class="btn btn-primary !py-1 !px-3 !text-xs"
          >
            {{ t('adminOrders.report.viewSummary') }}
          </button>
        </div></template>
      
      <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
        
        <div>
          <label for="seasonFilter" class="form-label">
            {{ t('adminOrders.filter.season') }}
          </label>
          <select 
            id="seasonFilter" 
            v-model="seasonFilter" 
            class="input"
            style="background-color: #000; color: white;"
          >
            <option value="all" style="background-color: #000;">
              {{ t('adminOrders.filter.allSeasons') }}
            </option>
            <option 
              v-for="season in adminStore.allOrderSeasonsList" 
              :key="season.id" 
              :value="season.id" style="background-color: #000;"
            >
              {{ season.nombre_temporada }}
            </option>
          </select>
        </div>
        
        <div>
          <label for="orderSearch" class="form-label">
            {{ t('adminOrders.search.label') }}
          </label>
          <input 
            id="orderSearch"
            type="text" 
            v-model="searchTerm"
            :placeholder="t('adminOrders.search.placeholder')"
            class="input"
          />
        </div>
      </div>
      
      <div v-if="adminStore.isLoadingOrders || adminStore.isLoadingUsers" class="text-gray-400 p-4 text-center">
        {{ t('dashboard.view.feeLoading') }}
      </div>
      <div v-else-if="adminStore.errorOrders" class="text-red-500 p-4 text-center">
        {{ t(adminStore.errorOrders) }}
      </div>
      
      <div v-else class="flex flex-col">
        <div class="hidden sm:grid grid-cols-7 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
          <span>{{ t('adminOrders.table.id') }}</span>
          <span class="col-span-2">{{ t('adminOrders.table.member') }}</span> <span>{{ t('adminOrders.table.date') }}</span>
          <span>{{ t('adminOrders.table.status') }}</span>
          <span class="text-right">{{ t('adminOrders.table.total') }}</span>
          <span class="text-right">{{ t('adminOrders.table.actions') }}</span> </div>

        <div v-if="filteredOrders.length === 0" class="text-center text-gray-400 py-6">
          {{ t('adminOrders.search.noResults') }}
        </div>

        <div 
          v-for="pedido in filteredOrders" 
          :key="pedido.id"
          class="grid grid-cols-2 sm:grid-cols-7 gap-y-2 gap-x-4 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminOrders.table.id') }}: </span>
            <span class="text-gray-400 text-sm font-mono">#...{{ pedido.id.slice(-6) }}</span>
          </div>

          <div class="sm:col-span-2 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminOrders.table.member') }}: </span>
            <span class="font-bold">{{ pedido.usuarioNombre }} {{ pedido.usuarioApellidos }}</span>
            <p class="text-xs text-gray-500">{{ pedido.usuarioEmail }}</p>
          </div>

          <div class="sm:col-span-1 col-span-1">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminOrders.table.date') }}: </span>
            <span class="text-gray-400 text-sm">{{ d(new Date(pedido.fecha_creacion), 'short') }}</span>
          </div>

          <div class="sm:col-span-1 col-span-1">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminOrders.table.status') }}: </span>
            <PedidoStatusBadge :status="pedido.estado" />
          </div>

          <div class="sm:col-span-1 col-span-1 text-right">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminOrders.table.total') }}: </span>
            <span class="font-bold">€{{ pedido.total_calculado }}</span>
          </div>
          
<div class="sm:col-span-1 col-span-2 text-right flex sm:justify-end gap-2 items-center">
          
          <span v-if="loadingOrderId === pedido.id" class="material-symbols-outlined animate-spin text-red-600">
            progress_activity
          </span>
          
          <template v-else>
            <button 
              @click="adminStore.openOrderDetailModal(pedido.id)" 
              class="btn btn-secondary !py-1 !px-3 !text-xs"
            >
              {{ t('adminOrders.table.view') }}
            </button>

            <template v-if="pedido.estado === 'ENCARGADO'">
              <button 
                @click="handleMarkAsPaid(pedido.id)"
                class="btn btn-secondary !py-1 !px-3 !text-xs !bg-green-600 hover:!bg-green-700"
              >
                {{ t('adminOrders.actions.markPaid') }}
              </button>
              <button 
                @click="handleCancelOrder(pedido.id)"
                class="btn btn-secondary !py-1 !px-3 !text-xs !bg-red-800 hover:!bg-red-700"
              >
                {{ t('adminOrders.actions.cancel') }}
              </button>
            </template>
          </template>

        </div>
        </div>
      </div>
    </AdminCard>
    
    <AdminOrderDetailModal
      v-if="adminStore.isOrderDetailModalOpen"
      @close="adminStore.closeOrderDetailModal"
    />

<OrderProductionSummaryModal
      v-if="isSummaryModalOpen"
      :summary-data="adminStore.productionSummary"
      :is-loading="adminStore.isLoadingSummary"
      @close="isSummaryModalOpen = false"
    />
    
  </div>
</template>

<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import AdminCard from '@/components/Dashboard/shared/AdminCard.vue'
import PedidoStatusBadge from '@/components/Dashboard/shared/PedidoStatusBadge.vue'
import AdminOrderDetailModal from '@/components/Dashboard/sections/AdminOrderDetailModal.vue'
import OrderProductionSummaryModal from '@/components/Dashboard/sections/OrderProductionSummaryModal.vue'

const isSummaryModalOpen = ref(false)
const { t, d } = useI18n()
const adminStore = useAdminStore()

// --- ESTADO LOCAL ---
const loadingOrderId = ref(null) 
const seasonFilter = ref('all')
const searchTerm = ref('')

// --- LÓGICA DE CARGA ---
onMounted(() => {
  adminStore.fetchAllOrderSeasons()
  adminStore.fetchAllOrders('all') 
  adminStore.fetchAllUsers() 
})

// --- LÓGICA DE FILTROS (Computeds y Watcher) ---
watch(seasonFilter, (newSeasonId) => {
  adminStore.fetchAllOrders(newSeasonId)
})

// 1. JOIN en el Frontend
const ordersWithDetail = computed(() => {
  if (!adminStore.allOrdersList.length || !adminStore.userList.length || !adminStore.allOrderSeasonsList.length) {
    return []
  }
  const userMap = new Map(adminStore.userList.map(u => [u.id, u]));
  const seasonMap = new Map(adminStore.allOrderSeasonsList.map(s => [s.id, s.nombre_temporada]));

  return adminStore.allOrdersList.map(pedido => {
    const usuario = userMap.get(pedido.usuario_id);
    return {
      ...pedido,
      usuarioNombre: pedido.usuario_nombre || (usuario ? `${usuario.nombre} ${usuario.apellidos}` : 'Usuario desconocido'),
      usuarioEmail: pedido.usuarioEmail || (usuario ? usuario.email : ''),
      nombreTemporada: seasonMap.get(pedido.temporada_id) || 'Desconocida'
    }
  })
})

// 2. FILTRADO (para la tabla principal)
const filteredOrders = computed(() => {
  let orders = ordersWithDetail.value
  const query = searchTerm.value.toLowerCase().trim()

  if (!query) return orders // Devuelve la lista filtrada por temporada

  // Filtra por texto
  return orders.filter(pedido => {
    const idMatch = (pedido.id || '').toLowerCase().includes(query)
    const nameMatch = (pedido.usuarioNombre || '').toLowerCase().includes(query)
    const emailMatch = (pedido.usuarioEmail || '').toLowerCase().includes(query)
    return idMatch || nameMatch || emailMatch
  })
})
async function openSummaryModal() {
  const seasonId = seasonFilter.value
  if (seasonId === 'all') {
    alert('Por favor, selecciona una temporada específica para ver el resumen.');
    return;
  }
  
  await adminStore.fetchProductionSummary(seasonId)
  isSummaryModalOpen.value = true
}


// --- FUNCIONES DE ACCIÓN (Corregidas con authStore) ---

async function handleMarkAsPaid(pedidoId) {
  loadingOrderId.value = pedidoId
  try {
    // Llama a la acción del store (que ahora usa authStore)
    await adminStore.markOrderAsPaid(pedidoId)
  } catch (error) {
    alert(t(error.message)) 
  } finally {
    loadingOrderId.value = null
  }
}

async function handleCancelOrder(pedidoId) {
  if (confirm(t('adminOrders.actions.confirmCancel'))) {
    loadingOrderId.value = pedidoId
    try {
      await adminStore.cancelOrder(pedidoId)
    } catch (error) {
      alert(t(error.message))
    } finally {
      loadingOrderId.value = null
    }
  }
}
</script>