<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex justify-center items-start p-4 sm:items-center">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-lg p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ t('merchandise.cartTitle') }}
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div class="max-h-[60vh] overflow-y-auto pr-2">
        <div v-if="pedidosStore.isLoading" class="text-center text-gray-400 p-8">
          <span class="material-symbols-outlined animate-spin text-red-600 text-4xl">
            progress_activity
          </span>
        </div>

        <div v-else-if="!pedidosStore.draftOrder || pedidosStore.cartItemCount === 0" class="text-center text-gray-400 p-8">
          {{ t('merchandise.cart.empty') }}
        </div>

        <div v-else>
          <div class="space-y-4">
            <div 
              v-for="linea in pedidosStore.draftOrder.lineas" 
              :key="linea.id"
              class="flex items-center gap-3"
            >
              <div class="flex-grow">
                <p class="font-bold text-white">{{ linea.desc_variante_conxelada }}</p>
                <p class="text-sm text-gray-400">
                  {{ linea.cantidad }} x €{{ linea.precio_unitario_conxelado }}
                </p>
              </div>
              <button 
                @click="pedidosStore.removeLine(linea.id)" 
                class="text-red-500 hover:text-red-400"
              >
                <span class="material-symbols-outlined">delete</span>
              </button>
            </div>
          </div>

          <hr class="border-gray-700 my-4">

          <div class="flex justify-between items-center font-display text-2xl uppercase">
            <span class="text-gray-400">{{ t('merchandise.total') }}</span>
            <span class="text-white font-bold">€{{ pedidosStore.draftOrder.total_calculado }}</span>
          </div>

          <div class="mt-6 flex flex-col gap-3">
            <button 
              @click="pedidosStore.confirmAndPay"
              class="btn btn-primary w-full"
            >
              {{ t('merchandise.buttons.pay') }} (Stripe)
            </button>
            <button 
              @click="pedidosStore.confirmAndCommission"
              class="btn btn-secondary w-full"
            >
              {{ t('merchandise.buttons.commission') }}
            </button>
          </div>
        </div>
      </div> </div>
  </div>
</template>

<script setup>
import { usePedidosStore } from '@/stores/pedidosStore'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const pedidosStore = usePedidosStore()
defineEmits(['close'])
</script>