<template>
  <div class="bg-black border-2 border-red-600 overflow-hidden">
    <h3 class="font-display text-2xl font-bold uppercase tracking-wider text-white p-4 sm:p-6">
      <slot name="title" />
    </h3>
    
    <div class="p-4 sm:p-6 border-t border-gray-800">
      <slot />
    </div>
  </div>
</template>