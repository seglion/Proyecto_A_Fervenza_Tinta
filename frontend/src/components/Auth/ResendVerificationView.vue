<template>
  <AuthLayout>
    <div class.="flex flex-col items-center justify-center text-center gap-6 p-4">
      
      <h1 class=" mb-2 font-display uppercase tracking-wider font-bold text-3xl sm:text-4xl">
        {{ t('resendVerification.title') }}
      </h1>

      <p class="text-base sm:text-lg mb-2">{{ t('resendVerification.detail') }}</p>

      <div v-if="mensajeExitoKey" class="mb-4  p-4 text-center text-white rounded-md bg-black/80 border border-red-600">
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
          {{ cargando ? t('resetPassword.sending') : t('resendVerification.sendLink') }}
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

// Validación
const { handleSubmit } = useForm({
  validationSchema: object({
    email: string().email(t('validation.emailInvalid')).required(t('validation.emailRequired'))
  })
})

const onSubmit = handleSubmit(async (values) => {
  cargando.value = true
  mensajeErrorKey.value = null
  
  try {
    await authStore.resendVerificationEmail(values.email)
    mensajeExitoKey.value = 'resendVerification.success'
  } catch (error) {
    mensajeErrorKey.value = error.message
  } finally {
    cargando.value = false
  }
})
</script>