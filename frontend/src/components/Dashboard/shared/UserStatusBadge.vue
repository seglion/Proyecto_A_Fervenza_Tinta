<template>
  <span :class="badgeClasses" class="px-3 py-1 text-sm font-bold rounded-full uppercase tracking-wider">
    {{ translatedStatus }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  esta_activo: { type: Boolean, required: true },
  aprobado_por_admin: { type: Boolean, required: true }
})

const { t } = useI18n()

// Determina la clave de estado (key)
const statusKey = computed(() => {
  if (props.esta_activo && props.aprobado_por_admin) {
    return 'active'
  }
  if (!props.esta_activo && props.aprobado_por_admin) {
    return 'inactive'
  }
  // Si aprobado_por_admin es false (independientemente de esta_activo)
  return 'pending'
})

// Asigna clases CSS basadas en la clave
const badgeClasses = computed(() => {
  switch (statusKey.value) {
    case 'active': 
      return 'bg-green-600 text-white'
    case 'inactive': 
      return 'bg-gray-700 text-gray-200'
    case 'pending': 
      return 'bg-yellow-600 text-white'
    default: 
      return 'bg-gray-700 text-gray-200' // Fallback
  }
})

// Traduce la clave
const translatedStatus = computed(() => {
  return t(`adminUsers.status.${statusKey.value}`)
})
</script>