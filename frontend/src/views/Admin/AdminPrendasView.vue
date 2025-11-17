<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.admin.nav.prendas') }}
    </h1>

    <AdminCard>
      <template #title>
        <div class="flex justify-between items-center">
          <span>{{ t('adminPrendas.view.title') }}</span>
          <button @click="adminStore.openCreatePrendaModal()" class="btn btn-primary !py-1 !px-3 !text-xs">
            {{ t('adminPrendas.actions.create') }}
          </button>
        </div>
      </template>
      
      <div v-if="adminStore.isLoadingPrendas" class="text-gray-400 p-4 text-center">
        {{ t('dashboard.view.feeLoading') }}
      </div>
      <div v-else-if="adminStore.errorPrendas" class="text-red-500 p-4 text-center">
        {{ t(adminStore.errorPrendas) }}
      </div>
      
      <div v-else class="flex flex-col">
        <div class="hidden sm:grid grid-cols-5 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
          <span class="col-span-2">{{ t('adminPrendas.table.prenda') }}</span>
          <span>{{ t('adminPrendas.table.variants') }}</span>
          <span class="text-right">{{ t('adminPrendas.table.price') }}</span>
          <span class="text-right">{{ t('adminPrendas.table.actions') }}</span>
        </div>

        <div v-if="adminStore.prendasList.length === 0" class="text-center text-gray-400 py-6">
          {{ t('adminPrendas.search.noResults') }}
        </div>

        <div 
          v-for="prenda in adminStore.prendasList" 
          :key="prenda.id"
          class="grid grid-cols-3 sm:grid-cols-5 gap-y-4 gap-x-2 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          <div class="sm:col-span-2 col-span-3 flex items-center gap-4">
            <img 
              :src="prenda.imagen_url || 'https://via.placeholder.com/80'" 
              class="h-12 w-12 rounded-md object-cover bg-gray-700" 
            />
            <div>
              <span class="font-bold">{{ prenda.nombre }}</span>
              <span class="block text-gray-400 text-sm">{{ prenda.descripcion.substring(0, 50) }}...</span>
            </div>
          </div>

          <div class="sm:col-span-1 col-span-1">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPrendas.table.variants') }}: </span>
            <span class="font-bold">{{ prenda.variantes.length }}</span>
          </div>

          <div class="sm:col-span-1 col-span-1 text-right">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminPrendas.table.price') }}: </span>
            <span class="font-bold">€{{ prenda.precio }}</span>
          </div>

          <div class="sm:col-span-1 col-span-3 text-right flex sm:justify-end gap-2">
<span v-if="loadingPrendaId === prenda.id" class="material-symbols-outlined animate-spin text-red-600">
              progress_activity
            </span>

            <template v-else>
              <button @click="adminStore.openEditPrendaModal(prenda)" class="btn btn-secondary !py-1 !px-3 !text-xs">
                {{ t('adminPrendas.table.edit') }}
              </button>
              
              <button @click="handleDelete(prenda.id)" class="btn btn-secondary !py-1 !px-3 !text-xs !bg-red-800 hover:!bg-red-700">
                {{ t('adminPrendas.table.delete') }}
              </button>
            </template>
          </div>
        </div>
      </div>
    </AdminCard>
    <PrendaEditModal 
      v-if="adminStore.isPrendaModalOpen"
      @close="adminStore.closePrendaModal"
    />
    </div>
</template>

<script setup>
import { onMounted,ref } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import AdminCard from '@/components/Dashboard/shared/AdminCard.vue'
import PrendaEditModal from '@/components/dashboard/sections/PrendaEditModal.vue'
const { t } = useI18n()
const adminStore = useAdminStore()
const loadingPrendaId = ref(null) // <-- 2. Añade ref para el spinner
onMounted(() => {
  adminStore.fetchAllPrendas()
})
async function handleDelete(prendaId) {
  // Pide confirmación
  if (confirm(t('adminPrendas.actions.confirmDelete'))) {
    loadingPrendaId.value = prendaId
    try {
      await adminStore.deletePrenda(prendaId)
      // La lista se refresca automáticamente desde la acción del store
    } catch (error) {
      // Muestra el error (ej. si la prenda está en un pedido)
      alert(t(error.message)) 
    } finally {
      loadingPrendaId.value = null
    }
  }
}

</script>