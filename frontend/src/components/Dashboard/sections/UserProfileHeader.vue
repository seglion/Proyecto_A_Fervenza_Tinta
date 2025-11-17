<template>
  <div class="flex flex-col items-center p-6 border-b border-gray-800 gap-3">
    
    <div 
      class="h-20 w-20 rounded-full bg-gray-700 overflow-hidden flex items-center justify-center text-center text-xs p-2"
    >
      <img 
        :alt="t('dashboard.profile.avatarAlt')" class="h-25 w-25 rounded-full object-cover bg-gray-700 mt-1"
        :src="avatarUrl"
      />
    </div>
    
    <h2 class="font-bold text-lg">
      {{ userNickname }}
    </h2>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  user: {
    type: Object,
    default: null,
  },
});

const { t } = useI18n();

// Muestra el apodo si existe, si no, el nombre, si no, "Usuario"
const userNickname = computed(() => {
  return  props.user?.nombre + ' ' + props.user?.apellidos || t('dashboard.profile.guest'); // Clave simplificada
});

// Muestra el avatar del usuario, o un fallback si no tiene
const avatarUrl = computed(() => {
  // TODO: Reemplaza esta string con una URL a tu avatar por defecto
 
  const defaultAvatar = 'https://via.placeholder.com/80'; 
  
  return props.user?.url_avatar || defaultAvatar;
});
</script>