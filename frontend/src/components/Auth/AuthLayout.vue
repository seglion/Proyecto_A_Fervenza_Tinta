<template>
  <div class="relative flex min-h-screen w-full flex-col bg-black text-white font-mono">
    <div class="absolute inset-0 bg-black/70"></div>

    <main class="relative z-10 flex flex-1 flex-col items-center justify-center p-4">
      <div
        class="w-full max-w-md bg-black/80 p-6 sm:p-8 md:p-10 border border-red-600"
      >
        <slot />
      </div>
    </main>
  </div>
</template>

<script setup>

</script>
