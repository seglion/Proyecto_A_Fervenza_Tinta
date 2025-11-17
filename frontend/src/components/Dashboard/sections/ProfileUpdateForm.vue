<template>
  <div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
      <AuthInput
        name="email"
        :label="t('register.emailLabel')"
        :modelValue="authStore.user?.email"
        disabled 
      />
      <AuthInput
        name="phone"
        :label="t('register.phoneLabel')"
        :modelValue="authStore.user?.numero_telefono"
        disabled
      />
    </div>

    <hr class="border-gray-700 my-6">

    <p v-if="mensajeExitoKey" class="text-green-400 text-sm mb-4 text-center">
      {{ t(mensajeExitoKey) }}
    </p>
    <p v-if="mensajeErrorKey" class="text-red-500 text-sm mb-4 text-center">
      {{ t(mensajeErrorKey, 'apiErrors.genericError') }}
    </p>

    <form @submit="onSubmit" class="flex flex-col gap-6">
      
      <template v-if="isEditing">
        <AuthInput 
          name="nombre" 
          :label="t('register.nombreLabel')" 
          :placeholder="authStore.user?.nombre || ''"
        />
        <AuthInput 
          name="apellidos" 
          :label="t('register.apellidosLabel')" 
          :placeholder="authStore.user?.apellidos || ''"
        />
        <AuthInput 
          name="apodo" 
          :label="t('register.nicknameLabel')" 
          :placeholder="authStore.user?.apodo || ''"
        />
        
        <Field name="url_avatar" v-slot="{ field, value }">
          <ImageUploader 
            :label="t('dashboard.profile.form.avatarLabel')"
            :modelValue="value"
            @update:modelValue="field.onChange"
          />
        </Field>
      </template>

      <template v-else>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <InfoRow :label="t('register.nombreLabel')" :value="authStore.user?.nombre" />
          <InfoRow :label="t('register.apellidosLabel')" :value="authStore.user?.apellidos" />
          <InfoRow :label="t('register.nicknameLabel')" :value="authStore.user?.apodo" />
          
          <div class="py-2">
            <label class="form-label">{{ t('dashboard.profile.form.avatarLabel') }}</label>
            <img 
              v-if="authStore.user?.url_avatar"
              :src="authStore.user.url_avatar" 
              class="h-20 w-20 rounded-full object-cover bg-gray-700 mt-1"
            />
            <p v-else class="text-gray-400 mt-1">-</p>
          </div>
        </div>
      </template>

      <div class="flex justify-end mt-4">
        <button 
          v-if="!isEditing" 
          @click="startEditing" 
          type="button" 
          class="btn btn-secondary w-full sm:w-auto"
        >
          {{ t('dashboard.profile.form.edit') }}
        </button>
        
        <button 
          v-if="isEditing" 
          type="submit" 
          :disabled="cargando" 
          class="btn btn-primary w-full sm:w-auto"
        >
          {{ cargando ? t('resetPassword.sending') : t('dashboard.profile.form.submit') }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import { useForm ,Field} from 'vee-validate' 
import { object, string } from 'yup'
import AuthInput from '@/components/Auth/AuthInput.vue'
import InfoRow from '../shared/InfoRow.vue' 
import ImageUploader from '../shared/ImageUploader.vue'
const { t } = useI18n()
const authStore = useAuthStore()

const isEditing = ref(false)
const cargando = ref(false)
const mensajeExitoKey = ref(null)
const mensajeErrorKey = ref(null)

// --- Lógica de VeeValidate ---



const schema = computed(() => object({
nombre: string().required(t('validation.nameRequired')),
  apellidos: string().required(t('validation.surnameRequired')),
  apodo: string().nullable(),
  url_avatar: string().url(t('validation.urlInvalid')).nullable(),
}))

// eslint-disable-next-line no-unused-vars
const { handleSubmit, setValues, setErrors, resetForm } = useForm({
  validationSchema: schema,
  initialValues: {
    nombre: authStore.user?.nombre || '',
    apellidos: authStore.user?.apellidos || '',
    apodo: authStore.user?.apodo || '',
    url_avatar: authStore.user?.url_avatar || '',
  }
})


watch(() => authStore.user, (newUser) => {
  if (newUser && !isEditing.value) {
    resetForm({
      values: {
        nombre: newUser.nombre || '',
        apellidos: newUser.apellidos || '',
        apodo: newUser.apodo || '',
        url_avatar: newUser.url_avatar || '',
      }
    })
  }
}, { immediate: true, deep: true }) 


const startEditing = () => {
  mensajeExitoKey.value = null
  mensajeErrorKey.value = null
  setErrors({})
  setValues({
    nombre: authStore.user?.nombre || '',
    apellidos: authStore.user?.apellidos || '',
    apodo: authStore.user?.apodo || '',
    url_avatar: authStore.user?.url_avatar || '',
  })
  isEditing.value = true
}


const onSubmit = handleSubmit(async (values) => {
  cargando.value = true
  mensajeErrorKey.value = null

  const apiPayload = {
    ...values,
    numero_telefono: authStore.user.numero_telefono
  };

  try {
    await authStore.updateProfile(apiPayload) 
    mensajeExitoKey.value = 'dashboard.profile.form.success'
    isEditing.value = false
  
  } catch (error) {
    mensajeErrorKey.value = error.message
  } finally {
    cargando.value = false
  }
})
</script>