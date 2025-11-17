<template>
  <div class="language-selector space-x-2 sm:space-x-4">
    <a
      href="#"
      @click.prevent="settingsStore.setLocale('es')"
      :class="['lang-link', { 'lang-active': settingsStore.locale === 'es' }]"
    >
      ES
    </a>

    <span class="text-gray-500 text-xs sm:text-sm">/</span>

    <a
      href="#"
      @click.prevent="settingsStore.setLocale('en')"
      :class="['lang-link', { 'lang-active': settingsStore.locale === 'en' }]"
    >
      EN
    </a>

    <span class="text-gray-500 text-xs sm:text-sm">/</span>

    <a
      href="#"
      @click.prevent="settingsStore.setLocale('gal')"
      :class="['lang-link', { 'lang-active': settingsStore.locale === 'gal' }]"
    >
      GAL
    </a>
  </div>
</template>

<script setup>


import { useSettingsStore } from '@/stores/settings'
const settingsStore = useSettingsStore()


</script>

<style scoped>
/* Estilos para los enlaces de idioma */
.lang-link {
  font-family: 'Space Mono', monospace;
  font-weight: 700;
  color: #a8a29e; /* stone-400 */
  text-decoration: none;
  transition: color 0.2s ease-in-out;
  
  /* --- Estilo Responsive (Mobile-First) --- */
  
  /* 1. Estilo base (Móvil) */
  font-size: 12px; /* text-sm */

}

.lang-link:hover {
  color: #ffffff;
}

.lang-active {
  color: #dc2626; /* red-600 */
  text-decoration: underline;
  text-underline-offset: 4px;
}
</style>