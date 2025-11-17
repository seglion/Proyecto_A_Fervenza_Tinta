<template>
  <footer class="flex flex-col gap-4 sm:gap-6 px-5 py-8 text-center bg-black border-t-2 border-red-600">
    
    <div class="flex flex-wrap items-center justify-center gap-4 sm:gap-6 text-sm sm:text-base">
      <NavLink :label="t('footer.links.about')" :to="{ name: 'about' }" />
      <NavLink :label="t('footer.links.contact')" :to="{ name: 'contact' }" />
      <NavLink :label="t('footer.links.privacy')" :to="{ name: 'privacy' }" />
      <NavLink :label="t('footer.links.terms')" :to="{ name: 'terms' }" />
    </div>

    <div class="flex justify-center gap-4 sm:gap-6">
      <SocialIcon />
      </div>

    <p class="text-white text-xs sm:text-sm font-normal leading-normal font-space">
      © {{ new Date().getFullYear() }} A Fervenza Tinta. {{ t('footer.copyright') }} . 
    </p>
    <p class="text-white text-xs sm:text-sm font-normal leading-normal font-space">Una Web desarrollada por <a href="https://www.linkedin.com/in/miguel-angel-vigo-baz-aa578b47/">Miguel Angel Vigo Baz</a></p>
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