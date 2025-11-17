<template>
  <nav class="grow p-3">
    
    <div v-if="authStore.user" class="px- pb-4 mb-4 border-b border-gray-800">
      <span class="text-xs font-semibold uppercase text-gray-500">
        {{ t('dashboard.nav.currentRole') }}:
      </span>
      <p class="font-bold text-sm text-brand-red mt-1">
        {{ t(`dashboard.roles.${authStore.user.rol}`) }} 
      </p>
    </div>
    <ul class="space-y-2">
      <li>
        <SidebarNavLink
          to="/dashboard"
          :label="t('dashboard.nav.home')"
          icon="dashboard"
        />
      </li>
      <li>
        <SidebarNavLink
          to="/dashboard/profile"
          :label="t('dashboard.nav.profile')"
          icon="person"
        />
      </li>
      <li>
        <SidebarNavLink
          to="/dashboard/payments"
          :label="t('dashboard.nav.paymentshistory')"
          icon="payments"
        />
      </li>
      <li>
        <SidebarNavLink
          to="/dashboard/store"
          :label="t('dashboard.nav.store')"
          icon="shopping_cart" 
        />
      </li>
      <li>
        <SidebarNavLink
          to="/dashboard/pedidos"
          :label="t('dashboard.nav.orders')"
          icon="inventory"
        />
      </li>

      <li v-if="authStore.user && authStore.user.rol === Role.ADMIN" class="pt-4 mt-4 border-t border-gray-800">
        <span class="px-4 text-xs font-semibold uppercase text-gray-500">
          {{ t('dashboard.nav.adminTitle') }}
        </span>
      </li>

      <li v-if="authStore.user && authStore.user.rol === Role.ADMIN">
        <SidebarNavLink
          to="/dashboard/admin" :label="t('dashboard.admin.nav.dashboard')"
          icon="admin_panel_settings"
        />
      </li>
      <li v-if="authStore.user && authStore.user.rol === Role.ADMIN">
        <SidebarNavLink
          to="/dashboard/admin/users"
          :label="t('dashboard.nav.adminUsers')"
          icon="manage_accounts"
        />
      </li>
           
      <li v-if="authStore.user && authStore.user.rol === Role.ADMIN">
        <SidebarNavLink
          to="/dashboard/admin/orders"
          :label="t('dashboard.admin.nav.orders')"
          icon="inventory"
        />
      </li>
      <li v-if="authStore.user && authStore.user.rol === Role.ADMIN">
        <SidebarNavLink
          to="/dashboard/admin/payments"
          :label="t('dashboard.admin.nav.payments')"
          icon="payments"
        />
      </li>
       <li v-if="authStore.user && authStore.user.rol === Role.ADMIN">
        <SidebarNavLink
          to="/dashboard/admin/seasons"
          :label="t('dashboard.admin.nav.seasons')"
          icon="settings" 
        />
      </li>
      <li v-if="authStore.user && authStore.user.rol === Role.ADMIN">
        <SidebarNavLink
          to="/dashboard/admin/clothes"
          :label="t('dashboard.admin.nav.prendas')"
          icon="shopping_bag" />
      </li>
      <li v-if="authStore.user && authStore.user.rol === Role.ADMIN" class="pl-4">
        <SidebarNavLink
          to="/dashboard/admin/orders/seasons"
          :label="t('dashboard.admin.nav.orderSeasons')"
          icon="settings" 
        />
      </li>

    </ul>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { Role } from '@/constants/roles';
import SidebarNavLink from '../shared/SidebarNavLink.vue';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const authStore = useAuthStore();
</script>