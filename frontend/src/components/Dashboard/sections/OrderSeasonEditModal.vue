<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    
    <div class="bg-black border-2 border-red-600 rounded-lg w-full max-w-2xl p-6 z-50">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4">
        <h2 class="font-display text-2xl uppercase text-white">
          {{ title }}
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <form @submit="onSubmit" class="space-y-4 max-h-[70vh] overflow-y-auto pr-2">
        
        <AuthInput
          name="nombre_temporada"
          type="text"
          :label="t('adminSeasons.table.name')"
          placeholder="Ej: Temporada Pedido 2026-2027"
        />
        
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <AuthInput
            name="fecha_inicio"
            type="date"
            :label="t('adminSeasons.table.startDate')"
          />
          <AuthInput
            name="fecha_fin"
            type="date"
            :label="t('adminSeasons.table.endDate')"
          />
        </div>

        <hr class="border-gray-700">

        <Field name="esta_activa" v-slot="{ field, value }">
          <label class="flex items-center gap-3 p-3 border border-gray-800 rounded-md cursor-pointer hover:border-gray-600">
            <input 
              type="checkbox"
              v-bind="field"
              :checked="value"
              class="h-5 w-5 rounded bg-gray-700 text-brand-red focus:ring-brand-red"
            />
            <span class="font-bold text-white">{{ t('adminOrderSeasons.form.isActive') }}</span>
          </label>
        </Field>
        
        <p v-if="adminStore.errorOrderSeason" class="text-red-500 text-sm text-center">
          {{ t(adminStore.errorOrderSeason) }}
        </p>

        <div class="flex justify-end pt-4">
          <button 
            type="submit" 
            :disabled="adminStore.isUpdatingOrderSeason"
            class="btn btn-primary w-full sm:w-auto"
          >
            <span v-if="adminStore.isUpdatingOrderSeason">{{ t('resetPassword.sending') }}</span>
            <span v-else>{{ isEditing ? t('adminSeasons.modal.submitEdit') : t('adminSeasons.modal.submitCreate') }}</span>
          </button>
        </div>
        
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { useI18n } from 'vue-i18n'
import { useForm, Field } from 'vee-validate' 
import * as yup from 'yup'
import AuthInput from '@/components/Auth/AuthInput.vue'

const props = defineProps({
  seasonData: { 
    type: Object,
    default: null
  }
})
const emit = defineEmits(['close'])

const { t } = useI18n()
const adminStore = useAdminStore()

const isEditing = computed(() => !!props.seasonData)
const title = computed(() => isEditing.value ? t('adminOrderSeasons.modal.editTitle') : t('adminSeasons.modal.createTitle'))


const validationSchema = yup.object({
  nombre_temporada: yup.string().required(t('validation.nameRequired')),
  fecha_inicio: yup.date().required(t('validation.dateRequired')),
  fecha_fin: yup.date().required(t('validation.dateRequired'))
    .min(yup.ref('fecha_inicio'), t('validation.dateMin')),
  esta_activa: yup.boolean() // El checkbox
})

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toISOString().split('T')[0]
}

const { handleSubmit } = useForm({
  validationSchema: validationSchema,
  initialValues: {
    nombre_temporada: props.seasonData?.nombre_temporada || '',
    fecha_inicio: formatDate(props.seasonData?.fecha_inicio),
    fecha_fin: formatDate(props.seasonData?.fecha_fin),
    esta_activa: props.seasonData?.esta_activa || false // Valor por defecto 'false' al crear
  }
})

const onSubmit = handleSubmit(async (values) => {
  try {
    if (isEditing.value) {
      await adminStore.updateOrderSeason(props.seasonData.id, values)
    } else {
      await adminStore.createOrderSeason(values)
    }
    emit('close') 
  // eslint-disable-next-line no-unused-vars
  } catch (error) {
    // El error se muestra en el template (adminStore.errorOrderSeason)
  }
})
</script>