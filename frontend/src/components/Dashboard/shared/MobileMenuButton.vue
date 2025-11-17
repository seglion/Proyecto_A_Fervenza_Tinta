<template>
  <button
    @click="$emit('toggle')"
    class="
      fixed bottom-6 right-6 z-30
      flex items-center justify-center w-14 h-14
      bg-brand-red text-white rounded-full shadow-lg
      transition-transform duration-200 ease-in-out
      hover:scale-110
      sm:hidden
    "
  >
    <span v-if="!isOpen" class="material-symbols-outlined text-3xl">menu</span>
    <span v-else class="material-symbols-outlined text-3xl">close</span>
  </button>
</template>

<script setup>
defineProps({
  isOpen: {
    type: Boolean,
    default: false,
  },
});

defineEmits(['toggle']);
</script>