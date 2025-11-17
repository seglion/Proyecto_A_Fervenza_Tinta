<template>
    <div>
        <h1 class="font-display font-bold uppercase tracking-wider text-white mb-8 text-4xl sm:text-5xl">
            {{ t('merchandise.title') }}
        </h1>

        <button 
          @click="isCartModalOpen = true"
          class="sm:invisible fixed top-6 right-6 z-30 btn btn-primary rounded-full! p-3! h-16! w-16! shadow-lg"
        >
          <span class="material-symbols-outlined text-3xl">shopping_cart</span>
          <span 
            v-if="pedidosStore.cartItemCount > 0"
            class="absolute -top-1 -right-1 bg-white text-black text-xs font-bold rounded-full h-6 w-6 flex items-center justify-center"
          >
            {{ pedidosStore.cartItemCount }}
          </span>
        </button>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <div class="lg:col-span-2">
                <div v-if="adminStore.isLoadingPrendas" class="text-gray-400 p-4 text-center">
                    {{ t('dashboard.view.feeLoading') }}
                </div>
                <div v-else-if="adminStore.errorPrendas" class="text-red-500 p-4 text-center">
                    {{ t(adminStore.errorPrendas) }}
                </div>

                <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <ProductCard
                        v-for="prenda in adminStore.prendasList"
                        :key="prenda.id"
                        :prenda="prenda"
                        @select="openVariantModal(prenda)"
                    />
                </div>
            </div>

            <div class="hidden lg:block lg:col-span-1">
                <ShoppingCart class="sticky top-8" />
            </div>
        </div>

        <ProductVariantModal
            v-if="selectedPrenda"
            :prenda="selectedPrenda"
            @close="closeVariantModal"
        />

        <CartModal 
            v-if="isCartModalOpen" 
            @close="isCartModalOpen = false" 
        />

    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useAdminStore } from '@/stores/adminStore'
import { usePedidosStore } from '@/stores/pedidosStore'
import { useI18n } from 'vue-i18n'
import ProductCard from '@/components/dashboard/shared/ProductCard.vue'
import ProductVariantModal from '@/components/dashboard/sections/ProductVariantModal.vue'
import ShoppingCart from '@/components/Dashboard/sections/ShoppingCart.vue' // <-- Columna Desktop
import CartModal from '@/components/Dashboard/sections/CartModal.vue' // <-- Modal Móvil

const { t } = useI18n()
const adminStore = useAdminStore()
const pedidosStore = usePedidosStore()

// --- Estado local para los modales ---
const selectedPrenda = ref(null)
const isCartModalOpen = ref(false) // <-- Estado local, no en Pinia

onMounted(() => {
    adminStore.fetchAllPrendas()
    pedidosStore.fetchDraftOrder()
})

function openVariantModal(prenda) {
    selectedPrenda.value = prenda
}
function closeVariantModal() {
    selectedPrenda.value = null
}
</script>