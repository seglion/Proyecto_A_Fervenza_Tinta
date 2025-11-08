<template>
  <footer class="flex flex-col gap-6 px-5 py-8 text-center bg-black border-t-2 border-red-600">
    <!-- Links -->
    <div class="flex flex-wrap items-center justify-center gap-6 sm:justify-around">
      <NavLink :label="t('footer.links.about')" />
      <NavLink :label="t('footer.links.contact')" />
      <NavLink :label="t('footer.links.privacy')" />
      <NavLink :label="t('footer.links.terms')" />
    </div>

    <!-- Socials -->
    <div class="flex justify-center gap-6">
      <SocialIcon />

    </div>

    <p class="text-white text-sm font-normal leading-normal font-space">
      © 2025 A Fervenza Tinta. TODOS LOS DERECHOS RESERVADOS.
    </p>
  </footer>
</template>

<script setup>
import NavLink from '../shared/NavLink.vue'
import SocialIcon from '../shared/SocialIcon.vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()






</script>

<style scoped>
.font-space { font-family: 'Space Mono', monospace; }
</style>
