<template>
  <form @submit="onSubmit" class="flex flex-col gap-6">
    <AuthInput
      v-for="f in fields"
      :key="f.name"
      v-bind="f"
    />

    <button
      type="submit"
      class="btn btn-primary w-full text-lg"
      :disabled="loading"
    >
      {{ loading ? 'Cargando...' : submitLabel }}
    </button>

    <p v-if="error" class="text-red-500 text-sm mt-2 text-center">{{ error }}</p>
  </form>
</template>

<script setup>
// 2. Ya no necesitas importar { Form }
import AuthInput from './AuthInput.vue'

defineProps({
  fields: { type: Array, required: true },
  onSubmit: { type: Function, required: true },
  submitLabel: { type: String, default: 'Enviar' },
  loading: { type: Boolean, default: false },
  error: { type: String, default: '' },
})
</script>