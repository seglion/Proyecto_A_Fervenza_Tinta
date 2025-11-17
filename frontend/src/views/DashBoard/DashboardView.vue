<template>
  <div>
    
    <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>

    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.nav.home') }}
    </h1>

    <div class="space-y-8">
      <CuotaCard />
      
      <InfoCard :title="t('dashboard.view.storeTitle')">
        
        <div v-if="adminStore.isLoadingPrendas" class="text-gray-400 p-4 text-center">
          {{ t('dashboard.view.feeLoading') }}
        </div>

        <div v-else class="p-6">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <div 
              v-for="prenda in firstTwoPrendas" 
              :key="prenda.id"
              class="border border-gray-800 rounded-lg overflow-hidden"
            >
              <div class="h-48 bg-gray-900 flex items-center justify-center p-2">
                <img 
                  :src="prenda.imagen_url || 'https://via.placeholder.com/400'" 
                  :alt="prenda.nombre"
                  class="w-auto h-auto max-w-full max-h-full object-contain"
                />
              </div>
              <div class="p-3 bg-gray-900/50">
                <h3 class="font-bold text-white truncate">{{ prenda.nombre }}</h3>
                <p class="font-mono text-sm text-gray-400">€{{ prenda.precio }}</p>
              </div>
            </div>

            <RouterLink 
              :to="{ name: 'merchandise-store' }"
              v-if="adminStore.prendasList.length > 2"
              class="border-2 border-dashed border-gray-700 rounded-lg 
                     flex items-center justify-center text-gray-400
                     hover:border-brand-red hover:text-white transition-colors"
            >
              <span>{{ t('dashboard.admin.view.viewAll') }} &rarr;</span>
            </RouterLink>

          </div>
          
          <div v-if="adminStore.prendasList.length === 0" class="text-center">
            <p class="text-gray-400 mb-4">{{ t('dashboard.view.storeEmpty') }}</p>
            <RouterLink :to="{ name: 'merchandise-store' }" class="btn btn-secondary">
              {{ t('dashboard.view.storeButton') }}
            </RouterLink>
          </div>
        </div>

      </InfoCard>
    </div>

  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue' // <-- 1. Importa computed
import { useI18n } from 'vue-i18n'
import { RouterLink } from 'vue-router'
import { useAdminStore } from '@/stores/adminStore' // <-- 2. Importa adminStore
import InfoCard from '@/components/Dashboard/shared/InfoCard.vue'
import CuotaCard from '@/components/Dashboard/sections/CuotaCard.vue'
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'

const { t } = useI18n()
const adminStore = useAdminStore() // <-- 3. Inicializa adminStore

// 4. Carga las prendas al montar la vista
onMounted(() => {
  adminStore.fetchAllPrendas()
})

// 5. Computed para coger solo las 2 primeras prendas
const firstTwoPrendas = computed(() => {
  return adminStore.prendasList.slice(0, 2)
})
</script>