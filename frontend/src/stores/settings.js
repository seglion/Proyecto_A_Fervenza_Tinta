import { defineStore } from 'pinia'
import { ref } from 'vue'

const initialLocale = localStorage.getItem('lang') || 'es'

// LA PALABRA "EXPORT" ES LA CLAVE
export const useSettingsStore = defineStore('settings', () => {
  const locale = ref(initialLocale)

  function setLocale(newLocale) {
    locale.value = newLocale
    localStorage.setItem('lang', newLocale)
  }

  return { locale, setLocale }
})