<template>
  <span 
    :class="badgeClasses" 
    class="
      px-3 py-1 text-sm font-bold rounded-full uppercase tracking-wider
      whitespace-nowrap 
    "
  >
    {{ translatedStatus }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  status: { 
    type: String, 
    required: true 
  }
})

const { t } = useI18n()

// Asigna colores (sin cambios)
const badgeClasses = computed(() => {
  switch (props.status) {
    case 'COMPLETADO':
      return 'bg-green-600 text-white'
    case 'PENDIENTEPAGO':
      return 'bg-yellow-600 text-white'
    case 'ENCARGADO':
      return 'bg-blue-600 text-white'
    case 'CANCELADO':
      return 'bg-red-700 text-white'
    default:
      return 'bg-gray-700 text-gray-200'
  }
})

// Traduce el estado (sin cambios)
const translatedStatus = computed(() => {
  // Busca la clave (ej. 'userOrders.status.PENDIENTEPAGO')
  const key = `userOrders.status.${props.status}`
  // t() la traducirá a "Pendiente de Pago"
  return t(key)
})
</script>