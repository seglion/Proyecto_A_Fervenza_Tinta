<template>
  <div class="flex flex-col gap-4">
    <h1 class="text-white text-5xl sm:text-6xl lg:text-7xl font-bold leading-tight tracking-tight font-antonio">
      {{t('landing.welcomeMessage')}}
    </h1>
    <p class="text-white text-base sm:text-lg font-normal leading-normal font-space">
      {{t('landing.subtitle')}}
    </p>
  </div>
</template>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Antonio:wght@700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&display=swap');

.font-antonio { font-family: 'Antonio', sans-serif; }
.font-space { font-family: 'Space Mono', monospace; }
</style>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
</script>