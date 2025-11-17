import axios from 'axios'
import router from '@/router'

// Lee la URL base del .env
const baseURL = import.meta.env.VITE_API_BASE_URL

const apiClient = axios.create({
  baseURL: baseURL,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
})

// === INTERCEPTOR DE PETICIÓN (Request) ===

apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwt_token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// === INTERCEPTOR DE RESPUESTA (Response) ===

apiClient.interceptors.response.use(
  (response) => {

    return response
  },
  async (error) => {
    const originalRequest = error.config


    if (error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true // Marcamos la petición para no entrar en un bucle infinito

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (!refreshToken) {
          throw new Error('No hay refresh token')
        }

        // --- 1. Preparamos el body para el refresh ---

        const body = {
          refresh_token: refreshToken
        }

        // --- 2. Pedimos los nuevos tokens ---
        // Usamos 'axios.post' (el global) 
        // Usamos el endpoint que especificaste: /users/auth/refresh
        const res = await axios.post(`${baseURL}/users/auth/refresh`, body, {
          headers: {
            'Content-Type': 'application/json' // Como pide tu API
          }
        })

        // --- 3. Guardamos los nuevos tokens ---

        const newAccessToken = res.data.access_token
        const newRefreshToken = res.data.refresh_token

        localStorage.setItem('jwt_token', newAccessToken)
        localStorage.setItem('refresh_token', newRefreshToken)

        // --- 4. Actualizamos el header de la petición original ---
        originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`

        // --- 5. Reintentamos la petición original ---
        return apiClient(originalRequest)

      } catch (refreshError) {
        // --- El REFRESH_TOKEN falló (también expiró o es inválido) ---
        // Limpiamos todo y mandamos al login.
        console.error('No se pudo refrescar el token:', refreshError)
        localStorage.removeItem('jwt_token')
        localStorage.removeItem('refresh_token')
        
        router.push({ name: 'login' }).catch(() => {})
        
        return Promise.reject(refreshError)
      }
    }

    // Si el error no es 401, simplemente lo devolvemos.
    return Promise.reject(error)
  }
)

export default apiClient