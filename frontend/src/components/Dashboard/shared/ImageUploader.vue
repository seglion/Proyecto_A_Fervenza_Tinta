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
const API_BASE = import.meta.env.VITE_API_BASE_URL

const props = defineProps({
  label: { type: String, required: true },
  modelValue: { type: String, default: '' }
})
const emit = defineEmits(['update:modelValue'])

const { t } = useI18n()
const fileInput = ref(null)
const isLoading = ref(false)
const error = ref(null)
const imageUrl = ref(props.modelValue)

watch(() => props.modelValue, (newUrl) => {
  imageUrl.value = newUrl
})

function triggerFileInput() {
  error.value = null
  fileInput.value.click()
}

function removeImage() {
  imageUrl.value = ''
  emit('update:modelValue', '')
  fileInput.value.value = null
}

async function handleFileChange(event) {
  const file = event.target.files[0]
  if (!file) return

  isLoading.value = true
  error.value = null

  const formData = new FormData()
  formData.append('file', file)

  try {
    const token = localStorage.getItem('jwt_token')
    const response = await fetch(`${API_BASE}/files/upload-image`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData,
    })
    if (!response.ok) {
      const errData = await response.json()
      throw new Error(errData.detail ?? 'Error al subir la imagen.')
    }
    const data = await response.json()
    imageUrl.value = data.url
    emit('update:modelValue', data.url)
  } catch (err) {
    error.value = err.response?.data?.detail ?? 'Error al subir la imagen.'
  } finally {
    isLoading.value = false
  }
}
</script>
