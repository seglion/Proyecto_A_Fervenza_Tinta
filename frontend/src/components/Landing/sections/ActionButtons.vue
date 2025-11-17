<template>
  <div class="flex flex-col sm:flex-row flex-wrap gap-4 justify-start">
    <RouterLink
      to="/login"
      class="btn btn-primary"
      :class="responsiveButtonClasses"
    >
      {{ t('login.title') }}
    </RouterLink>

    <RouterLink
      to="/register"
      class="btn btn-secondary"
      :class="responsiveButtonClasses"
    >
      {{ t('register.title') }}
    </RouterLink>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 2. Centralizamos las clases responsive
const responsiveButtonClasses = computed(() => [
  'flex justify-center', // Para centrar el texto
  'w-full sm:w-auto', // Móvil: Ancho completo. Desktop: Ancho automático
  'h-12 sm:h-14',       // Altura
  'px-6 sm:px-8',       // Padding
  'text-base sm:text-lg', // Tamaño de fuente
  // 'min-w-[120px]' ya no es necesario gracias a 'sm:w-auto'
])
</script>