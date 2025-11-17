<template>
  <div>
    <label class="form-label">{{ label }}</label>
    
    <input 
      type="file" 
      ref="fileInput" 
      @change="handleFileChange" 
      accept="image/png, image/jpeg"
      class="hidden"
    />

    <div 
      class="w-full h-48 border-2 border-dashed border-gray-600 rounded-md 
             flex items-center justify-center text-center p-4
             relative hover:border-brand-red transition-colors"
    >
      <div v-if="isLoading" class="text-gray-400">
        <span class="material-symbols-outlined animate-spin text-red-600 text-4xl">
          progress_activity
        </span>
        <p>{{ t('imageUploader.loading') }}</p>
      </div>
      
      <div v-else-if="imageUrl" class="relative w-full h-full">
        <img :src="imageUrl" alt="Vista previa" class="w-full h-full object-contain rounded-md" />
        <button 
          type="button" 
          @click.stop="removeImage" 
          class="absolute -top-3 -right-3 bg-red-600 text-white rounded-full p-1 shadow-lg hover:scale-110 transition-transform"
        >
          <span class="material-symbols-outlined">delete</span>
        </button>
      </div>

      <button 
        v-else 
        type="button" 
        @click="triggerFileInput" 
        class="btn btn-secondary"
      >
        <span class="material-symbols-outlined">upload_file</span>
        <span>{{ t('imageUploader.button') }}</span>
      </button>
    </div>
    
    <p v-if="error" class="text-red-500 text-sm mt-2">{{ error }}</p>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  label: { type: String, required: true },
  modelValue: { type: String, default: '' } // Para v-model
})
const emit = defineEmits(['update:modelValue'])

const { t } = useI18n()
const fileInput = ref(null)
const isLoading = ref(false)
const error = ref(null)
const imageUrl = ref(props.modelValue)

// Lee las variables de entorno de Vite
const CLOUD_NAME = import.meta.env.VITE_CLOUDINARY_CLOUD_NAME
const UPLOAD_PRESET = import.meta.env.VITE_CLOUDINARY_UPLOAD_PRESET
const UPLOAD_URL = `https://api.cloudinary.com/v1_1/${CLOUD_NAME}/image/upload`
console.log('Cloudinary Config:', { CLOUD_NAME, UPLOAD_PRESET })
// Sincroniza el v-model si cambia desde el padre
watch(() => props.modelValue, (newUrl) => {
  imageUrl.value = newUrl
})

function triggerFileInput() {
  error.value = null
  fileInput.value.click()
}

function removeImage() {
  imageUrl.value = ''
  emit('update:modelValue', '') // Emite la URL vacía
  fileInput.value.value = null // Resetea el input
}

async function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return
  
  isLoading.value = true
  error.value = null
  const formData = new FormData()
  formData.append('file', file)
  formData.append('upload_preset', UPLOAD_PRESET)

  try {
    const response = await fetch(UPLOAD_URL, {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
        console.error('Error de Cloudinary:', data.error.message)
      const errData = await response.json()
      throw new Error(errData.error.message || 'Error al subir la imagen.')
    }
    
    const data = await response.json()
    const secureUrl = data.secure_url
    
    imageUrl.value = secureUrl
    emit('update:modelValue', secureUrl) // ¡Emite la nueva URL!
    
  } catch (err) {
    error.value = err.message
  } finally {
    isLoading.value = false
  }
}
</script>