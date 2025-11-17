<template>
  <div>
    <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
      {{ t('dashboard.admin.view.title') }}
    </h1>
    <p class="text-gray-400 mb-8 -mt-6">
      {{ t('dashboard.admin.view.subtitle', { name: authStore.user?.apodo || 'Admin' }) }}
    </p>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">

      <div class="flex flex-col gap-8">
<AdminCard>
          <template #title>{{ t('dashboard.admin.stats.title') }}</template>
          
          <div v-if="adminStore.isLoadingUsers" class="text-gray-400">
            {{ t('dashboard.view.feeLoading') }}
          </div>

          <div v-else-if="adminStore.errorUsers" class="text-red-500">
            {{ t(adminStore.errorUsers) }}
          </div>
          
          <div v-else>
            <AdminStat 
              :label="t('dashboard.admin.stats.activeMembers')" 
              :value="adminStore.getActiveMembers" />
            <AdminStat 
              :label="t('dashboard.admin.stats.newMembers')" 
              :value="adminStore.getNewMembers30d" colorClass="text-red-600" 
            />
            <AdminStat 
              :label="t('dashboard.admin.stats.totalUsers')" 
              :value="adminStore.getTotalUsers" />
          </div>
        </AdminCard>
      </div>

      <div class="flex flex-col gap-8">
        <AdminCard>
          <template #title>{{ t('dashboard.admin.pendingOrders.title') }}</template>
          
          <div class="flex flex-col gap-4">
            <div class="grid grid-cols-3 gap-2 text-sm sm:text-base">
              <span class="text-gray-400">#AFT-8341</span>
              <span>John Doe</span>
              <span class="text-right font-bold">€45.00</span>
            </div>
            <div class="grid grid-cols-3 gap-2 text-sm sm:text-base">
              <span class="text-gray-400">#AFT-8339</span>
              <span>Jane Smith</span>
              <span class="text-right font-bold">€22.50</span>
            </div>
          </div>
          <div class="text-right mt-6">
            <RouterLink to="/dashboard/admin/orders" class="font-bold text-red-600 hover:text-red-500">
              {{ t('dashboard.admin.view.viewAll') }} &rarr;
            </RouterLink>
          </div>
        </AdminCard>
      </div>

      <div class="lg:col-span-2">
        <AdminCard>
          <template #title>{{ t('dashboard.admin.recentPayments.title') }}</template>
          
          <div v-if="adminStore.isLoadingPayments" class="text-gray-400 p-4 text-center">
             {{ t('dashboard.view.feeLoading') }}
          </div>
          
          <div v-else-if="adminStore.errorPayments" class="text-red-500 p-4 text-center">
             {{ t(adminStore.errorPayments) }}
          </div>

          <div v-else class="flex flex-col">
            <div class="hidden sm:grid grid-cols-5 gap-4 text-xs text-gray-500 uppercase pb-2 border-b border-gray-800">
              <span>{{ t('dashboard.admin.recentPayments.member') }}</span>
              <span>{{ t('dashboard.admin.recentPayments.plan') }}</span>
              <span>{{ t('dashboard.admin.recentPayments.date') }}</span>
              <span>{{ t('dashboard.admin.recentPayments.status') }}</span>
              <span class="text-right">{{ t('dashboard.admin.recentPayments.amount') }}</span>
            </div>
            
            <div v-if="adminStore.recentPayments.length === 0" class="text-center text-gray-400 py-6">
              {{ t('adminUsers.search.noResults') }} </div>

            <div 
              v-for="pago in adminStore.recentPayments" 
              :key="pago.id"
              class="grid grid-cols-2 sm:grid-cols-5 gap-y-4 gap-x-2 sm:gap-4 py-3 border-b border-gray-800 items-center"
            >
              <span class="sm:hidden col-span-2 text-xs text-gray-500 uppercase">{{ t('dashboard.admin.recentPayments.member') }}</span>
              <span class="col-span-2 sm:col-span-1 font-bold">{{ pago.usuario_nombre }} {{ pago.usuario_apellidos }}</span>
              
              <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('dashboard.admin.recentPayments.plan') }}</span>
              <span class="capitalize">{{ t(`dashboard.feeTypes.${pago.tipo_cuota_nombre}`) }}</span>
              
              <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('dashboard.admin.recentPayments.date') }}</span>
              <span>{{ d(new Date(pago.fecha_pago), 'short') }}</span>
              
              <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('dashboard.admin.recentPayments.status') }}</span>
              <span><CuotaStatusBadge :status="pago.estado_pago" /></span>
              
              <span class="sm:hidden text-xs text-gray-500 uppercase">{{ t('dashboard.admin.recentPayments.amount') }}</span>
              <span class="text-right font-bold">€{{ pago.importe_pagado }}</span>
            </div>
          </div>

          <div class="text-right mt-6">
            <RouterLink to="/dashboard/admin/payments" class="font-bold text-red-600 hover:text-red-500">
              {{ t('dashboard.admin.view.viewAll') }} &rarr;
            </RouterLink>
          </div>

        </AdminCard>
      </div>

    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useAdminStore } from '@/stores/adminStore' // <-- Importa el nuevo store
import { useI18n } from 'vue-i18n'
import AdminCard from '@/components/Dashboard/shared/AdminCard.vue'
import AdminStat from '@/components/Dashboard/shared/AdminStat.vue'
import CuotaStatusBadge from '@/components/Dashboard/shared/CuotaStatusBadge.vue' // Reutilizamos el badge

const { t,d } = useI18n()
const authStore = useAuthStore()
const adminStore = useAdminStore()
onMounted(() => {
  adminStore.fetchAllUsers()
  adminStore.fetchRecentPayments()
})

</script>