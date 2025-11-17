<template>
  <div class="flex flex-col sm:flex-row gap-3 items-center">
    <select v-model="selectedRole" class="grow w-full border-2 border-white rounded-md p-3 text-base text-white
             bg-black focus:border-red-600 focus:outline-none focus:ring-0">
      <option 
        v-for="role in availableRoles" 
        :key="role.value" 
        :value="role.value"
        style="background-color: #000000; color: white;"
      >
        {{ role.label }}
      </option>
    </select>
    
    <button 
      @click="updateRole" 
      :disabled="isLoading" 
      
      class="btn btn-primary w-full sm:w-auto" 
      
      
    >
      {{ isLoading ? t('resetPassword.sending') : t('adminUsers.actions.updateRole') }}
    </button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAdminStore } from '@/stores/adminStore';
import { Role } from '@/constants/roles';
import { useI18n } from 'vue-i18n';

const props = defineProps({
  user: { type: Object, required: true }
});
const emit = defineEmits(['role-updated']);

const { t } = useI18n();
const adminStore = useAdminStore();

const isLoading = ref(false);
const selectedRole = ref(props.user.rol); // Valor inicial

const availableRoles = computed(() => [

  { value: Role.ADMIN, label: t(`dashboard.roles.ADMIN`) },
  { value: Role.USER, label: t(`dashboard.roles.USUARIO`) }
]);

async function updateRole() {
  if (selectedRole.value === props.user.rol) return; 
  isLoading.value = true;
  try {
    await adminStore.setUserRole(props.user.id, selectedRole.value);
    emit('role-updated'); 
  } catch (error) {
    alert(error.message);
  } finally {
    isLoading.value = false;
  }
}
</script>