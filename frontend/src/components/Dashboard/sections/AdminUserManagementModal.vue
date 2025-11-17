<template>
  <div class="fixed inset-0 bg-black/80 z-40 flex items-center justify-center p-4">
    <div class=" border-2 border-red-600 rounded-lg w-full max-w-lg p-6 z-50"  style="background-color: #000000">
      
      <div class="flex justify-between items-center border-b border-gray-700 pb-3 mb-4" >
        <h2 class="font-display text-2xl uppercase text-white">
          {{ t('adminUsers.modal.title') }}
        </h2>
        <button @click="$emit('close')" class="text-gray-400 hover:text-white">
          <span class="material-symbols-outlined">close</span>
        </button>
      </div>

      <div class="mb-6">
        <p class="text-lg text-red-600 font-bold">{{ user.nombre }} ({{ user.rol }})</p>
        <p class="text-gray-400 text-sm">{{ user.email }}</p>
      </div>

      <div class="space-y-4">
        <h3 class="text-white font-bold">{{ t('adminUsers.modal.roleTitle') }}</h3>
        <UserRoleForm :user="user" @role-updated="handleSuccess" />

        <hr class="border-gray-700">

        <h3 class="text-white font-bold">{{ t('adminUsers.modal.actionsTitle') }}</h3>
        <div class="flex flex-col sm:flex-row gap-3">
          <button @click="forceReset" :disabled="isLoadingAction" class="btn btn-secondary !py-2 !px-4 !bg-red-800 hover:!bg-red-700">
            {{ t('adminUsers.actions.forceReset') }}
          </button>
          <button @click="handleDelete" :disabled="isLoadingAction" class="btn btn-secondary !py-2 !px-4 !bg-red-900 hover:!bg-red-800">
            {{ t('adminUsers.actions.deleteUser') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAdminStore } from '@/stores/adminStore';
import { useI18n } from 'vue-i18n';
import UserRoleForm from './UserRoleForm.vue'; 

const props = defineProps({
  user: { type: Object, required: true }
});
const emit = defineEmits(['close']);
const { t } = useI18n();
const adminStore = useAdminStore();

const isLoadingAction = ref(false);

const handleSuccess = () => {
  emit('close'); 
};

async function forceReset() {
  if (!confirm(t('adminUser.actions.confirmReset'))) return;
  isLoadingAction.value = true;
  try {
    await adminStore.forcePasswordReset(props.user.id);
    alert(t('adminUsers.actions.resetSuccess'));
    emit('close');
  } catch (error) {
    alert(t(error.message));
  } finally {
    isLoadingAction.value = false;
  }
}

async function handleDelete() {
  if (!confirm(t('adminUsers.actions.confirmDelete'))) return;
  isLoadingAction.value = true;
  try {
    await adminStore.rejectUser(props.user.id); 
    emit('close');
  } catch (error) {
    alert(t(error.message));
  } finally {
    isLoadingAction.value = false;
  }
}
</script>