import { createI18n } from 'vue-i18n'
import messages from '@intlify/unplugin-vue-i18n/messages'

// Lee el idioma guardado o usa español por defecto
const savedLocale = localStorage.getItem('lang') || 'es'

const i18n = createI18n({
  legacy: false,             // Composition API
  globalInjection: true,     // Permite usar $t() en templates sin importar el componente
  locale: savedLocale,
  fallbackLocale: 'es',
  messages,
  datetimeFormats: {
    es: { short: { year: 'numeric', month: '2-digit', day: '2-digit' } },
    en: { short: { year: 'numeric', month: 'short', day: 'numeric' } },
    gal:{ short:{ year: 'numeric', month: '2-digit', day: '2-digit' } }
  }
})

export default i18n