<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-2xl p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ title }}
        </h2>
        <button @click="adminStore.closePrendaModal" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>
<div class="max-h-[70vh] overflow-y-auto pr-2">
      <form @submit="onSubmit" class="space-y-4 max-h-[70vh] overflow-y-auto pr-2">
        
        <AuthInput
          name="nombre"
          type="text"
          :label="t('adminPrendas.form.name')"
          placeholder="Ej: Camiseta Técnica"
        />
        
        <AuthInput
          name="descripcion"
          type="text"
          :label="t('adminPrendas.form.description')"
          placeholder="Ej: Camiseta transpirable..."
        />
        
        <AuthInput
          name="precio"
          type="number"
          :label="t('adminPrendas.table.price')"
          placeholder="Ej: 25.00"
          step="0.01"
        />
        
        <Field name="imagen_url" v-slot="{ field, value }">
          <ImageUploader 
            :label="t('adminPrendas.form.image')"
            :modelValue="value"
            @update:modelValue="field.onChange"
          />
        </Field>
        <p v-if="adminStore.errorPrendaModal" class="text-red-500 text-sm text-center">
            {{ t(adminStore.errorPrendaModal) }}
          </p>

          <div class="flex justify-end pt-4">
            <button 
              type="submit" 
              :disabled="adminStore.isLoadingPrendaModal"
              class="btn btn-primary w-full sm:w-auto"
            >
              <span v-if="adminStore.isLoadingPrendaModal">{{ t('resetPassword.sending') }}</span>
              <span v-else>{{ isEditing ? t('adminPrendas.modal.submitEdit') : t('adminPrendas.modal.submitCreate') }}</span>
            </button>
          </div>
      </form>
        <div v-if="isEditing" class="mt-6 pt-4 border-t border-gray-700">
          <h3 class="font-bold text-lg text-red-600 mb-4">{{ t('adminPrendas.variants.title') }}</h3>
          
          <div class="space-y-2 mb-4">
            <div 
              v-for="variante in prenda.variantes" 
              :key="variante.id"
              class="flex justify-between items-center p-2 bg-gray-900 rounded-md"
            >
              <span class="text-white">{{ t(`adminPrendas.enums.GeneroPrenda.${variante.genero}`) }} / {{ t(`adminPrendas.enums.TallaPrenda.${variante.talla}`) }}</span>
              <button 
                @click="handleDeleteVariante(variante.id)" 
                class="text-red-500 hover:text-red-400"
              >
                <span class="material-symbols-outlined">delete</span>
              </button>
            </div>
            <p v-if="prenda.variantes.length === 0" class="text-gray-500 text-sm">
              {{ t('adminPrendas.variants.noVariants') }}
            </p>
          </div>

          <form @submit.prevent="handleAddVariante" class="flex flex-col sm:flex-row gap-4">
            <select v-model="newVariante.genero" class="input" style="background-color: #000; color: white;">
              <option disabled value="">{{ t('adminPrendas.variants.selectGender') }}</option>
              <option v-for="g in generos" :key="g" :value="g" style="background-color: #000;">
                {{ t(`adminPrendas.enums.GeneroPrenda.${g}`) }}
              </option>
            </select>
            
            <select v-model="newVariante.talla" class="input" style="background-color: #000; color: white;">
              <option disabled value="">{{ t('adminPrendas.variants.selectSize') }}</option>
              <option v-for="talla in tallas" :key="talla" :value="talla" style="background-color: #000;">
                {{ t(`adminPrendas.enums.TallaPrenda.${talla}`) }}
              </option>
            </select>
            
            <button type="submit" class="btn btn-secondary w-full sm:w-auto">
              {{ t('adminPrendas.variants.add') }}
            </button>
          </form>
        </div>

      </div> 
    </div>
  </div>
</template>

<script setup>
import { computed,ref } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import { useForm, Field } from 'vee-validate' 
import * as yup from 'yup'
import AuthInput from '@/components/Auth/AuthInput.vue'
import ImageUploader from '@/components/Dashboard/shared/ImageUploader.vue'
import { GeneroPrenda, TallaPrenda } from '@/constants/prendas'
const { t } = useI18n()
const adminStore = useAdminStore()

const prenda = computed(() => adminStore.prendaToEdit) 
const isEditing = computed(() => !!prenda.value)

const title = computed(() => isEditing.value ? t('adminPrendas.modal.editTitle') : t('adminPrendas.modal.createTitle'))

// --- Lógica del Formulario (VeeValidate) ---

const schema = yup.object({
  nombre: yup.string().required(t('validation.nameRequired')),
  descripcion: yup.string().required(t('validation.descriptionRequired')),
  precio: yup.number().min(0).required(t('validation.amountRequired')),
  imagen_url: yup.string().url(t('validation.urlInvalid')).required(t('validation.imageRequired')),
})

const { handleSubmit } = useForm({
  validationSchema: schema,
  initialValues: {
    nombre: prenda.value?.nombre || '',
    descripcion: prenda.value?.descripcion || '',
    precio: prenda.value?.precio || 0.00,
    imagen_url: prenda.value?.imagen_url || '',
  }
})

// --- Lógica de Submit ---
const onSubmit = handleSubmit(async (values) => {
  try {
    if (isEditing.value) {
      await adminStore.updatePrenda(prenda.value.id, values)
    } else {
      await adminStore.createPrenda(values)
    }
    adminStore.closePrendaModal() // Cierra el modal si tiene éxito
  // eslint-disable-next-line no-unused-vars
  } catch (error) {
    // El error se muestra en el template (adminStore.errorPrendaModal)
  }
})
const generos = Object.values(GeneroPrenda)
const tallas = Object.values(TallaPrenda)

const newVariante = ref({
  genero: '',
  talla: ''
})

async function handleAddVariante() {
  if (!newVariante.value.genero || !newVariante.value.talla) {
    alert('Por favor, selecciona género y talla.')
    return
  }
  
  try {
    await adminStore.addPrendaVariante(prenda.value.id, newVariante.value)
    // Limpia el formulario de variantes
    newVariante.value = { genero: '', talla: '' }
  // eslint-disable-next-line no-unused-vars
  } catch (error) {
    // El error se muestra en el template (adminStore.errorPrendaModal)
  }
}

async function handleDeleteVariante(varianteId) {
  if (confirm(t('adminPrendas.variants.confirmDelete'))) {
    try {
      await adminStore.deletePrendaVariante(prenda.value.id, varianteId)
    // eslint-disable-next-line no-unused-vars
    } catch (error) {
      // El error se muestra en el template
    }
  }
}
</script>