<template>
  <div class="language-selector space-x-4">
    <a
      href="#"
      @click.prevent="setLocale('es')"
      :class="['lang-link', { 'lang-active': locale === 'es' }]"
    >
      ES
    </a>
    <span classclass="text-gray-500">/</span>
    <a
      href="#"
      @click.prevent="setLocale('en')"
      :class="['lang-link', { 'lang-active': locale === 'en' }]"
    >
      EN
    </a>
    <span class="text-gray-500">/</span>
    <a
      href="#"
      @click.prevent="setLocale('gal')"
      :class="['lang-link', { 'lang-active': locale === 'gal' }]"
    >
      GAL
    </a>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

// 1. Obtenemos 'locale' (el idioma activo)
const { locale } = useI18n()

// 2. Creamos la función para cambiar el idioma
const setLocale = (lang) => {
  locale.value = lang // Cambia el idioma en la app
  localStorage.setItem('lang', lang) // Guarda la preferencia
}
</script>

<style scoped>
/* Estilos para los enlaces de idioma */
.lang-link {
  font-family: 'Space Mono', monospace;
  font-size: 16px;
  font-weight: 700;
  color: #a8a29e; /* Un gris-piedra (Tailwind stone-400) */
  text-decoration: none;
  transition: color 0.2s ease-in-out;
}

.lang-link:hover {
  color: #ffffff; /* Blanco al pasar el ratón */
}

/* Estilo para el enlace activo */
.lang-active {
  color: #dc2626; /* Rojo (Tailwind red-600) */
  text-decoration: underline;
  text-underline-offset: 4px;
}
</style>