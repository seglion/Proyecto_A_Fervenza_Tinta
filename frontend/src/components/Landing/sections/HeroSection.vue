<template>
  <section class="relative flex items-center justify-center flex-1">
    <!-- Red overlay -->
    <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>
    <div class="absolute inset-0 z-10 bg-red-600/70"></div>

    <!-- Content -->
    <div class="relative z-20 flex w-full h-full p-4 lg:p-8 items-end justify-end">
      <div class="bg-black/80 p-6 sm:p-10 lg:p-12 text-white flex flex-col gap-6 w-full max-w-full sm:max-w-[70%] lg:max-w-[60%] xl:max-w-[50%] h-auto min-h-[300px] justify-center items-start text-left">
        <HeadingBlock />
        <ActionButtons />
      </div>
    </div>
  </section>
</template>

<script setup>
import HeadingBlock from './HeadingBlock.vue'
import ActionButtons from './ActionButtons.vue'
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'
</script>
