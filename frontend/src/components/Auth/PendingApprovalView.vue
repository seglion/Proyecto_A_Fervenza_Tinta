<template>
  <AuthLayout>
    <div class="flex flex-col items-center justify-center text-center gap-6 p-4">
      
      <h1 class="font-display uppercase tracking-wider font-bold text-3xl sm:text-5xl">
        {{ t('pendingApproval.title') }}
      </h1>

      <p class="text-base sm:text-lg max-w-md">
        {{ t('pendingApproval.message') }}
      </p>
      
      <svg class="w-16 h-16 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
      </svg>

      <button 
        @click="handleLogout" 
        class="btn btn-secondary w-full sm:w-auto mt-4"
      >
        {{ t('pendingApproval.logout') }}
      </button>

    </div>
  </AuthLayout>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import AuthLayout from '@/components/Auth/AuthLayout.vue'

const { t } = useI18n()
const authStore = useAuthStore()

const handleLogout = () => {
  authStore.logout()
}
</script>