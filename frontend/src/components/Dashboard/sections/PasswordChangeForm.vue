<template>
  <div>
    <p v-if="mensajeExitoKey" class="text-green-400 text-sm mb-4 text-center">
      {{ t(mensajeExitoKey) }}
    </p>
    <p v-if="mensajeErrorKey" class="text-red-500 text-sm mb-4 text-center">
      {{ t(mensajeErrorKey, 'apiErrors.genericError') }}
    </p>

    <AuthForm
      :fields="fields"
      :onSubmit="onSubmit"
      :loading="cargando"
      :submitLabel="t('password.form.submit')"
      :isReadOnly="false" 
    />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import { useForm } from 'vee-validate' 
import { object, string, ref as yupRef } from 'yup'
import AuthForm from '@/components/Auth/AuthForm.vue'

const { t } = useI18n()
const authStore = useAuthStore()

const cargando = ref(false)
const mensajeExitoKey = ref(null)
const mensajeErrorKey = ref(null)

const fields = computed(() => [
  { 
    name: 'oldPassword', 
    type: 'password', 
    label: t('password.form.oldPassword'), 
    placeholder: '********', 
    autocomplete: 'current-password' 
  },
  { 
    name: 'newPassword', 
    type: 'password', 
    label: t('password.form.newPassword'), 
    placeholder: '********', 
    autocomplete: 'new-password' 
  },
  { 
    name: 'newPasswordConfirm', 
    type: 'password', 
    label: t('password.form.confirmPassword'), 
    placeholder: '********', 
    autocomplete: 'new-password' 
  },
])

const schema = computed(() => object({
  oldPassword: string().required(t('validation.passwordRequired')),
  newPassword: string()
    .required(t('validation.passwordRequired'))
    .min(8, t('validation.passwordMin'))
    .matches(/[a-z]/, t('validation.passwordLowercase'))
    .matches(/[A-Z]/, t('validation.passwordUppercase'))
    .matches(/[0-9]/, t('validation.passwordNumber'))
    .matches(/[^A-Za-z0-9]/, t('validation.passwordSpecial')),
  newPasswordConfirm: string()
    .required(t('validation.passwordRequired'))
    .oneOf([yupRef('newPassword')], t('validation.passwordConfirmMatch')),
}))

const { handleSubmit, resetForm } = useForm({
  validationSchema: schema,
  initialValues: { oldPassword: '', newPassword: '', newPasswordConfirm: '' }
})

const onSubmit = handleSubmit(async (values) => {
  cargando.value = true;
  mensajeExitoKey.value = null;
  mensajeErrorKey.value = null;
  
  const passwordData = {
    oldPassword: values.oldPassword,
    newPassword: values.newPassword
  };

  try {
    await authStore.changePassword(passwordData);
    mensajeExitoKey.value = 'password.form.success';
    resetForm(); // Limpia los campos
  
  } catch (error) {
    mensajeErrorKey.value = error.message;
  } finally {
    cargando.value = false;
  }
});
</script>