<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-lg p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ t('adminUsers.detail.title') }}
        </h2>
        <button @click="handleClose" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div v-if="adminStore.isLoadingDetail" class="text-gray-400 text-center p-8">
        <span class="material-symbols-outlined animate-spin text-red-600 text-4xl">
          progress_activity
        </span>
      </div>

      <div v-else-if="adminStore.errorDetail" class="text-red-500 text-center p-8">
        <p>{{ t(adminStore.errorDetail) }}</p>
      </div>
      
      <div v-else-if="adminStore.userDetail" class="space-y-4">
        
        <div class="flex items-center gap-4">
          <img 
            :src="adminStore.userDetail.url_avatar || 'https://via.placeholder.com/80'" 
            class="h-16 w-16 rounded-full object-cover bg-gray-700" 
          />
          <div>
            <p class="text-lg text-red-600 font-bold">
              {{ adminStore.userDetail.nombre }} {{ adminStore.userDetail.apellidos }}
            </p>
            <p class="text-gray-400 text-sm">{{ adminStore.userDetail.email }}</p>
          </div>
        </div>
        
        <hr class="border-gray-700">
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <InfoRow :label="t('register.nicknameLabel')" :value="adminStore.userDetail.apodo" />
          <InfoRow :label="t('register.phoneLabel')" :value="adminStore.userDetail.numero_telefono" />
          <InfoRow :label="t('dashboard.nav.currentRole')" :value="t(`dashboard.roles.${adminStore.userDetail.rol}`)" />
          
          <div class="py-2">
            <label class="block text-sm font-medium text-gray-400">
              {{ t('adminUsers.table.status') }}
            </label>
            <UserStatusBadge
              class="mt-1"
              :esta_activo="adminStore.userDetail.esta_activo"
              :aprobado_por_admin="adminStore.userDetail.aprobado_por_admin"
            />
          </div>
        </div>
        
      </div>
      </div>
  </div>
</template>

<script setup>
import { useAdminStore } from '@/stores/adminStore';
import { useI18n } from 'vue-i18n';
// Asegúrate de que has creado este componente 'InfoRow.vue'
import InfoRow from '../shared/InfoRow.vue'; 
import UserStatusBadge from '../shared/UserStatusBadge.vue'; 

const emit = defineEmits(['close']);
const { t } = useI18n();
const adminStore = useAdminStore();

function handleClose() {
  emit('close');
}
</script>