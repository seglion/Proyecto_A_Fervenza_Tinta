<template>
  <MainLayout>
    <main class="container mx-auto px-4 py-16 sm:py-24 text-white">
      <h1 class="font-display font-bold uppercase text-4xl sm:text-5xl mb-8">
        {{ t('footer.links.contact') }}
      </h1>
      <p class="text-gray-300">
        [Aquí va tu formulario o información de contacto.]
      </p>
    </main>
  </MainLayout>
</template>

<script setup>
import MainLayout from '@/components/Landing/layout/MainLayout.vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>