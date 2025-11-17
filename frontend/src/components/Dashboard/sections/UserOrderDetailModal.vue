<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-lg p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ t('userOrders.detail.title') }}
        </h2>
        <button @click="handleClose" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div v-if="store.isLoadingOrderDetail" class="text-gray-400 text-center p-8">
        <span class="material-symbols-outlined animate-spin text-red-600 text-4xl">
          progress_activity
        </span>
      </div>

      <div v-else-if="store.errorOrderDetail" class="text-red-500 text-center p-8">
        <p>{{ t(store.errorOrderDetail) }}</p>
      </div>
      
      <div v-else-if="store.orderDetail" class="max-h-[60vh] overflow-y-auto pr-2">
        
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
          <InfoRow :label="t('userOrders.table.id')" :value="`#...${store.orderDetail.id.slice(-6)}`" />
          <InfoRow :label="t('userOrders.table.date')" :value="d(new Date(store.orderDetail.fecha_creacion), 'short')" />
          <div class="py-2">
            <label class="block text-sm font-medium text-gray-400">{{ t('userOrders.table.status') }}</label>
            <PedidoStatusBadge class="mt-1" :status="store.orderDetail.estado" />
          </div>
        </div>

        <hr class="border-gray-700 my-4">

        <h3 class="font-bold text-lg text-red-600 mb-2">{{ t('userOrders.detail.items') }}</h3>
        <div class="space-y-4">
          <div 
            v-for="linea in store.orderDetail.lineas" 
            :key="linea.id"
            class="flex items-center gap-3 p-2 bg-gray-900 rounded-md"
          >
            <div class="flex-grow">
              <p class="font-bold text-white">{{ linea.desc_variante_conxelada }}</p>
              <p class="text-sm text-gray-400">
                {{ linea.cantidad }} x €{{ linea.precio_unitario_conxelado }}
              </p>
            </div>
            <p class="font-bold text-white">€{{ (linea.cantidad * linea.precio_unitario_conxelado).toFixed(2) }}</p>
          </div>
        </div>
        
        <hr class="border-gray-700 my-4">
        <div class="flex justify-end items-center font-display text-2xl uppercase">
          <span class="text-gray-400 mr-4">{{ t('merchandise.total') }}</span>
          <span class="text-white font-bold">€{{ store.orderDetail.total_calculado }}</span>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { usePedidosStore } from '@/stores/pedidosStore';
import { useI18n } from 'vue-i18n';
import InfoRow from '../shared/InfoRow.vue'; 
import PedidoStatusBadge from '../shared/PedidoStatusBadge.vue'; 

const emit = defineEmits(['close']);
const { t, d } = useI18n(); 
const store = usePedidosStore();

function handleClose() {
  emit('close');
}
</script>