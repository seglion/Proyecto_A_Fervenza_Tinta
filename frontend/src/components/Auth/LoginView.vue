<template>
  <AuthLayout>
    <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>

    <div class="mb-8 text-center">
      <h1 class="font-display text-3xl sm:text-5xl font-bold uppercase tracking-wider">
        {{ t('login.title') }}
      </h1>
    </div>

    <AuthForm :fields="fields" :submitLabel="t('login.submit')" :onSubmit="onSubmit" :loading="cargando"
      :errorMessage="mensajeErrorKey ? t(mensajeErrorKey, 'apiErrors.genericError') : null" />

    <div class="mt-8 text-center">
      <p class="text-sm text-gray-300">
        {{ t('login.noAccount') }}
        <RouterLink to="/register" class="font-bold text-white underline hover:text-red-600">
          {{ t('login.registerLink') }}
        </RouterLink>
      </p>
      <p class="text-sm text-gray-300 mt-2">
        <RouterLink to="/request-password-reset" class="font-bold text-white underline hover:text-red-600">
          {{ t('login.forgotPassword') }}
        </RouterLink>
      </p>
      <p class="text-sm text-gray-300 mt-2">
        <RouterLink to="/resend-verification" class="font-bold text-white underline hover:text-red-600">
          {{ t('login.resendVerification') }}
        </RouterLink>
      </p>
    </div>
  </AuthLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { object, string } from 'yup'
import { useForm } from 'vee-validate'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import AuthLayout from './AuthLayout.vue'
import AuthForm from './AuthForm.vue'
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'

const { t } = useI18n()
const authStore = useAuthStore()

const cargando = ref(false)
const mensajeErrorKey = ref(null)

const fields = computed(() => [
  { name: 'email', type: 'email', placeholder: 'example@example.com', label: t('login.emailLabel') },
  { name: 'password', type: 'password', placeholder: '********', label: t('login.passwordLabel') },
])

const schema = computed(() => object({
  email: string().email(t('validation.emailInvalid')).required(t('validation.emailRequired')),
  password: string().required(t('validation.passwordRequired')),
}))

const { handleSubmit } = useForm({
  validationSchema: schema,
  initialValues: { email: '', password: '' }
})

const onSubmit = handleSubmit(async (values) => {
  cargando.value = true
  mensajeErrorKey.value = null
  try {
    await authStore.login(values.email, values.password)
  } catch (error) {
    mensajeErrorKey.value = error.message
  } finally {
    cargando.value = false
  }
})
</script>