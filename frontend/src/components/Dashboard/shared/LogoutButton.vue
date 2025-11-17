<template>
  <button
    @click="handleLogout"
    class="
      flex w-full items-center gap-3 rounded-md px-4 py-3
      text-gray-400
      transition-colors
      hover:bg-red-600 hover:text-white
    "
  >
    <span class="material-symbols-outlined">logout</span>
    <span>{{ t('dashboard.nav.logout') }}</span>
  </button>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const authStore = useAuthStore();

const handleLogout = () => {
  // Llama a la acción de logout del store.
  // El store se encargará de limpiar localStorage y redirigir a /login
  authStore.logout();
};
</script>

<style scoped>
/* Estilos para el icono de Material Symbols */
.material-symbols-outlined {
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
  font-size: 24px;
}
</style>