<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-2xl p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ t('adminOrders.report.viewSummary') }}
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div class="max-h-[70vh] overflow-y-auto pr-2">
        
        <div v-if="adminStore.isLoadingSummary" class="text-gray-400 p-4 text-center">
          <span class="material-symbols-outlined animate-spin text-red-600 text-4xl">
            progress_activity
          </span>
        </div>

        <p v-else-if="!adminStore.productionSummary.length" class="text-center text-gray-400 p-4">
          {{ t('adminOrders.report.noItems') }}
        </p>

        <div v-else class="flex flex-col">
          <div class="grid grid-cols-4 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
            <span class="col-span-2">{{ t('adminOrders.report.item') }}</span>
            <span>{{ t('adminOrders.report.season') }}</span>
            <span class="text-right">{{ t('adminOrders.report.totalQuantity') }}</span>
          </div>

          <div 
            v-for="item in adminStore.productionSummary"
            :key="item.key"
            class="grid grid-cols-4 gap-4 py-3 border-b border-gray-800 items-center"
          >
            <span class="col-span-2 font-bold text-white">{{ item.desc_variante_conxelada }}</span>
            <span class="text-gray-400 text-sm">{{ item.temporada_nombre }}</span>
            <span class="text-right font-bold text-lg text-red-600">{{ item.total_cantidad }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n';
import { useAdminStore } from '@/stores/adminStore'; 

const { t } = useI18n();
const adminStore = useAdminStore(); 


defineEmits(['close']);
</script>