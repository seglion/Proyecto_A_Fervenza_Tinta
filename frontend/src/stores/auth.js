import { defineStore } from 'pinia'
import apiClient from '@/api/axios'
import { Role } from '@/constants/roles'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('jwt_token') || null,
    user: null,
    authStatus: 'unauthenticated',
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    getUserProfile: (state) => state.user,
  },

  // Todo debe estar DENTRO de este bloque 'actions'
  actions: {
    /**
     * Acción de Login
     */
    async login(email, password) {
      const data = new URLSearchParams()
      data.append('grant_type', 'password')
      data.append('username', email)
      data.append('password', password)
      data.append('scope', '')
      data.append('client_id', 'string')
      data.append('client_secret', '********')
      const config = { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }

      try {
        const response = await apiClient.post('/users/auth/token', data, config)
        const token = response.data.access_token
        const refresh_token = response.data.refresh_token

        this.token = token
        localStorage.setItem('jwt_token', token)
        localStorage.setItem('refresh_token', refresh_token)

        await this.fetchProfile()

        const router = (await import('@/router')).default
        router.push({ name: 'dashboard' })
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 'apiErrors.invalidCredentials'
        throw new Error(errorMsg)
      }
    },
async resendVerificationEmail(email) {
      try {
        // Llama al endpoint que nos mostraste
        await apiClient.post('/users/reenviar-verificacion', { email: email })
        // La API (como vimos) siempre devuelve éxito
        
      } catch (error) {
        // Aunque el backend lo oculte, capturamos si algo falla (ej. 500)
        console.error('Error resending verification:', error)
        const errorMsg = error.response?.data?.detail || 'apiErrors.genericError'
        throw new Error(errorMsg)
      }
    },
    /**
     * Carga el perfil del usuario
     */
    async fetchProfile() {
      if (!this.token) return
      try {
        const response = await apiClient.get('/users/me')
        this.user = response.data 
        if (response.data.esta_activo) {
          this.authStatus = 'authenticated'
        } else {
          this.authStatus = 'pendingAdminApproval'
        }
      } catch (error) {
        console.error('Error cargando el perfil:', error)
        if (error.response?.status === 401) {
          this.logout()
        }
      }
    },

    /**
     * Cierra la sesión
     */
    async logout() {
      this.token = null
      this.user = null
      this.authStatus = 'unauthenticated'
      localStorage.removeItem('jwt_token')
      localStorage.removeItem('refresh_token')

      // Importación dinámica ASÍNCRONA (await) - Esto arregla el crash
      const router = (await import('@/router')).default 
      router.push({ name: 'home' })
    },

    /**
     * Registro de Usuario
     */
    async register(values) {
      const apiData = {
        email: values.email,
        contrasena: values.password,
        nombre: values.nombre,
        apellidos: values.apellidos,
        numero_telefono: values.phone,
        apodo: values.nickname || null,
        rol: Role.USER 
      }
      const config = { headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' } }

      try {
        const response = await apiClient.post('/users/register', apiData, config)
        console.log('Respuesta de la API de Registro:', response.data)
        this.authStatus = 'pendingEmailVerification'
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 'apiErrors.genericError'
        throw new Error(errorMsg)
      }
    },

    /**
     * Verificación de Email
     */
    async verifyEmail(token) {
      try {
        await apiClient.get('/users/verificar-email', {
          params: { token: token }
        })
        this.authStatus = 'pendingAdminApproval'
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 'apiErrors.invalidToken'
        throw new Error(errorMsg)
      }
    },

    /**
     * Solicitar Reseteo de Contraseña
     */
    async requestPasswordReset(email) {
      try {
        await apiClient.post('/users/solicitar-reseteo', { email: email })
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 'apiErrors.genericError'
        throw new Error(errorMsg)
      }
    },

    /**
     * Confirmar Reseteo de Contraseña
     */
    async resetPassword(token, newPassword) {
      try {
        await apiClient.post('/users/confirmar-reseteo', {
          token: token,
          nueva_contrasena: newPassword
        })
      } catch (error) {
        const errorMsg = error.response?.data?.detail || 'apiErrors.invalidToken'
        throw new Error(errorMsg)
      }
    },

    /**
     * Actualizar Perfil
     */
    async updateProfile(profileData) {

      try {
        const response = await apiClient.put('/users/me', profileData)
        
        
        // Esta es la línea que "guarda"
        this.user = response.data 

      } catch (error) {
        
        // Imprime el error real que viene del backend
     
        
        throw new Error(error.response?.data?.detail || 'apiErrors.genericError')
      }
    },

    /**
     * Cambiar Contraseña
     */
    async changePassword(passwordData) {
      const apiData = {
        contrasena_antigua: passwordData.oldPassword,
        contrasena_nueva: passwordData.newPassword
      }
      try {
        await apiClient.put('/users/me/password', apiData)
      } catch (error) {
        console.error('Error changing password:', error)
        throw new Error(error.response?.data?.detail || 'apiErrors.genericError')
      }
    }
    
  }, // <-- El bloque 'actions' termina aquí

  persist: {
    paths: ['user', 'authStatus'],
  },

})