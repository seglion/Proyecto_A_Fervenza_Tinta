<template>
  <li>
    <RouterLink
      :to="to"
      class="
        flex items-center gap-2 rounded-md px-4 py-1 
        text-gray-400 
        transition-colors 
        hover:bg-red-700 hover:text-white
      "
      active-class="bg-red-900 text-white" 
    >
      <span class="material-symbols-outlined" style="min-width: 24px;">
        {{ icon }}
      </span>
      
      <span>
        {{ label }}
      </span>
    </RouterLink>
  </li>
</template>

<script setup>
import { RouterLink } from 'vue-router';

defineProps({
  to: { type: String, required: true },
  label: { type: String, required: true },
  icon: { type: String, required: true },
});
</script>

<style scoped>
.material-symbols-outlined {
  font-size: 24px;
}
</style>