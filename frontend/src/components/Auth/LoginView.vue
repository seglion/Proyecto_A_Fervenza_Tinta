<template>

  <AuthLayout>
    <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>
    <div class="mb-8 text-center">
      <h1 class="font-display text-5xl font-bold uppercase tracking-wider">
        {{ t('login.title') }}
      </h1>
    </div>

    <AuthForm
      :fields="fields"
      :submitLabel="t('login.submit')" :onSubmit="onSubmit"
      :loading="cargando"
      :error="mensajeError"
    />

    <div class="mt-8 text-center">
      <p class="text-sm text-gray-300">
        {{ t('login.noAccount') }} <RouterLink to="/register" class="font-bold text-white underline hover:text-red-600">
          {{ t('login.registerLink') }} </RouterLink>
      </p>
    </div>
  </AuthLayout>
</template>


<script setup>
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'
import AuthLayout from './AuthLayout.vue'
import AuthForm from './AuthForm.vue'
import { object, string } from 'yup'
import { useForm } from 'vee-validate'
import { ref, computed } from 'vue' // <-- 1. Importa 'computed'
import { useRouter } from 'vue-router'
import apiClient from '@/api/axios' // <-- 2. Importa tu 'apiClient' configurado
import { useI18n } from 'vue-i18n' // <-- 3. Importa el hook de i18n

// --- Setup de i18n ---
const { t } = useI18n() // <-- 4. Obtén la función de traducción

// --- Refs estándar ---
const router = useRouter()
const cargando = ref(false)
const mensajeError = ref(null)
// const baseURL = import.meta.env.VITE_API_BASE_URL // <-- 5. Ya no se necesita aquí

// --- Fields (ahora como 'computed' para ser reactivo a los cambios de idioma) ---
const fields = computed(() => [
  {
    name: 'email',
    type: 'email',
    placeholder: 'example@example.com',
    label: t('login.emailLabel'), // <-- TRADUCIDO
  },
  {
    name: 'password',
    type: 'password',
    placeholder: '********',
    label: t('login.passwordLabel'), // <-- TRADUCIDO
  },
])

// --- Schema de Validación ---
// (Mantenemos los mensajes de Yup en español por simplicidad,
// pero también podrían hacerse reactivos si fuera necesario)
const schema = computed(() => {
  return object({
    email: string()
      .email(t('validation.emailInvalid')) // <-- TRADUCIDO
      .required(t('validation.emailRequired')), // <-- TRADUCIDO
    password: string()
      .required(t('validation.passwordRequired')), // <-- TRADUCIDO
  })
})


const { handleSubmit } = useForm({ validationSchema: schema })

// --- Lógica de Submit ---
const onSubmit = handleSubmit(async (values) => {
  cargando.value = true
  mensajeError.value = null

  try {
    // const url = baseURL + '/users/auth/token' // <-- 6. Ya no se necesita

    const data = new URLSearchParams()
    data.append('grant_type', 'password')
    data.append('username', values.email)
    data.append('password', values.password)
    data.append('scope', '')
    data.append('client_id', 'string')
    data.append('client_secret', '********')

    const config = {
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }

    // --- 7. Usa apiClient y solo el endpoint relativo ---
    const respuesta = await apiClient.post('/users/auth/token', data, config)
    const token = respuesta.data.access_token
    const refresh_token = respuesta.data.refresh_token

    localStorage.setItem('jwt_token', token)
    localStorage.setItem('refresh_token', refresh_token)

    router.push({ name: 'home' })
  } catch (error) {
    if (error.response) {
      mensajeError.value = error.response.data.detail || 'Credenciales incorrectas.'
    } else if (error.request) {
      mensajeError.value = 'No se pudo conectar con el servidor.'
    } else {
      mensajeError.value = error.message
    }
  } finally {
    cargando.value = false
  }
})
</script>

<style scoped>

</style>