<template>
  <AuthLayout>
    <div class="absolute top-6 right-6 z-30">
      <LanguageSelector />
    </div>

    <div class="mb-8 text-center">
      <h1 class="font-display text-3xl sm:text-5xl font-bold uppercase tracking-wider">
        {{ t('register.title') }}
      </h1>
    </div>

    <AuthForm
      :fields="fields"
      :submitLabel="t('register.submit')"
      :onSubmit="onSubmit" :loading="cargando"
      :successMessage="mensajeExitoKey ? t(mensajeExitoKey) : null"
      :errorMessage="mensajeErrorKey ? t(mensajeErrorKey, 'apiErrors.genericError') : null"
    />

    <div class="mt-8 text-center">
      <p class="text-sm text-gray-300">
        {{ t('register.alreadyAccount') }}
        <RouterLink to="/login" class="font-bold text-white underline hover:text-red-600">
          {{ t('register.loginLink') }}
        </RouterLink>
      </p>
    </div>
  </AuthLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { object, string, ref as yupRef } from 'yup'
import { useForm } from 'vee-validate' 
import { useAuthStore } from '@/stores/auth'
import { useI18n } from 'vue-i18n'
import AuthLayout from './AuthLayout.vue'
import AuthForm from './AuthForm.vue'
import LanguageSelector from '@/components/lenguage/LanguageSelector.vue'

const { t } = useI18n()
const authStore = useAuthStore()
const cargando = ref(false)
const mensajeExitoKey = ref(null)
const mensajeErrorKey = ref(null)

const fields = computed(() => [
  { name: 'nombre', type: 'text', placeholder: 'Tu nombre', label: t('register.nombreLabel') },
  { name: 'apellidos', type: 'text', placeholder: 'Tus apellidos', label: t('register.apellidosLabel') },
  { name: 'phone', type: 'tel', placeholder: '+34 600 000 000', label: t('register.phoneLabel') },
  { name: 'email', type: 'email', placeholder: 'example@example.com', label: t('register.emailLabel') },
  { name: 'nickname', type: 'text', placeholder: 'Tu apodo (opcional)', label: t('register.nicknameLabel') },
  { name: 'password', type: 'password', placeholder: 'Crea tu contraseña', label: t('register.passwordLabel') },
  { name: 'passwordConfirm', type: 'password', placeholder: 'Confirma tu contraseña', label: t('register.passwordConfirmLabel') },
])

const schema = computed(() => object({
  nombre: string().required(t('validation.nameRequired')),
  apellidos: string().required(t('validation.surnameRequired')),
  phone: string().required(t('validation.phoneRequired')),
  email: string().email(t('validation.emailInvalid')).required(t('validation.emailRequired')),
  nickname: string().nullable(),
  password: string()
    .required(t('validation.passwordRequired'))
    .min(8, t('validation.passwordMin'))
    .matches(/[a-z]/, t('validation.passwordLowercase'))
    .matches(/[A-Z]/, t('validation.passwordUppercase'))
    .matches(/[0-9]/, t('validation.passwordNumber'))
    .matches(/[^A-Za-z0-9]/, t('validation.passwordSpecial')),
  passwordConfirm: string()
    .required(t('validation.passwordRequired'))
    .oneOf([yupRef('password')], t('validation.passwordConfirmMatch')),
}))

const initialValues = {
  nombre: '', apellidos: '', phone: '', email: '',
  nickname: '', password: '', passwordConfirm: '',
}

const { handleSubmit } = useForm({
  validationSchema: schema,
  initialValues: initialValues
})

const onSubmit = handleSubmit(async (values, { resetForm }) => {
  cargando.value = true
  mensajeErrorKey.value = null
  mensajeExitoKey.value = null
  try {
    await authStore.register(values)
    mensajeExitoKey.value = 'register.successMessage'
    resetForm()
  } catch (error) {
    mensajeErrorKey.value = error.message
  } finally {
    cargando.value = false
  }
})
</script>