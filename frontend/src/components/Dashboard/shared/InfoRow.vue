<template>
  <div class="py-2">
    <label class="block text-sm font-medium text-gray-400 font-space">
      {{ label }}
    </label>
    <p class="text-base text-white mt-1">
      {{ value || '-' }}
    </p>
  </div>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  value: { type: String, default: '' }
})
</script>