<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.admin.nav.orderSeasons') }}
    </h1>

    <AdminCard>
      <template #title>
        <div class="flex justify-between items-center">
          <span>{{ t('adminOrderSeasons.view.title') }}</span>
          <button @click="openSeasonModal(null)" class="btn btn-primary !py-1 !px-3 !text-xs">
            {{ t('adminSeasons.actions.create') }} </button>
        </div>
      </template>
      
      <div v-if="adminStore.isLoadingOrderSeasons" class="text-gray-400 p-4 text-center">
        {{ t('dashboard.view.feeLoading') }}
      </div>
      <div v-else-if="adminStore.errorOrderSeason" class="text-red-500 p-4 text-center">
        {{ t(adminStore.errorOrderSeason) }}
      </div>
      
      <div v-else class="flex flex-col">
        <div class="hidden sm:grid grid-cols-5 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
          <span>{{ t('adminSeasons.table.name') }}</span>
          <span>{{ t('adminSeasons.table.startDate') }}</span>
          <span>{{ t('adminSeasons.table.endDate') }}</span>
          <span>{{ t('adminOrderSeasons.table.status') }}</span>
          <span class="text-right">{{ t('adminSeasons.table.actions') }}</span>
        </div>

        <div v-if="adminStore.allOrderSeasonsList.length === 0" class="text-center text-gray-400 py-6">
          {{ t('adminSeasons.view.noSeasons') }}
        </div>

        <div 
          v-for="season in adminStore.allOrderSeasonsList" 
          :key="season.id"
          class="grid grid-cols-2 sm:grid-cols-5 gap-y-4 gap-x-2 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          <div class="sm:col-span-1 col-span-2">
            <span class="font-bold">{{ season.nombre_temporada }}</span>
          </div>

          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminSeasons.table.startDate') }}: </span>
          <span class="text-gray-400 text-sm">{{ d(new Date(season.fecha_inicio), 'short') }}</span>
          
          <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminSeasons.table.endDate') }}: </span>
          <span class="text-gray-400 text-sm">{{ d(new Date(season.fecha_fin), 'short') }}</span>

          <div class="sm:col-span-1 col-span-1">
            <span 
              v-if="season.esta_activa" 
              class="px-3 py-1 text-sm font-bold rounded-full uppercase tracking-wider bg-green-600 text-white"
            >
              {{ t('adminOrderSeasons.status.active') }}
            </span>
            <span v-else class="px-3 py-1 text-sm font-bold rounded-full uppercase tracking-wider bg-gray-700 text-gray-200">
              {{ t('adminOrderSeasons.status.inactive') }}
            </span>
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
    
    <OrderSeasonEditModal 
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
// ¡Importa el nuevo modal (siguiente paso)!
import OrderSeasonEditModal from '@/components/dashboard/sections/OrderSeasonEditModal.vue'

const { t, d } = useI18n()
const adminStore = useAdminStore()

const isModalOpen = ref(false)
const selectedSeason = ref(null) 

function openSeasonModal(season) {
  selectedSeason.value = season 
  isModalOpen.value = true
}

function closeSeasonModal() {
  isModalOpen.value = false
  selectedSeason.value = null
}

onMounted(() => {
  adminStore.fetchAllOrderSeasons()
})
</script>