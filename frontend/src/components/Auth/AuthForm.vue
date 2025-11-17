<template>
  <form @submit="onSubmit" class="flex flex-col gap-6">
    
    <AuthInput
      v-for="f in fields"
      :key="f.name"
      v-bind="f"
      :disabled="isReadOnly"
      :modelValue="f.modelValue" />

    <p v-if="successMessage" class="text-green-400 text-sm text-center">
      {{ successMessage }}
    </p>
    <p v-if="errorMessage" class="text-red-500 text-sm text-center">
      {{ errorMessage }}
    </p>
    
    <div v-if="!isReadOnly" class="flex justify-end mt-4">
      <button
        type="submit"
        :disabled="loading"
        class="btn btn-primary w-full sm:w-auto"
      >
        {{ loading ? t('resetPassword.sending') : submitLabel }}
      </button>
    </div>
  </form>
</template>

<script setup>
import AuthInput from './AuthInput.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  fields: { type: Array, required: true },
  onSubmit: { type: Function, required: true }, 
  submitLabel: { type: String, default: 'Enviar' },
  loading: { type: Boolean, default: false },
  isReadOnly: { type: Boolean, default: false },
  successMessage: { type: String, default: null },
  errorMessage: { type: String, default: null },
})
</script>