<template>
  <span :class="badgeClasses" class="px-3 py-1 text-sm font-bold rounded-full uppercase tracking-wider">
    {{ translatedStatus }}
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  status: {
    type: String,
    required: true,
    default: 'pendiente'
  }
})

const { t } = useI18n()


const badgeClasses = computed(() => {
  switch (props.status) {
    case 'pendiente':
      return 'bg-yellow-600 text-white' // Amarillo/Naranja para pendiente
    case 'completado': 
      return 'bg-green-600 text-white' // Verde para completado
    case 'fallido': 
      return 'bg-red-700 text-white' // Rojo para fallido
    default:
      return 'bg-gray-700 text-gray-200'
  }
})

const translatedStatus = computed(() => {
  return t(`dashboard.feeStatus.${props.status}`)
})
</script>