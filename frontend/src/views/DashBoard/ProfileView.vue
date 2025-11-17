<template>
  <div>
    <h1
      class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl"
    >
      {{ t('dashboard.profile.viewTitle') }} </h1>

    <InfoCard :title="t('dashboard.profile.viewTitle')"> <nav class="flex flex-wrap border-b border-gray-700">
        <button
          @click="activeTab = 'profile'"
          :class="getTabClasses('profile')"
        >
          {{ t('dashboard.profile.tabs.account') }}
        </button>
        <button
          @click="activeTab = 'password'"
          :class="getTabClasses('password')"
        >
          {{ t('dashboard.profile.tabs.security') }}
        </button>
      </nav>

      <div class="py-6">
        <div v-show="activeTab === 'profile'">
          <ProfileUpdateForm />
        </div>

        <div v-show="activeTab === 'password'">
          <PasswordChangeForm />
        </div>
      </div>
    </InfoCard>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useI18n } from 'vue-i18n';
import InfoCard from '@/components/Dashboard/shared/InfoCard.vue';
import ProfileUpdateForm from '@/components/Dashboard/sections/ProfileUpdateForm.vue';
import PasswordChangeForm from '@/components/Dashboard/sections/PasswordChangeForm.vue';

const { t } = useI18n();

// Estado para controlar la pestaña activa
const activeTab = ref('profile'); // 'profile' o 'password'

// Clases dinámicas para los botones de las pestañas
const getTabClasses = (tabName) => {
  const isActive = activeTab.value === tabName;
  
  // Clases base (Mobile-first)
  let classes = [
    'py-3', 'px-4', 'sm:py-4', 'sm:px-6',
    'font-mono', 'font-bold', 'text-sm', 'sm:text-base',
    'uppercase', 'tracking-wider', 'transition-colors',
    'border-b-2', 'sm:border-b-4'
  ];

  if (isActive) {
    // Estilo ACTIVO (rojo)
    classes.push('border-brand-red', 'text-white');
  } else {
    // Estilo INACTIVO (gris)
    classes.push('border-transparent', 'text-gray-500', 'hover:text-gray-300');
  }
  
  return classes;
};
</script>