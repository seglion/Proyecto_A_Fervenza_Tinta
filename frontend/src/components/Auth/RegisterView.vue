<template>
  <AuthLayout>
    <div class="mb-8 text-center">
      <h1 class="font-display text-5xl font-bold uppercase tracking-wider">Register</h1>
    </div>

    <AuthForm
      :fields="fields"
      :submitLabel="'Register'"
      :onSubmit="handleSubmit"
    />

    <div class="mt-8 text-center">
      <p class="text-sm text-gray-300">
        Already have an account?
        <RouterLink to="/login" class="font-bold text-white underline hover:text-red-600">
          Login
        </RouterLink>
      </p>
    </div>
  </AuthLayout>
</template>

<script setup>
import AuthLayout from './AuthLayout.vue'
import AuthForm from './AuthForm.vue'
import { object, string, ref as yupRef } from 'yup'
import { useForm } from 'vee-validate'

const fields = [
  { name: 'fullName', placeholder: 'Full Name' },
  { name: 'email', type: 'email', placeholder: 'Email' },
  { name: 'password', type: 'password', placeholder: 'Password' },
  { name: 'confirmPassword', type: 'password', placeholder: 'Confirm Password' },
]

const schema = object({
  fullName: string().required(),
  email: string().email().required(),
  password: string().min(6).required(),
  confirmPassword: string()
    .oneOf([yupRef('password')], 'La contraseña debe coincidir')
    .required(),
})

const { handleSubmit } = useForm({
  validationSchema: schema,
  onSubmit: (values) => {
    console.log('Register:', values)
  },
})
</script>
