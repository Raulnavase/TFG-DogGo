import { defineStore } from 'pinia'
import api from '../../api/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    registrationError: null,
    isRegistering: false,
    registrationSuccess: false,
  }),

  actions: {
    async registerUser(userData) {
      this.isRegistering = true
      this.registrationError = null
      this.registrationSuccess = false
      try {
        const response = await api.post('/register', userData)
        this.registrationSuccess = true
        console.log('Registro exitoso:', response.data)
      } catch (error) {
        this.registrationError = error.response?.data?.msg || 'Error al registrar el usuario'
        console.error('Error de registro:', error)
        throw error
      } finally {
        this.isRegistering = false
      }
    },
  },
})
