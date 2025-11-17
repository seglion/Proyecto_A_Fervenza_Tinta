import { defineStore } from 'pinia'
import { ref } from 'vue'
import apiClient from '@/api/axios'

export const useCuotasStore = defineStore('cuotas', () => {
  // --- STATE ---
  const cuotaActiva = ref(null)
  const isLoading = ref(false)
  const error = ref(null)
 

  const historialPagos = ref([])
  const isLoadingHistorial = ref(false)
  const errorHistorial = ref(null)
  // --- ACTIONS ---
  
  /**
   * Obtiene la cuota activa del usuario desde la API.
   */
  async function fetchCuotaActiva() {
    isLoading.value = true
    error.value = null
    try {
      const response = await apiClient.get('/cuotas/mi-cuota-activa')
      cuotaActiva.value = response.data
    } catch (e) {
      console.error('Error fetching active fee:', e)
      // Usamos la clave de error de la API
      error.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoading.value = false
    }
  }

  /**
   * Llama a la API para crear un intento de pago y redirige a Stripe.
   */
  async function createPaymentIntent() {
    isLoading.value = true // Reusamos isLoading para el botón
    error.value = null
    try {
      // 1. Llamar a la API
      const response = await apiClient.post('/cuotas/crear-intento-pago')
      
      // 2. Obtener la URL de Stripe (asumiendo que la API la devuelve así)
      const redirectUrl = response.data.url_pago 
      
      if (!redirectUrl) {
        throw new Error('apiErrors.paymentLinkError')
      }
      
      // 3. Redirigir al usuario a Stripe
      window.location.href = redirectUrl

    } catch (e) {
      console.error('Error creating payment intent:', e)
      error.value = e.response?.data?.detail || 'apiErrors.paymentLinkError'
    } finally {
      // No ponemos isLoading a false porque la página va a redirigir
    }
  }

  async function fetchHistorialPagos() {
    if (historialPagos.value.length > 0) return // No recargar

    isLoadingHistorial.value = true
    errorHistorial.value = null
    try {
      const response = await apiClient.get('/cuotas/historial')
      // El DTO devuelve { historial: [...] }
      historialPagos.value = response.data.historial
    } catch (e) {
      console.error('Error fetching payment history:', e)
      errorHistorial.value = e.response?.data?.detail || 'apiErrors.genericError'
    } finally {
      isLoadingHistorial.value = false
    }
  }

  return { cuotaActiva, 
    isLoading,
     error, 
     fetchCuotaActiva,
      createPaymentIntent,
    historialPagos,
    isLoadingHistorial,
    errorHistorial,
    fetchHistorialPagos }
})