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
          placeholder="Ej: 2026-2027"
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
        
        <h3 class="font-bold text-lg text-red-600">{{ t('adminSeasons.modal.feeTypesTitle') }}</h3>
        
        <div class="space-y-4">
          <div 
            v-for="(field, idx) in tipoCuotaFields" 
            :key="field.key" 
            class="grid grid-cols-2 gap-4 p-3 border border-gray-800 rounded-md"
          >
            <AuthInput
              :name="`tipos_cuota[${idx}].nombre`"
              type="text"
              :label="`Tipo de Cuota ${idx + 1}`"
              :modelValue="field.value.nombre"
              disabled
            />
            
            <AuthInput
              :name="`tipos_cuota[${idx}].importe`"
              type="number"
              :label="`${field.value.nombre === 'ALTA' ? t('dashboard.feeTypes.ALTA') : t('dashboard.feeTypes.SOCIO')}`"
              placeholder="Ej: 25.00"
              step="0.01"
            />
          </div>
        </div>

        <p v-if="adminStore.errorSeason" class="text-red-500 text-sm text-center">
          {{ t(adminStore.errorSeason) }}
        </p>

        <div class="flex justify-end pt-4">
          <button 
            type="submit" 
            :disabled="adminStore.isUpdatingSeason"
            class="btn btn-primary w-full sm:w-auto"
          >
            <span v-if="adminStore.isUpdatingSeason">{{ t('resetPassword.sending') }}</span>
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
import { useForm, useFieldArray } from 'vee-validate' 
import * as yup from 'yup'
import AuthInput from '@/components/Auth/AuthInput.vue'
import { NombreTipoCuota } from '@/constants/cuotas' 

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
const title = computed(() => isEditing.value ? t('adminSeasons.modal.editTitle') : t('adminSeasons.modal.createTitle'))

// --- Lógica del Formulario (VeeValidate) ---

const validationSchema = yup.object({
  nombre_temporada: yup.string().required(t('validation.nameRequired')),
  fecha_inicio: yup.date().required(t('validation.dateRequired')),
  fecha_fin: yup.date().required(t('validation.dateRequired'))
    .min(yup.ref('fecha_inicio'), t('validation.dateMin')), // Fecha fin > Fecha inicio
  tipos_cuota: yup.array().of(
    yup.object({
      nombre: yup.string().required(),
      importe: yup.number().min(0).required(t('validation.amountRequired'))
    })
  ).min(2, 'Debe haber 2 tipos de cuota') // Forzamos ALTA y SOCIO
})

// Función para formatear fechas (YYYY-MM-DD)
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
    tipos_cuota: props.seasonData?.tipos_cuota || [
      { nombre: NombreTipoCuota.ALTA, importe: 25.00 },
      { nombre: NombreTipoCuota.SOCIO, importe: 25.00 }
    ]
  }
})

// Lógica de FieldArray para los tipos de cuota
const { fields: tipoCuotaFields } = useFieldArray('tipos_cuota')

// --- Lógica de Submit ---
const onSubmit = handleSubmit(async (values) => {
  try {
    if (isEditing.value) {
      // Para EDITAR, necesitamos fusionar los IDs originales
      const updateDTO = {
        ...values,
        tipos_cuota: values.tipos_cuota.map((tc, index) => ({
          // Coge el ID y fecha_creacion originales
          ...props.seasonData.tipos_cuota[index],
          // Sobrescribe con los valores editados
          ...tc 
        }))
      }
      await adminStore.updateSeason(props.seasonData.id, updateDTO)
    } else {
      // Para CREAR, los 'values' coinciden con el 'CrearTemporadaDTO'
      await adminStore.createSeason(values)
    }
    emit('close') // Cierra el modal si tiene éxito
  // eslint-disable-next-line no-unused-vars
  } catch (error) {
    // El error se muestra en el template (adminStore.errorSeason)
  }
})
</script>