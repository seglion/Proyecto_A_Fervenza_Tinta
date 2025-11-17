<template>
  <RouterLink 
    :to="to" 
    class="text-white text-base font-normal leading-normal hover:text-red-600 transition-colors font-space"
  >
    {{ label }}
  </RouterLink>
</template>

<script setup>
import { RouterLink } from 'vue-router'

defineProps({ 
  label: String,
  to: { 
    type: [String, Object],
    required: true
  } 
})
</script>

<style scoped>
.font-space { font-family: 'Space Mono', monospace; }
</style>