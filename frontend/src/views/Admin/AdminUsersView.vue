<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.nav.adminUsers') }}
    </h1>

    <AdminCard>
      <template #title>{{ t('adminUsers.view.title') }}</template>

      <nav class="flex flex-wrap border-b border-gray-700 mb-4">
        <button
          @click="statusFilter = 'all'"
          :class="getTabClasses('all')"
        >
          {{ t('adminUsers.filter.all') }}
        </button>
        <button
          @click="statusFilter = 'active'"
          :class="getTabClasses('active')"
        >
          {{ t('adminUsers.status.active') }}
        </button>
        
        <button
          @click="statusFilter = 'pending'"
          :class="getTabClasses('pending')"
        >
          <span v-if="adminStore.getPendingMembersCount > 0">
            {{ t('adminUsers.status.pendingWithCount', { count: adminStore.getPendingMembersCount }) }}
          </span>
          <span v-else>
            {{ t('adminUsers.status.pending') }}
          </span>
        </button>

        <button
          @click="statusFilter = 'inactive'"
          :class="getTabClasses('inactive')"
        >
          {{ t('adminUsers.status.inactive') }}
        </button>
      </nav>

      <div class="mb-4">
        <label for="userSearch" class="form-label">
          {{ t('adminUsers.search.label') }}
        </label>
        <input 
          id="userSearch"
          type="text" 
          v-model="searchTerm"
          :placeholder="t('adminUsers.search.placeholder')"
          class="input"
        />
      </div>
      
      <div v-if="adminStore.isLoadingUsers" class="text-gray-400 p-4 text-center">
        {{ t('dashboard.view.feeLoading') }}
      </div>
      
      <div v-else-if="adminStore.errorUsers" class="text-red-500 p-4 text-center">
        {{ t(adminStore.errorUsers) }}
      </div>

      <div v-else class="flex flex-col">
        <div class="hidden sm:grid grid-cols-3 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
          <span>{{ t('adminUsers.table.user') }}</span>

          <span>{{ t('adminUsers.table.status') }}</span>
          <span class="text-right">{{ t('adminUsers.table.actions') }}</span>
        </div>

        <div v-if="filteredUsers.length === 0" class="text-center text-gray-400 py-6">
          {{ t('adminUsers.search.noResults') }}
        </div>

        <div 
          v-for="user in filteredUsers" 
          :key="user.id"
          class="grid grid-cols-2 sm:grid-cols-3 gap-y-4 gap-x-2 sm:gap-4 py-3 border-b border-gray-800 items-center"
        >
          
          <div class="sm:col-span-1 col-span-2">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminUsers.table.user') }}: </span>
            <span class="font-bold">{{ user.nombre + ' ' + user.apellidos}}</span>
            <span v-if="user.apodo" class="text-gray-400 text-sm block sm:inline sm:ml-1">({{ user.apodo }})</span>
          </div>
          

          <div class="sm:col-span-1 col-span-1">
            <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('adminUsers.table.status') }}: </span>
            <UserStatusBadge
              :esta_activo="user.esta_activo"
              :aprobado_por_admin="user.aprobado_por_admin"
            />
          </div>

          <div class="sm:col-span-1 col-span-2 text-right flex sm:justify-end gap-2 items-center">
            
            <span v-if="loadingUserId === user.id" class="material-symbols-outlined animate-spin text-red-600">
              progress_activity
            </span>

            <template v-if="loadingUserId !== user.id && !user.aprobado_por_admin">
              <button 
            @click="adminStore.openDetailModal(user.id)"
            class="btn btn-secondary !py-1 !px-3 !text-xs"
          >
            {{ t('adminUsers.table.view') }} </button>
              <button @click="handleApprove(user.id)" class="btn btn-primary !py-1 !px-3 !text-xs !bg-green-600 hover:!bg-green-700">
                {{ t('adminUsers.actions.approve') }}
              </button>
              <button @click="handleReject(user.id)" class="btn btn-secondary !py-1 !px-3 !text-xs">
                {{ t('adminUsers.actions.reject') }}
              </button>
              
          

            </template>

            <template v-else-if="loadingUserId !== user.id && user.aprobado_por_admin">
              <button 
            @click="adminStore.openDetailModal(user.id)"
            class="btn btn-secondary !py-1 !px-3 !text-xs"
          >
            {{ t('adminUsers.table.view') }} </button>
              <button v-if="user.esta_activo" @click="handleToggleActive(user.id, false)" class="btn btn-secondary !py-1 !px-3 !text-xs !bg-yellow-600 hover:!bg-yellow-700">
                {{ t('adminUsers.actions.deactivate') }}
              </button>
              <button v-else @click="handleToggleActive(user.id, true)" class="btn btn-secondary !py-1 !px-3 !text-xs !bg-green-600 hover:!bg-green-700">
                {{ t('adminUsers.actions.activate') }}
              </button>
              
              <button class="btn btn-secondary !py-1 !px-3 !text-xs" @click="openManagementModal(user)">
                {{ t('adminUsers.table.manage') }}
              </button>

              
            </template>

          </div>
        </div>
      </div>
    </AdminCard>
    
    <AdminUserManagementModal 
      v-if="adminStore.isManagementModalOpen"
      :user="adminStore.userToManage"
      @close="adminStore.closeManagementModal"
    />
    <AdminUserDetailModal 
      v-if="adminStore.isDetailModalOpen"
      @close="adminStore.closeDetailModal"
    />
    
    <AdminUserManagementModal 
      v-if="adminStore.isManagementModalOpen"
      :user="adminStore.userToManage"
      @close="adminStore.closeManagementModal"
    />
  </div>

</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import AdminCard from '@/components/Dashboard/shared/AdminCard.vue'
import UserStatusBadge from '@/components/Dashboard/shared/UserStatusBadge.vue'
import AdminUserManagementModal from '@/components/Dashboard/sections/AdminUserManagementModal.vue' 
import AdminUserDetailModal from '@/components/Dashboard/sections/AdminUserDetailModal.vue'
const { t } = useI18n()
const adminStore = useAdminStore()

onMounted(() => {
  adminStore.fetchAllUsers()
})

// --- Lógica de Búsqueda y Filtro ---
const searchTerm = ref('')
const loadingUserId = ref(null)
const statusFilter = ref('all') // <-- Estado para las pestañas

// Helper para obtener la clave de estado (igual que en UserStatusBadge)
const getUserStatusKey = (user) => {
  if (user.esta_activo && user.aprobado_por_admin) return 'active';
  if (!user.esta_activo && user.aprobado_por_admin) return 'inactive';
  if (!user.aprobado_por_admin) return 'pending';
  return 'inactive'; // Fallback
}

const filteredUsers = computed(() => {
  if (!adminStore.userList) {
    return []
  }
  
  // 1. Aplicar filtro de ESTADO primero
  const statusFiltered = adminStore.userList.filter(user => {
    if (statusFilter.value === 'all') return true;
    return getUserStatusKey(user) === statusFilter.value;
  });

  // 2. Aplicar filtro de BÚSQUEDA (texto) después
  const query = searchTerm.value.toLowerCase().trim()
  if (!query) {
    return statusFiltered; // Devuelve la lista ya filtrada por estado
  }

  return statusFiltered.filter((user) => {
    const fullName = `${user.nombre} ${user.apellidos}`.toLowerCase()
    const email = (user.email || '').toLowerCase()
    const apodo = (user.apodo || '').toLowerCase()
    
    return fullName.includes(query) || email.includes(query) || apodo.includes(query)
  })
})

// Helper para clases de pestañas
const getTabClasses = (filterName) => {
  const isActive = statusFilter.value === filterName;
  let classes = [
    'py-2 px-3 sm:py-3 sm:px-4',
    'font-mono font-bold text-xs sm:text-sm',
    'uppercase tracking-wider transition-colors',
    'border-b-2 sm:border-b-4'
  ];
  if (isActive) {
    classes.push('border-brand-red', 'text-white');
  } else {
    classes.push('border-transparent', 'text-gray-500', 'hover:text-gray-300');
  }
  return classes;
};


// --- Lógica de Acciones ---
function openManagementModal(user) {
  adminStore.openManagementModal(user);
}

async function handleApprove(userId) {
  loadingUserId.value = userId
  try {
    await adminStore.approveUser(userId)
  } catch (error) {
    alert(t(error.message)) 
  } finally {
    loadingUserId.value = null
  }
}

async function handleReject(userId) {
  if (confirm(t('adminUsers.actions.confirmReject'))) {
    loadingUserId.value = userId
    try {
      await adminStore.rejectUser(userId)
    } catch (error) {
      alert(t(error.message))
    } finally {
      loadingUserId.value = null
    }
  }
}

async function handleToggleActive(userId, newStatus) {
  loadingUserId.value = userId
  try {
    await adminStore.setUserStatus(userId, newStatus)
  } catch (error) {
    alert(t(error.message))
  } finally {
    loadingUserId.value = null
  }
}
</script>