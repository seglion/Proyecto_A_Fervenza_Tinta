<template>
  <AuthLayout>

    <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>
    <div class="flex flex-col items-center justify-center text-center gap-6 p-4">
      
      <h1 class="font-display uppercase tracking-wider font-bold text-3xl sm:text-5xl">
        {{ t('resetPassword.requestTitle') }}
      </h1>

      <p class="text-base sm:text-lg">{{ t('resetPassword.requestDetail') }}</p>

      <div v-if="mensajeExitoKey" class="mb-4 p-4 text-center text-white rounded-md bg-black/80 border border-red-600">
        {{ t(mensajeExitoKey) }}
      </div>

      <form v-else @submit.prevent="onSubmit" class="w-full flex flex-col gap-6">
        <AuthInput
          name="email"
          type="email"
          placeholder="example@example.com"
          :label="t('login.emailLabel')"
        />
        
        <p v-if="mensajeErrorKey" class="text-red-500">{{ t(mensajeErrorKey, 'apiErrors.genericError') }}</p>

        <button type="submit" class="btn btn-primary w-full" :disabled="cargando">
          {{ cargando ? t('resetPassword.sending') : t('resetPassword.sendLink') }}
        </button>
      </form>

      <div class="mt-8 text-center">
        <RouterLink to="/login" class="font-bold text-white underline hover:text-red-600">
          {{ t('resetPassword.backToLogin') }}
        </RouterLink>
      </div>

    </div>
  </AuthLayout>
</template>

<script setup>
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'

import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import { useForm } from 'vee-validate'
import { object, string } from 'yup'
import AuthLayout from '@/components/Auth/AuthLayout.vue'
import AuthInput from '@/components/Auth/AuthInput.vue'

const { t } = useI18n()
const authStore = useAuthStore()

const cargando = ref(false)
const mensajeExitoKey = ref(null)
const mensajeErrorKey = ref(null)

// Validación de VeeValidate
const { handleSubmit } = useForm({
  validationSchema: object({
    email: string().email(t('validation.emailInvalid')).required(t('validation.emailRequired'))
  })
})

// Lógica de Submit
const onSubmit = handleSubmit(async (values) => {
  cargando.value = true
  mensajeErrorKey.value = null
  
  try {
    await authStore.requestPasswordReset(values.email)
    mensajeExitoKey.value = 'resetPassword.requestSuccess'
  } catch (error) {
    mensajeErrorKey.value = error.message
  } finally {
    cargando.value = false
  }
})
</script>