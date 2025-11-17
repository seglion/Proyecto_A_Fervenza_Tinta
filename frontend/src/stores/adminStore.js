import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/axios'
import { useAuthStore } from './auth'
export const useAdminStore = defineStore('admin', () => {
  // --- STATE ---

  // Estado para la lista principal de usuarios
  const userList = ref([])
  const isLoadingUsers = ref(false)
  const errorUsers = ref(null)

  // Estado para el Modal de GESTIÓN (Editar Rol, etc.)
  const isManagementModalOpen = ref(false)
  const userToManage = ref(null)

  // Estado para el Modal de DETALLE (Solo Ver Perfil)
  const isDetailModalOpen = ref(false)
  const userDetail = ref(null)
  const isLoadingDetail = ref(false)
  const errorDetail = ref(null)

  // --- ¡NUEVO! Estado para Pagos Recientes ---
  const recentPayments = ref([])
  const isLoadingPayments = ref(false)
  const errorPayments = ref(null)

  const allPaymentsList = ref([]) // Para la lista completa de cuotas
  const isLoadingAllPayments = ref(false)
  const allSeasonsList = ref([]) // Para el dropdown de temporadas
  const isLoadingSeasons = ref(false)
  const errorAllPayments = ref(null) // Error para la lista de cuotas
  const isUpdatingSeason = ref(false)
  const errorSeason = ref(null)
  const isPaymentDetailModalOpen = ref(false)
  const paymentDetail = ref(null) // Guardará el detalle de la cuota
  const isLoadingPaymentDetail = ref(false)
  const errorPaymentDetail = ref(null)

  const pendingReport = ref([])
  const isLoadingPendingReport = ref(false)
  const errorPendingReport = ref(null)

  const isManualPaymentModalOpen = ref(false)
  const cuotaToPayManually = ref(null) // Guardará la cuota a pagar
  const isLoadingManualPayment = ref(false)
  const errorManualPayment = ref(null)

  const prendasList = ref([])
  const isLoadingPrendas = ref(false)
  const errorPrendas = ref(null)

  const isPrendaModalOpen = ref(false)
  const prendaToEdit = ref(null) // null = Crear, Objeto = Editar
  const isLoadingPrendaModal = ref(false)
  const errorPrendaModal = ref(null)

  const allOrdersList = ref([])
  const allOrderSeasonsList = ref([])
  const isLoadingOrders = ref(false)
  const errorOrders = ref(null)

  const isOrderDetailModalOpen = ref(false)
  const orderDetail = ref(null)
  const isLoadingOrderDetail = ref(false)
  const errorOrderDetail = ref(null)
  const productionSummary = ref([])
  const isLoadingSummary = ref(false)

  const isUpdatingOrderSeason = ref(false) // Para el modal
  const errorOrderSeason = ref(null)
  // --- ACTIONS (API) ---

  /**
   * Obtiene la lista COMPLETA de usuarios de la API.
   */
  async function fetchAllUsers(forceRefresh = false) {
    if (userList.value.length > 0 && !forceRefresh) return

    isLoadingUsers.value = true
    errorUsers.value = null
    try {
      const response = await apiClient.get('/admin/users')
      userList.value = response.data
    } catch (e) {
      errorUsers.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingUsers.value = false
    }
  }

  // --- ¡NUEVA ACCIÓN! ---
  /**
   * Obtiene las 5 cuotas completadas más recientes desde
   * el nuevo endpoint optimizado.
   */
  async function fetchRecentPayments() {
    // No recargar si ya los tenemos
    if (recentPayments.value.length > 0) return

    isLoadingPayments.value = true
    errorPayments.value = null

    try {
      // Llama al endpoint de 'recentes'
      const response = await apiClient.get('/cuotas/recientes')
      recentPayments.value = response.data.cuotas
    } catch (e) {
      console.error('Error fetching recent payments:', e)
      errorPayments.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingPayments.value = false
    }
  }

  /**
   * Llama a la API para aprobar un usuario y refresca la lista.
   */
  async function approveUser(userId) {
    try {
      await apiClient.post(`/admin/users/${userId}/aprobar`)
      await fetchAllUsers(true) // Refresca la lista
    } catch (e) {
      console.error('Error approving user:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  /**
   * Llama a la API para rechazar (Borrar/Desactivar) un usuario y refresca la lista.
   */
  async function rejectUser(userId) {
    try {
      await apiClient.delete(`/admin/users/${userId}`)
      await fetchAllUsers(true) // Refresca la lista
    } catch (e) {
      console.error('Error rejecting user:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  /**
   * Llama a la API para cambiar el estado (activar/desactivar) y refresca la lista.
   */
  async function setUserStatus(userId, newStatus) {
    try {
      await apiClient.put(`/admin/users/${userId}/estado`, { esta_activo: newStatus })
      await fetchAllUsers(true) // Refresca la lista
    } catch (e) {
      console.error('Error setting user status:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  /**
   * Llama a la API para modificar el rol de un usuario y refresca la lista.
   */
  async function setUserRole(userId, newRole) {
    try {
      await apiClient.put(`/admin/users/${userId}/roles`, { rol: newRole })
      await fetchAllUsers(true) // Refresca la lista
    } catch (e) {
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  /**
   * Llama a la API para forzar un reseteo de contraseña.
   */
  async function forcePasswordReset(userId) {
    try {
      await apiClient.post(`/admin/users/${userId}/forzar-reseteo`)
    } catch (e) {
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  // --- ACTIONS (MODAL DE DETALLE) ---

  async function openDetailModal(userId) {
    isDetailModalOpen.value = true
    isLoadingDetail.value = true
    errorDetail.value = null
    userDetail.value = null

    try {
      const response = await apiClient.get(`/admin/users/${userId}`)
      userDetail.value = response.data
    } catch (e) {
      console.error('Error fetching user by ID:', e)
      errorDetail.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingDetail.value = false
    }
  }

  function closeDetailModal() {
    isDetailModalOpen.value = false
    userDetail.value = null
    errorDetail.value = null
  }

  // --- ACTIONS (MODAL DE GESTIÓN) ---

  function openManagementModal(user) {
    userToManage.value = user
    isManagementModalOpen.value = true
  }

  function closeManagementModal() {
    isManagementModalOpen.value = false
    userToManage.value = null
  }

  // --- GETTERS (Estadísticas calculadas desde userList) ---

  const getTotalUsers = computed(() => userList.value.length)

  const getActiveMembers = computed(() => {
    return userList.value.filter((user) => user.esta_activo).length
  })

  const getNewMembers30d = computed(() => {
    const thirtyDaysAgo = new Date()
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
    return userList.value.filter((user) => {
      if (!user.fecha_creacion) return false
      const creationDate = new Date(user.fecha_creacion)
      return creationDate > thirtyDaysAgo
    }).length
  })

  const getPendingMembersCount = computed(() => {
    return userList.value.filter((user) => !user.aprobado_por_admin).length
  })

  async function fetchAllPayments() {
    if (allPaymentsList.value.length > 0) return

    isLoadingAllPayments.value = true
    errorAllPayments.value = null
    try {
      const response = await apiClient.get('/cuotas/')
      allPaymentsList.value = response.data.cuotas
    } catch (e) {
      console.error('Error fetching all payments:', e)
      errorAllPayments.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingAllPayments.value = false
    }
  }

  async function fetchAllSeasons() {
    if (allSeasonsList.value.length > 0) return
    isLoadingSeasons.value = true
    try {
      const response = await apiClient.get('/cuotas/temporadas')
      allSeasonsList.value = response.data.temporadas
    } catch (e) {
      console.error('Error fetching seasons:', e)
    } finally {
      isLoadingSeasons.value = false
    }
  }
  async function createSeason(seasonData) {
    isUpdatingSeason.value = true
    errorSeason.value = null
    try {
      // Llama a /api/v1/cuotas/temporadas
      await apiClient.post('/cuotas/temporadas', seasonData)
      await fetchAllSeasons(true) // Refresca la lista
    } catch (e) {
      console.error('Error creating season:', e)
      errorSeason.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorSeason.value) // Lanza el error al modal
    } finally {
      isUpdatingSeason.value = false
    }
  }

  /**
   * Actualiza una temporada existente (PUT)
   */
  async function updateSeason(temporadaId, seasonData) {
    isUpdatingSeason.value = true
    errorSeason.value = null
    try {
      // Llama a /api/v1/cuotas/temporadas/{id}
      await apiClient.put(`/cuotas/temporadas/${temporadaId}`, seasonData)
      await fetchAllSeasons(true) // Refresca la lista
    } catch (e) {
      console.error('Error updating season:', e)
      errorSeason.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorSeason.value) // Lanza el error al modal
    } finally {
      isUpdatingSeason.value = false
    }
  }
  async function openPaymentDetailModal(cuotaId) {
    isPaymentDetailModalOpen.value = true
    isLoadingPaymentDetail.value = true
    errorPaymentDetail.value = null
    paymentDetail.value = null

    try {
      // Llamamos al endpoint GET /api/v1/admin/cuotas/{cuota_id}
      // (Asumiendo que está en el router de admin, si no, quita /admin)
      const response = await apiClient.get(`/cuotas/${cuotaId}`)
      paymentDetail.value = response.data
    } catch (e) {
      console.error('Error fetching payment detail by ID:', e)
      errorPaymentDetail.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingPaymentDetail.value = false
    }
  }

  function closePaymentDetailModal() {
    isPaymentDetailModalOpen.value = false
    paymentDetail.value = null
    errorPaymentDetail.value = null
  }

  async function fetchPendingReport() {
    if (pendingReport.value.length > 0) return // No recargar

    isLoadingPendingReport.value = true
    errorPendingReport.value = null
    try {
      // (Asumiendo que está en el router de admin)
      const response = await apiClient.get('/cuotas/informe-pendientes')
      // El DTO devuelve { pendientes: [...] }
      pendingReport.value = response.data.pendientes
    } catch (e) {
      console.error('Error fetching pending report:', e)
      errorPendingReport.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingPendingReport.value = false
    }
  }

  async function registerManualPayment(cuotaId, paymentData) {
    isLoadingManualPayment.value = true
    errorManualPayment.value = null
    try {
      await apiClient.put(`/cuotas/${cuotaId}/registrar-manual`, paymentData)

      // Refresca AMBAS listas
      await fetchAllPayments(true)
      await fetchPendingReport(true)
    } catch (e) {
      console.error('Error registering manual payment:', e)
      errorManualPayment.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorManualPayment.value)
    } finally {
      isLoadingManualPayment.value = false
    }
  }
  async function fetchAllPrendas(forceRefresh = false) {
    // No recargar si ya las tenemos y no forzamos
    if (prendasList.value.length > 0 && !forceRefresh) return

    isLoadingPrendas.value = true
    errorPrendas.value = null
    try {
      // Llama al endpoint GET /api/v1/prendas/
      const response = await apiClient.get('/prendas/')
      // Tu API devuelve { "prendas": [...] }
      prendasList.value = response.data.prendas
    } catch (e) {
      console.error('Error fetching prendas:', e)
      errorPrendas.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingPrendas.value = false
    }
  }
  // --- ¡NUEVAS ACCIONES DE MODAL! ---
  function openManualPaymentModal(cuota) {
    cuotaToPayManually.value = cuota
    isManualPaymentModalOpen.value = true
    errorManualPayment.value = null // Limpia errores antiguos
  }

  function closeManualPaymentModal() {
    isManualPaymentModalOpen.value = false
    cuotaToPayManually.value = null
  }

  function openCreatePrendaModal() {
    prendaToEdit.value = null // Asegura que está vacío
    isPrendaModalOpen.value = true
    errorPrendaModal.value = null
  }

  // Abre el modal en modo "Editar"
  function openEditPrendaModal(prenda) {
    prendaToEdit.value = prenda // Carga la prenda a editar
    isPrendaModalOpen.value = true
    errorPrendaModal.value = null
  }

  // Cierra el modal
  function closePrendaModal() {
    isPrendaModalOpen.value = false
    prendaToEdit.value = null
  }

  /**
   * Llama a la API para crear una nueva prenda (POST)
   */
  async function createPrenda(prendaData) {
    isLoadingPrendaModal.value = true
    errorPrendaModal.value = null
    try {
      await apiClient.post('/prendas/', prendaData)
      await fetchAllPrendas(true) // Refresca la lista
    } catch (e) {
      console.error('Error creating prenda:', e)
      errorPrendaModal.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorPrendaModal.value) // Lanza el error al modal
    } finally {
      isLoadingPrendaModal.value = false
    }
  }

  /**
   * Llama a la API para actualizar una prenda (PUT)
   */
  async function updatePrenda(prendaId, prendaData) {
    isLoadingPrendaModal.value = true
    errorPrendaModal.value = null
    try {
      await apiClient.put(`/prendas/${prendaId}`, prendaData)
      await fetchAllPrendas(true) // Refresca la lista
    } catch (e) {
      console.error('Error updating prenda:', e)
      errorPrendaModal.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorPrendaModal.value) // Lanza el error al modal
    } finally {
      isLoadingPrendaModal.value = false
    }
  }

  /**
   * Llama a la API para borrar una prenda (DELETE)
   */
  async function deletePrenda(prendaId) {
    // Reutilizamos el estado de carga principal de prendas
    isLoadingPrendas.value = true
    errorPrendas.value = null
    try {
      // Llama al endpoint DELETE /api/v1/prendas/{prenda_id}
      await apiClient.delete(`/prendas/${prendaId}`)

      // Refresca la lista para eliminarla de la vista
      await fetchAllPrendas(true)
    } catch (e) {
      console.error('Error deleting prenda:', e)
      errorPrendas.value = e.response?.data?.detail || 'apiErrors.genericError'
      // Lanza el error para que el componente (vista) lo pueda atrapar
      throw new Error(errorPrendas.value)
    } finally {
      // (isLoadingPrendas se pondrá en 'false' por fetchAllPrendas)
    }
  }
  async function addPrendaVariante(prendaId, varianteData) {
    // No usamos el spinner global, el modal usará su propio spinner
    errorPrendaModal.value = null
    try {
      // Llama a POST /api/v1/prendas/{prenda_id}/variantes
      await apiClient.post(`/prendas/${prendaId}/variantes`, varianteData)

      // Refresca la lista Y el objeto 'prendaToEdit'
      await fetchAllPrendas(true) // Refresca la tabla principal
      const updatedPrenda = prendasList.value.find((p) => p.id === prendaId)
      if (updatedPrenda) {
        prendaToEdit.value = updatedPrenda // Refresca el modal
      }
    } catch (e) {
      console.error('Error adding variante:', e)
      errorPrendaModal.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorPrendaModal.value)
    }
  }

  /**
   * Llama a la API para BORRAR una variante de una prenda (DELETE)
   */
  async function deletePrendaVariante(prendaId, varianteId) {
    errorPrendaModal.value = null
    try {
      // Llama a DELETE /api/v1/prendas/{prenda_id}/variantes/{variante_id}
      await apiClient.delete(`/prendas/${prendaId}/variantes/${varianteId}`)

      // Refresca la lista Y el objeto 'prendaToEdit'
      await fetchAllPrendas(true)
      const updatedPrenda = prendasList.value.find((p) => p.id === prendaId)
      if (updatedPrenda) {
        prendaToEdit.value = updatedPrenda
      }
    } catch (e) {
      console.error('Error deleting variante:', e)
      errorPrendaModal.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorPrendaModal.value)
    }
  }
  async function fetchAllOrders(temporadaId = 'all') {
    isLoadingOrders.value = true
    errorOrders.value = null

    // Prepara los query params (SOLO temporada_id)
    const params = new URLSearchParams()
    if (temporadaId && temporadaId !== 'all') {
      params.append('temporada_id', temporadaId)
    }

    try {
      // Llama al endpoint con el filtro de temporada
      const response = await apiClient.get('/admin/pedidos/', { params })

      // Asumimos que la API devuelve los JOINs (nombres de usuario)
      allOrdersList.value = response.data.pedidos || response.data
    } catch (e) {
      console.error('Error fetching orders:', e)
      errorOrders.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingOrders.value = false
    }
  }

  /**
   * Obtiene las temporadas de PEDIDOS (diferentes a las de cuotas).
   * Endpoint: GET /api/v1/admin/pedidos/temporadas
   */
  async function fetchAllOrderSeasons(forceRefresh = false) {
    if (allOrderSeasonsList.value.length > 0 && !forceRefresh) return

    try {
      const response = await apiClient.get('/admin/pedidos/temporadas')
      allOrderSeasonsList.value = response.data.temporadas || response.data
    } catch (e) {
      console.error('Error fetching order seasons:', e)
    }
  }

  async function openOrderDetailModal(pedidoId) {
    isOrderDetailModalOpen.value = true
    isLoadingOrderDetail.value = true
    errorOrderDetail.value = null
    orderDetail.value = null

    try {
      // Llama al endpoint GET /api/v1/admin/pedidos/{pedido_id}
      const response = await apiClient.get(`/admin/pedidos/${pedidoId}`)
      orderDetail.value = response.data
    } catch (e) {
      console.error('Error fetching admin order detail:', e)
      errorOrderDetail.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingOrderDetail.value = false
    }
  }

  function closeOrderDetailModal() {
    isOrderDetailModalOpen.value = false
  }

  async function markOrderAsPaid(pedidoId) {
    const authStore = useAuthStore()
    const adminId = authStore.user.id

    // 2. Construimos el PAYLOAD requerido
    const payload = {
      // Usamos EFECTIVO o TRANSFERENCIA (asumimos EFECTIVO para la rapidez)
      metodo_pago: 'MANUAL',

      // Enviamos el ID del administrador para trazar quién hizo el registro manual
      id_transaccion_externa: adminId,
    }

    try {
      await apiClient.post(`/admin/pedidos/${pedidoId}/marcar-pagado`, payload)
      // Refresca la lista para que la UI muestre el estado "COMPLETADO"
      await fetchAllOrders(true)
    } catch (e) {
      console.error('Error marking order as paid:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  /**
   * Llama a la API para cancelar un pedido.
   * Endpoint: DELETE /api/v1/admin/pedidos/{pedido_id}/cancelar
   */
  async function cancelOrder(pedidoId) {
    try {
      await apiClient.delete(`/admin/pedidos/${pedidoId}/cancelar`)
      // Refresca la lista (el pedido desaparecerá o cambiará a "CANCELADO")
      await fetchAllOrders(true)
    } catch (e) {
      console.error('Error canceling order:', e)
      throw new Error(e.response?.data?.detail || 'apiErrors.genericError')
    }
  }

  async function fetchProductionSummary(temporadaId) {
    isLoadingSummary.value = true
    productionSummary.value = [] // Limpia el resumen anterior
    try {
      // Llama al nuevo endpoint
      const response = await apiClient.get(`/admin/pedidos/resumen-produccion/${temporadaId}`)

      productionSummary.value = response.data.resumen
    } catch (e) {
      console.error('Error fetching production summary:', e)
    } finally {
      isLoadingSummary.value = false
    }
  }
 

  /**
   * Crea una nueva temporada de PEDIDO (POST)
   */
  async function createOrderSeason(seasonData) {
    isUpdatingOrderSeason.value = true
    errorOrderSeason.value = null
    try {
      await apiClient.post('/admin/pedidos/temporadas', seasonData)
      await fetchAllOrderSeasons(true) // Refresca la lista
    } catch (e) {
      console.error('Error creating order season:', e)
      errorOrderSeason.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorOrderSeason.value)
    } finally {
      isUpdatingOrderSeason.value = false
    }
  }

  /**
   * Actualiza una temporada de PEDIDO (PUT)
   */
  async function updateOrderSeason(temporadaId, seasonData) {
    isUpdatingOrderSeason.value = true
    errorOrderSeason.value = null
    try {
      await apiClient.put(`/admin/pedidos/temporadas/${temporadaId}`, seasonData)
      await fetchAllOrderSeasons(true) // Refresca la lista
    } catch (e) {
      console.error('Error updating order season:', e)
      errorOrderSeason.value = e.response?.data?.detail || 'apiErrors.genericError'
      throw new Error(errorOrderSeason.value)
    } finally {
      isUpdatingOrderSeason.value = false
    }
  }
  // --- RETURN (Exportaciones del Store) ---
  return {
    // Lista de Usuarios
    userList,
    isLoadingUsers,
    errorUsers,
    fetchAllUsers,

    // Pagos Recientes
    recentPayments,
    isLoadingPayments,
    errorPayments,
    fetchRecentPayments,

    // Getters de Estadísticas
    getTotalUsers,
    getActiveMembers,
    getNewMembers30d,
    getPendingMembersCount,

    // Acciones de API
    approveUser,
    rejectUser,
    setUserStatus,
    setUserRole,
    forcePasswordReset,

    // Modal de Gestión (Editar)
    isManagementModalOpen,
    userToManage,
    openManagementModal,
    closeManagementModal,

    // Modal de Detalle (Ver)
    isDetailModalOpen,
    userDetail,
    isLoadingDetail,
    errorDetail,
    openDetailModal,
    closeDetailModal,

    allPaymentsList,
    isLoadingAllPayments,
    errorAllPayments,
    allSeasonsList,
    isLoadingSeasons,
    fetchAllPayments,
    fetchAllSeasons,
    isUpdatingSeason,
    errorSeason,
    createSeason,
    updateSeason,
    isPaymentDetailModalOpen,
    paymentDetail,
    isLoadingPaymentDetail,
    errorPaymentDetail,
    openPaymentDetailModal,
    closePaymentDetailModal,

    pendingReport,
    isLoadingPendingReport,
    errorPendingReport,
    fetchPendingReport,

    isManualPaymentModalOpen,
    cuotaToPayManually,
    isLoadingManualPayment,
    errorManualPayment,
    openManualPaymentModal,
    closeManualPaymentModal,
    registerManualPayment,

    prendasList,
    isLoadingPrendas,
    errorPrendas,
    fetchAllPrendas,
    isPrendaModalOpen,
    prendaToEdit,
    isLoadingPrendaModal,
    errorPrendaModal,
    openCreatePrendaModal,
    openEditPrendaModal,
    closePrendaModal,
    createPrenda,
    updatePrenda,
    deletePrenda,
    addPrendaVariante,
    deletePrendaVariante,
    allOrdersList,
    allOrderSeasonsList,
    isLoadingOrders,
    errorOrders,
    fetchAllOrders,
    fetchAllOrderSeasons,
    isOrderDetailModalOpen,
    orderDetail,
    isLoadingOrderDetail,
    errorOrderDetail,
    openOrderDetailModal,
    closeOrderDetailModal,
    markOrderAsPaid,
    cancelOrder,
    productionSummary,
    isLoadingSummary,
    fetchProductionSummary,

    isUpdatingOrderSeason,
    errorOrderSeason,
  
    createOrderSeason,
    updateOrderSeason
  }
})
