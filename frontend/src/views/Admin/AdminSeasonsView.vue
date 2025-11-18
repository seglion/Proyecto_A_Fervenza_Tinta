<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.admin.nav.seasons') }}
    </h1>

    <AdminCard>
      <template #title>
        <div class="flex justify-between items-center">
          <span>{{ t('adminSeasons.view.title') }}</span>
          <button @click="openSeasonModal(null)" class="btn btn-primary !py-1 !px-3 !text-xs">
            {{ t('adminSeasons.actions.create') }}
          </button>
        </div>
      </template>
      
      <div v-if="adminStore.isLoadingSeasons" class="text-gray-400 p-4 text-center">
        {{ t('dashboard.view.feeLoading') }}
      </div>
      <div v-else-if="adminStore.errorSeason" class="text-red-500 p-4 text-center">
        {{ t(adminStore.errorSeason) }}
      </div>
      
      <div v-else class="flex flex-col">
        <div class="hidden sm:grid grid-cols-4 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
          <span>{{ t('adminSeasons.table.name') }}</span>
          <span>{{ t('adminSeasons.table.startDate') }}</span>
          <span>{{ t('adminSeasons.table.endDate') }}</span>
          <span class="text-right">{{ t('adminSeasons.table.actions') }}</span>
        </div>

        <div v-if="adminStore.allSeasonsList.length === 0" class="text-center text-gray-400 py-6">
          {{ t('adminSeasons.view.noSeasons') }}
        </div>

        <div 
          v-for="season in adminStore.allSeasonsList" 
          :key="season.id"
          class="grid grid-cols-2 sm:grid-cols-4 gap-y-4 gap-x-2 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminSeasons.table.name') }}: </span>
            <span class="font-bold">{{ season.nombre_temporada }}</span>
          </div>

          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminSeasons.table.startDate') }}: </span>
            <span class="text-gray-400 text-sm">{{ d(new Date(season.fecha_inicio), 'short') }}</span>
          </div>

          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminSeasons.table.endDate') }}: </span>
            <span class="text-gray-400 text-sm">{{ d(new Date(season.fecha_fin), 'short') }}</span>
          </div>

          <div class="sm:col-span-1 col-span-2 text-right">
            <button 
              @click="openSeasonModal(season)"
              class="btn btn-secondary !py-1 !px-3 !text-xs"
            >
              {{ t('adminSeasons.actions.edit') }}
            </button>
          </div>
        </div>
      </div>
    </AdminCard>
    
    <SeasonEditModal 
      v-if="isModalOpen"
      :season-data="selectedSeason"
      @close="closeSeasonModal"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import AdminCard from '@/components/Dashboard/shared/AdminCard.vue'
// (Crearemos este componente en el sig. paso)
import SeasonEditModal from '@/components/Dashboard/sections/SeasonEditModal.vue'

const { t, d } = useI18n()
const adminStore = useAdminStore()

// --- Lógica del Modal ---
const isModalOpen = ref(false)
const selectedSeason = ref(null) // null = Crear, Objeto = Editar

function openSeasonModal(season) {
  selectedSeason.value = season // Guarda la temporada a editar (o null)
  isModalOpen.value = true
}

function closeSeasonModal() {
  isModalOpen.value = false
  selectedSeason.value = null // Limpia
}
// -----------------------

// Carga inicial de datos
onMounted(() => {
  adminStore.fetchAllSeasons()
})
</script>