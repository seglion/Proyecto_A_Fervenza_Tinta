<template>
  <div class="overflow-hidden bg-black border-2 border-red-600 rounded-md">
    <div class="bg-red-600 p-4">
      <h3 class="font-display text-xl font-bold uppercase tracking-wider text-white">
        {{ title }}
      </h3>
    </div>

    <div class="p-4">
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
});
</script>