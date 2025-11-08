<template>
  <a href="#" class="text-white text-base font-normal leading-normal hover:text-red-600 transition-colors font-space">
    {{ label }}
  </a>
</template>

<script setup>
defineProps({ label: String })
</script>

<style scoped>
.font-space { font-family: 'Space Mono', monospace; }
</style>
