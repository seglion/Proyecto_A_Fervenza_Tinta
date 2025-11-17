<template>
  <div>
    <label 
      :for="name" 
      class="form-label"
    >
      {{ label }}
    </label>
    
    <input
      v-if="disabled"
      :type="type"
      :value="modelValue"
      disabled
      class="input bg-gray-800 text-gray-400 cursor-not-allowed"
    />
    
    <Field v-else :name="name" v-slot="{ field, meta }">
      <input
        v-bind="field"
        :type="type"
        :placeholder="placeholder"
        class="input"
        :class="{ 'border-red-500 focus:border-red-500': !meta.valid && meta.touched }"
      />
    </Field>
    
    <ErrorMessage :name="name" class="form-error" />
  </div>
</template>

<script setup>
import { Field, ErrorMessage } from 'vee-validate'

defineProps({
  name: { type: String, required: true },
  label: { type: String, required: true },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  disabled: { type: Boolean, default: false },
  
  modelValue: { type: String, default: '' } ,
  autocomplete: { type: String, default: 'off' }
})
</script>