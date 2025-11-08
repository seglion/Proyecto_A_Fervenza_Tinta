import { createI18n } from 'vue-i18n'

// Importa tus archivos de idioma
import esMessages from './locales/es.json'
import enMessages from './locales/en.json'
import galMessages from './locales/gal.json'

// 1. Detecta el idioma guardado o usa 'es' por defecto
const defaultLocale = localStorage.getItem('lang') || 'gal'

// 2. Crea la instancia de i18n
const i18n = createI18n({
  legacy: false, // ¡IMPORTANTE! Usa el modo Composition API
  locale: defaultLocale, // Idioma por defecto
  fallbackLocale: 'es', // Idioma de respaldo si falta una traducción
  messages: {
    es: esMessages,
    en: enMessages,
    gal: galMessages,
  },
})

export default i18n