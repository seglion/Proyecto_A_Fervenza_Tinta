<script setup>
import { RouterView } from 'vue-router'
import { useSettingsStore } from '@/stores/settings'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import { watch } from 'vue'

// --- Sincronización de Idioma ---
// Conecta el 'locale' de Pinia (settingsStore) con
// el 'locale' del plugin de traducción (i18n).
const settingsStore = useSettingsStore()
const { locale: i18nLocale } = useI18n()
i18nLocale.value = settingsStore.locale
watch(
  () => settingsStore.locale,
  (newLocale) => {
    i18nLocale.value = newLocale
  },
)

// --- Sincronización de Autenticación ---
// Carga los datos del perfil del usuario (apodo, rol, etc.)
// al iniciar la aplicación, usando el token que ya está
// guardado en localStorage.
const authStore = useAuthStore()
authStore.fetchProfile()
</script>

<template>
  <RouterView />
</template>
