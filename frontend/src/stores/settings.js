import { defineStore } from 'pinia'
import { ref } from 'vue'
import i18n from '@/i18n'

export const useSettingsStore = defineStore('settings', () => {
  const locale = ref(localStorage.getItem('lang') || 'es')

  // Inicializa i18n con el valor guardado
  i18n.global.locale.value = locale.value

  function setLocale(newLocale) {
    locale.value = newLocale
    i18n.global.locale.value = newLocale
    localStorage.setItem('lang', newLocale)
  }

  return { locale, setLocale }
})