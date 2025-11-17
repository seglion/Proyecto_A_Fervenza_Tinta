<template>
  <AuthLayout>
       <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>
    <div class="flex flex-col items-center justify-center text-center gap-6 p-4">
      
      <h1 class="font-display uppercase tracking-wider font-bold text-3xl sm:text-5xl">
        {{ t('verifyEmail.title') }}
      </h1>

      <div v-if="cargando" class="text-lg">
        <p>{{ t('verifyEmail.verifying') }}</p>
      </div>

      <div v-if="mensajeExitoKey" class="flex flex-col items-center gap-4 w-full">
        <p class="text-lg" style="color: #4ade80;">{{ t(mensajeExitoKey) }}</p>
        <p class="text-base sm:text-lg">{{ t('verifyEmail.successDetail') }}</p>
        <RouterLink to="/login" class="btn btn-primary w-full sm:w-auto">
          {{ t('login.title') }}
        </RouterLink>
      </div>

      <div v-if="mensajeErrorKey" class="flex flex-col items-center gap-4 w-full">
        <p class="text-lg text-red-500">{{ t(mensajeErrorKey) }}</p>
        <p class="text-base sm:text-lg">{{ t('verifyEmail.errorDetail') }}</p>
        <RouterLink to="/register" class="btn btn-secondary w-full sm:w-auto">
          {{ t('register.title') }}
        </RouterLink>
      </div>

    </div>
  </AuthLayout>
</template>

<script setup>
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import AuthLayout from '@/components/Auth/AuthLayout.vue'

const route = useRoute()
const authStore = useAuthStore()
const { t } = useI18n()

const cargando = ref(true)
// 1. Renombramos las variables para que guarden "Keys" (claves)
const mensajeExitoKey = ref(null)
const mensajeErrorKey = ref(null)

onMounted(async () => {
  const token = route.query.token

  if (!token) {
    mensajeErrorKey.value = 'verifyEmail.noToken' 
    cargando.value = false
    return
  }

  try {
    await authStore.verifyEmail(token)
    mensajeExitoKey.value = 'verifyEmail.success'
  } catch (error) {
    mensajeErrorKey.value = error.message 
  } finally {
    cargando.value = false
  }
})
</script>