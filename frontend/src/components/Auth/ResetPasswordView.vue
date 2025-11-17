<template>
  <AuthLayout>
    <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>
    <div class="flex flex-col items-center justify-center text-center gap-6 p-4">

      <h1 class="font-display uppercase tracking-wider font-bold text-3xl sm:text-5xl">
        {{ t('resetPassword.newTitle') }}
      </h1>

      <div v-if="mensajeExitoKey" class="flex flex-col items-center gap-4 w-full">
        <p class="text-lg" style="color: #4ade80;">{{ t(mensajeExitoKey) }}</p>
        <RouterLink to="/login" class="btn btn-primary w-full sm:w-auto">
          {{ t('login.title') }}
        </RouterLink>
      </div>

      <AuthForm
        v-else
        :fields="fields"
        :submitLabel="t('resetPassword.saveButton')"
        :onSubmit="onSubmit"
        :loading="cargando"
        :error="mensajeErrorKey ? t(mensajeErrorKey, 'apiErrors.genericError') : null"
      />
      
      <div v-if="tokenError" class="text-red-500 text-lg">
        {{ t(tokenError) }}
      </div>
      
    </div>
  </AuthLayout>
</template>

<script setup>
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'

import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import { useForm } from 'vee-validate'
import { object, string, ref as yupRef } from 'yup'
import AuthLayout from '@/components/Auth/AuthLayout.vue'
import AuthForm from '@/components/Auth/AuthForm.vue'

const { t } = useI18n()
const authStore = useAuthStore()
const route = useRoute()

const cargando = ref(false)
const mensajeExitoKey = ref(null)
const mensajeErrorKey = ref(null)
const tokenError = ref(null) 
const token = ref(null)

const fields = computed(() => [
  { name: 'password', type: 'password', placeholder: 'Crea tu nueva contraseña', label: t('register.passwordLabel') },
  { name: 'passwordConfirm', type: 'password', placeholder: 'Confirma la contraseña', label: t('register.passwordConfirmLabel') },
])

const schema = computed(() => object({
  password: string()
    .required(t('validation.passwordRequired'))
    .min(8, t('validation.passwordMin'))
    .matches(/[a-z]/, t('validation.passwordLowercase'))
    .matches(/[A-Z]/, t('validation.passwordUppercase'))
    .matches(/[0-9]/, t('validation.passwordNumber'))
    .matches(/[^A-Za-z0-9]/, t('validation.passwordSpecial')),
  passwordConfirm: string()
    .required(t('validation.passwordRequired'))
    .oneOf([yupRef('password')], t('validation.passwordConfirmMatch')),
}))

const { handleSubmit } = useForm({ validationSchema: schema })

const onSubmit = handleSubmit(async (values) => {
  cargando.value = true
  mensajeErrorKey.value = null
  
  try {
    await authStore.resetPassword(token.value, values.password)
    mensajeExitoKey.value = 'resetPassword.newSuccess'
  } catch (error) {
    mensajeErrorKey.value = error.message
  } finally {
    cargando.value = false
  }
})

onMounted(() => {
  const tokenFromUrl = route.query.token
  if (!tokenFromUrl) {
    tokenError.value = 'verifyEmail.noToken' 
  } else {
    token.value = tokenFromUrl
  }
})
</script>