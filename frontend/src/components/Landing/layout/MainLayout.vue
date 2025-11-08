<template>
  <div class="relative flex min-h-screen flex-col bg-stone-950 overflow-x-hidden">
    <main class="flex-1 flex flex-col">
      <slot />
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Footer from './FooterLayout.vue'
</script>