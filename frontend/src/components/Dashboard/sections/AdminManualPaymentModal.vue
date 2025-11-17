<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-lg p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ t('adminPayments.manualPay.title') }}
        </h2>
        <button @click="handleClose" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <form v-if="cuota" @submit.prevent="handleSubmit" class="space-y-4">
        
        <p class="text-gray-400">
          {{ t('adminPayments.manualPay.description', { name: cuota.usuarioNombre }) }}
        </p>
        
        <div>
          <label for="manualAmount" class="form-label">
            {{ t('adminPayments.manualPay.amount') }}
          </label>
          <input 
            id="manualAmount"
            type="number"
            step="0.01"
            v-model="importe"
            class="input"
          />
        </div>
        
        <div>
          <label for="manualMethod" class="form-label">
            {{ t('adminPayments.manualPay.method') }}
          </label>
          <select 
            id="manualMethod" 
            v-model="metodo" 
            class="input"
            style="background-color: #000; color: white;"
          >
            <option value="EFECTIVO" style="background-color: #000;">{{ t('adminPayments.manualPay.cash') }}</option>
            <option value="TRANSFERENCIA_MANUAL" style="background-color: #000;">{{ t('adminPayments.manualPay.transfer') }}</option>
          </select>
        </div>
        
        <div>
          <label for="manualNotes" class="form-label">
            {{ t('adminPayments.manualPay.notes') }}
          </label>
          <textarea 
            id="manualNotes"
            v-model="notas"
            class="input"
            rows="3"
            :placeholder="t('adminPayments.manualPay.notesPlaceholder')"
          ></textarea>
        </div>
        
        <p v-if="adminStore.errorManualPayment" class="text-red-500 text-sm text-center">
          {{ t(adminStore.errorManualPayment) }}
        </p>

        <div class="flex justify-end pt-4">
          <button 
            type="submit" 
            :disabled="adminStore.isLoadingManualPayment"
            class="btn btn-primary w-full sm:w-auto"
          >
            {{ adminStore.isLoadingManualPayment ? t('resetPassword.sending') : t('adminPayments.manualPay.submit') }}
          </button>
        </div>
        
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAdminStore } from '@/stores/adminStore';
import { useI18n } from 'vue-i18n';

const emit = defineEmits(['close']);
const { t } = useI18n();
const adminStore = useAdminStore();

const cuota = adminStore.cuotaToPayManually;

// Estado del formulario
// Pre-rellena el importe con el valor esperado de la cuota
const importe = ref(cuota.importe_pagado); 
const metodo = ref('EFECTIVO'); // Valor por defecto
const notas = ref('');

function handleClose() {
  emit('close');
}

async function handleSubmit() {
  const paymentData = {
    importe: importe.value,
    metodo: metodo.value,
    notas: notas.value || 'Pago registrado manualmente por admin.'
  };

  try {
    await adminStore.registerManualPayment(cuota.id, paymentData);
    // Si tiene éxito, el store refresca las listas y cerramos
    handleClose();
  // eslint-disable-next-line no-unused-vars
  } catch (error) {
    // El error se mostrará en el template
  }
}
</script>