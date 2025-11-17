<template>
  <div class="flex justify-between items-center py-3 border-b border-gray-800">
    <span class="text-gray-400 text-sm sm:text-base">{{ label }}</span>
    <span class="font-bold text-2xl sm:text-3xl" :class="colorClass">{{ value }}</span>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  colorClass: {
    type: String,
    default: 'text-white' 
  }
})
</script>