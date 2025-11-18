<template>
  <div>
    <h1
      class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl"
    >
      {{ t('dashboard.nav.orders') }}
    </h1>

    <InfoCard :title="t('userOrders.view.title')">
      <div v-if="store.isLoadingHistory" class="text-gray-400 p-4 text-center">
        {{ t('dashboard.view.feeLoading') }}
      </div>
      <div v-else-if="store.errorHistory" class="text-red-500 p-4 text-center">
        {{ t(store.errorHistory) }}
      </div>

      <div v-else class="flex flex-col">
<div class="hidden sm:grid grid-cols-5 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
          <span>{{ t('userOrders.table.id') }}</span>
          <span>{{ t('userOrders.table.date') }}</span>
          <span>{{ t('userOrders.table.status') }}</span>
          <span class="text-right">{{ t('userOrders.table.total') }}</span>
          <span class="text-right">{{ t('userOrders.table.actions') }}</span> </div>

        <div v-if="store.orderHistory.length === 0" class="text-center text-gray-400 py-6">
          {{ t('userOrders.view.noHistory') }}
        </div>

<div 
          v-for="pedido in store.orderHistory" 
          :key="pedido.id"
          class="grid grid-cols-2 sm:grid-cols-5 gap-y-2 gap-x-4 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          <span class="sm:hidden text-xs text-gray-500 uppercase"
            >{{ t('userOrders.table.id') }}:
          </span>
          <span class="sm:col-span-1 font-bold text-sm text-gray-400"
            >#{{ pedido.id }}</span
          >

          <span class="sm:hidden text-xs text-gray-500 uppercase"
            >{{ t('userOrders.table.date') }}:
          </span>
          <span class="sm:col-span-1 text-gray-400 text-sm">{{
            d(new Date(pedido.fecha_creacion), 'short')
          }}</span>

          <span class="sm:hidden text-xs text-gray-500 uppercase"
            >{{ t('userOrders.table.status') }}:
          </span>
          <div class="sm:col-span-1">
            <PedidoStatusBadge :status="pedido.estado" />
          </div>

          <span class="sm:hidden text-xs text-gray-500 uppercase"
            >{{ t('userOrders.table.total') }}:
          </span>
          <span class="sm:col-span-1 text-right font-bold">€{{ pedido.total_calculado }}</span>
          <div class="sm:col-span-1 col-span-2 text-right">
            <button 
              @click="store.openOrderDetailModal(pedido.id)"
              class="btn btn-secondary !py-1 !px-3 !text-xs"
            >
              {{ t('userOrders.table.viewDetail') }}
            </button>
          </div>
        </div>
        
      </div>
    </InfoCard>
    <UserOrderDetailModal
      v-if="store.isOrderDetailModalOpen"
      @close="store.closeOrderDetailModal"
    />
    <OrderProductionSummaryModal
      v-if="isSummaryModalOpen"
      @close="isSummaryModalOpen = false"
    />
  </div>

</template>

<script setup>
import { onMounted } from 'vue'
import { usePedidosStore } from '@/stores/pedidosStore'
import { useI18n } from 'vue-i18n'
import InfoCard from '@/components/Dashboard/shared/InfoCard.vue'
// Reutilizamos el badge de Cuotas, pero le pasamos el texto traducido
import PedidoStatusBadge from '@/components/Dashboard/shared/PedidoStatusBadge.vue'
import UserOrderDetailModal from '@/components/Dashboard/sections/UserOrderDetailModal.vue'
import OrderProductionSummaryModal from '@/components/Dashboard/sections/OrderProductionSummaryModal.vue'
const { t, d } = useI18n()
const store = usePedidosStore()

onMounted(() => {
  store.fetchOrderHistory()
})
</script>
