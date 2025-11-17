<template>
  <aside
    class="
      text-white
      flex flex-col flex-shrink-0
      fixed sm:static z-20
      transition-transform duration-300 ease-in-out
      bg-black border-r-4 border-red-600
      
      w-full sm:w-64 
      
      h-screen 
    "
    :class="isOpen ? 'translate-x-0' : '-translate-x-full sm:translate-x-0'"
  >
    <UserProfileHeader :user="user" />

    <SidebarNav />

    <div class="p-4 border-t border-gray-800">
      <LogoutButton />
    </div>
  </aside>
</template>

<script setup>
// ... (tu script no cambia)
import UserProfileHeader from './UserProfileHeader.vue'
import SidebarNav from './SidebarNav.vue'
import LogoutButton from '../shared/LogoutButton.vue'

defineProps({
  user: {
    type: Object,
    default: null,
  },
  isOpen: {
    type: Boolean,
    default: false,
  },
});
</script>