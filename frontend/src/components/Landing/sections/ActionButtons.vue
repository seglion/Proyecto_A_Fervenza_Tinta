<template>
  <div class="flex flex-wrap gap-4 justify-start">
    <RouterLink
      to="/login"
      class="btn btn-primary min-w-[120px] h-12 sm:h-14 px-6 sm:px-8"
    >
     {{t('login.title')}}
    </RouterLink>

    <RouterLink
      to="/register"
      class="btn btn-secondary min-w-[120px] h-12 sm:h-14 px-6 sm:px-8"
    >
      {{t('register.title')}}


    </RouterLink>
  </div>
</template>


<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()// No necesitas emits ni funciones aquí.
// <RouterLink> gestiona la navegación directamente.
</script>