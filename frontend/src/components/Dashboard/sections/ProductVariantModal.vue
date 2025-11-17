<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-lg p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ prenda.nombre }}
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <form @submit.prevent="handleAddToCart" class="space-y-4">
        
        <p class="text-gray-400">{{ prenda.descripcion }}</p>
        <p class="font-mono text-2xl text-white">€{{ prenda.precio }}</p>
        
        <hr class="border-gray-700">

        <div>
          <label for="genero" class="form-label">{{ t('adminPrendas.enums.GeneroPrenda.title') }}</label>
          <select 
            id="genero" 
            v-model="selectedGenero" 
            class="input"
            style="background-color: #000; color: white;"
          >
            <option disabled value="">{{ t('adminPrendas.variants.selectGender') }}</option>
            <option v-for="g in generosDisponibles" :key="g" :value="g" style="background-color: #000;">
              {{ t(`adminPrendas.enums.GeneroPrenda.${g}`) }}
            </option>
          </select>
        </div>

        <div>
          <label for="talla" class="form-label">{{ t('adminPrendas.enums.TallaPrenda.title') }}</label>
          <select 
            id="talla" 
            v-model="selectedTalla" 
            :disabled="!selectedGenero"
            class="input"
            style="background-color: #000; color: white;"
          >
            <option disabled value="">{{ t('adminPrendas.variants.selectSize') }}</option>
            <option v-for="talla in tallasDisponibles" :key="talla" :value="talla" style="background-color: #000;">
              {{ t(`adminPrendas.enums.TallaPrenda.${talla}`) }}
            </option>
          </select>
        </div>
        
        <div>
          <label for="cantidad" class="form-label">{{ t('merchandise.list.quantity') }}</label>
          <input 
            id="cantidad"
            type="number"
            v-model.number="cantidad"
            min="1"
            max="10"
            class="input"
          />
        </div>

        <p v-if="error" class="text-red-500 text-sm text-center">
          {{ t(error) }}
        </p>

        <div class="flex justify-end pt-4">
          <button 
            type="submit" 
            :disabled="!varianteSeleccionada"
            class="btn btn-primary w-full sm:w-auto"
          >
            {{ t('merchandise.list.addToCart') }}
          </button>
        </div>
        
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { usePedidosStore } from '@/stores/pedidosStore'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  prenda: { type: Object, required: true }
})
const emit = defineEmits(['close'])

const { t } = useI18n()
const pedidosStore = usePedidosStore()
const error = ref(null)
const cantidad = ref(1)

// --- Lógica de Variantes ---
const selectedGenero = ref('')
const selectedTalla = ref('')

// 1. Obtiene géneros únicos de las variantes (ej. ["HOMBRE", "MUJER"])
const generosDisponibles = computed(() => {
  const generos = props.prenda.variantes.map(v => v.genero)
  return [...new Set(generos)] // Elimina duplicados
})

// 2. Obtiene tallas basadas en el género seleccionado
const tallasDisponibles = computed(() => {
  if (!selectedGenero.value) return []
  const tallas = props.prenda.variantes
    .filter(v => v.genero === selectedGenero.value)
    .map(v => v.talla)
  return [...new Set(tallas)]
})

// 3. Resetea la talla si el género cambia
watch(selectedGenero, () => {
  selectedTalla.value = ''
})

// 4. Encuentra el ID de la variante seleccionada
const varianteSeleccionada = computed(() => {
  if (!selectedGenero.value || !selectedTalla.value) return null
  
  return props.prenda.variantes.find(v => 
    v.genero === selectedGenero.value && v.talla === selectedTalla.value
  )
})

// 5. Acción de Añadir al Carrito
async function handleAddToCart() {
  if (!varianteSeleccionada.value) return
  error.value = null

  try {
    // Llama a la acción del store (POST /pedidos/borrador/lineas)
    await pedidosStore.addPrendaToCart(
      props.prenda.id, 
      varianteSeleccionada.value.id, 
      cantidad.value
    )
    emit('close') // Cierra el modal si tiene éxito
  } catch (err) {
    error.value = err.message
  }
}
</script>