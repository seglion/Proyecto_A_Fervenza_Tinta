<template>
  <div class="bg-black border-2 border-red-600 overflow-hidden rounded-lg group flex flex-col">
    
    <div class="w-full h-80 flex items-center justify-center p-4 bg-gray-900 overflow-hidden"> 
      <img 
        :src="prenda.imagen_url || 'https://via.placeholder.com/400'" 
        :alt="prenda.nombre"
        class="
          w-auto h-auto 
          max-w-full max-h-full 
          object-contain 
          transition-transform duration-300 group-hover:scale-105
        "
      />
    </div>
    
    <div class="p-4 flex-grow">
      <h3 class="font-display text-2xl font-bold uppercase tracking-wider text-white">
        {{ prenda.nombre }}
      </h3>
      <p class="font-mono text-lg text-gray-300 mt-1">€{{ prenda.precio }}</p>
    </div>
    
    <button 
      @click="$emit('select')" 
      class="btn btn-primary w-full !rounded-none"
    >
      {{ t('merchandise.list.selectVariant') }}
    </button>
  </div>
</template>

<script setup>
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps({
  prenda: {
    type: Object,
    required: true
  }
})

defineEmits(['select'])
</script>