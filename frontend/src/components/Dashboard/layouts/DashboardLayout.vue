<template>
<div class="flex min-h-screen bg-background-dark text-white font-mono">
    
    <MobileMenuButton 
      :isOpen="isMobileSidebarOpen"
      @toggle="isMobileSidebarOpen = !isMobileSidebarOpen" 
    />

    <div 
      v-if="isMobileSidebarOpen"
      @click="isMobileSidebarOpen = false"
      class="fixed inset-0 z-10 bg-black/60 sm:hidden"
    ></div>

    <DashboardSidebar
      :user="authStore.user" 
      :isOpen="isMobileSidebarOpen"
    />

    <main class="flex-1 bg-black p-6 sm:p-8 overflow-x-auto">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import MobileMenuButton from '../shared/MobileMenuButton.vue'
import DashboardSidebar from '../sections/DashboardSidebar.vue'




const authStore = useAuthStore()
const isMobileSidebarOpen = ref(false)
</script>