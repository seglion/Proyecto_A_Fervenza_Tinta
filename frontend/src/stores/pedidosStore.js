import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/axios'
import { useAdminStore } from './adminStore'

export const usePedidosStore = defineStore('pedidos', () => {
  // --- STATE ---
  const draftOrder = ref(null) // El carrito
  const isLoading = ref(false)
  const error = ref(null)

  // Dependencias
  const adminStore = useAdminStore()

  const orderHistory = ref([])
  const isLoadingHistory = ref(false)
  const errorHistory = ref(null)
  const isOrderDetailModalOpen = ref(false)
  const orderDetail = ref(null) // Guardará el pedido detallado
  const isLoadingOrderDetail = ref(false)
  const errorOrderDetail = ref(null)
  // --- ACTIONS ---

  async function fetchPrendas() {
    if (adminStore.prendasList.length === 0) {
      await adminStore.fetchAllPrendas(true)
    }
  }

  async function fetchDraftOrder() {
    isLoading.value = true
    error.value = null
    try {
      const response = await apiClient.get('/pedidos/borrador')
      draftOrder.value = response.data
    } catch (e) {
      console.error('Error fetching draft order:', e)
      // Si el error es 401/422 (token caducado), el interceptor de Axios debería manejar el logout
      error.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoading.value = false
    }
  }

  async function addPrendaToCart(prendaId, varianteId, cantidad) {
    if (!draftOrder.value) return

    try {
      const payload = {
        prenda_id: prendaId,
        variante_prenda_id: varianteId,
        cantidad: cantidad,
      }
      // La API (UseCase) ya devuelve el borrador actualizado
      const response = await apiClient.post('/pedidos/borrador/lineas', payload)
      draftOrder.value = response.data // Actualiza el estado
    } catch (e) {
      console.error('Error adding item to cart:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  async function removeLine(lineaId) {
    try {
      // Tu API de 'eliminar linea' también debería devolver el borrador actualizado
      const response = await apiClient.delete(`/pedidos/borrador/lineas/${lineaId}`)
      draftOrder.value = response.data
    } catch (e) {
      console.error('Error removing item from cart:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  async function confirmAndPay() {
    try {
      const response = await apiClient.post('/pedidos/borrador/confirmar-pago')
      const redirectUrl = response.data.url_pago
      if (!redirectUrl) throw new Error('apiErrors.paymentLinkError')
      window.location.href = redirectUrl // Redirige a Stripe
    } catch (e) {
      console.error('Error confirming order and paying:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  async function confirmAndCommission() {
    try {
      await apiClient.post('/pedidos/borrador/confirmar-encargo')
      const router = (await import('@/router')).default
      router.push({ name: 'order-commissioned' }) // Redirige al historial de cuotas (o pedidos)
    } catch (e) {
      console.error('Error confirming order as commission:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  async function fetchOrderHistory() {
    if (orderHistory.value.length > 0) return // No recargar

    isLoadingHistory.value = true
    errorHistory.value = null
    try {
      // Llama al endpoint de Listar Pedidos
      const response = await apiClient.get('/pedidos/')

      // Asumimos que la API devuelve una lista de PedidoDTO
      // (Filtramos el 'BORRADOR' porque solo queremos el historial)
      orderHistory.value = response.data.pedidos.filter((pedido) => pedido.estado !== 'BORRADOR')
    } catch (e) {
      console.error('Error fetching order history:', e)
      errorHistory.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingHistory.value = false
    }
  }
async function openOrderDetailModal(pedidoId) {
    isOrderDetailModalOpen.value = true
    isLoadingOrderDetail.value = true
    errorOrderDetail.value = null
    orderDetail.value = null 
    
    try {
      // Llama al endpoint GET /api/v1/pedidos/{pedido_id}
      const response = await apiClient.get(`/pedidos/${pedidoId}`)
      orderDetail.value = response.data
    } catch (e) {
      console.error('Error fetching order detail by ID:', e)
      errorOrderDetail.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingOrderDetail.value = false
    }
  }
  function closeOrderDetailModal() {
    isOrderDetailModalOpen.value = false
    orderDetail.value = null
    errorOrderDetail.value = null
  }
  // --- GETTERS ---
  const cartItemCount = computed(() => {
    return draftOrder.value?.lineas?.reduce((total, line) => total + line.cantidad, 0) || 0
  })

  const prendasList = computed(() => adminStore.prendasList)

  return {
    draftOrder,
    prendasList,
    isLoading,
    error,
    fetchPrendas,
    fetchDraftOrder,
    cartItemCount,
    addPrendaToCart,
    removeLine,
    confirmAndPay,
    confirmAndCommission,

    orderHistory,
    isLoadingHistory,
    errorHistory,
    fetchOrderHistory,
    isOrderDetailModalOpen,
    orderDetail,
    isLoadingOrderDetail,
    errorOrderDetail,
    openOrderDetailModal,
    closeOrderDetailModal
  }
})
