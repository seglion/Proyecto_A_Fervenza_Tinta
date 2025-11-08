<template>
  <div>
    <label :for="name" class="form-label">{{ label }}</label>
    
    <Field :name="name" v-slot="{ field, meta }">
      <input
        v-bind="field"
        :type="type"
        :placeholder="placeholder"
        class="input"
        :class="{ 'border-red-500': !meta.valid && meta.touched }"
      />
    </Field>

    <ErrorMessage :name="name" class="form-error" />
  </div>
</template>

<script setup>
import { Field, ErrorMessage } from 'vee-validate'

defineProps({
  name: String,
  type: String,
  label: String,
  placeholder: String,
})
</script>