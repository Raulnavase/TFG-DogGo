import { defineStore } from 'pinia'
import { post } from '../../api/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    registrationError: null,
    isRegistering: false,
    registrationSuccess: false,
    loginError: null,
    isLoggingIn: false,
    user: JSON.parse(localStorage.getItem('user')) || null,
    isAuthenticated: localStorage.getItem('accessToken') ? true : false,
    role: localStorage.getItem('userRole') || null,
  }),

  actions: {
    initializeAuth() {
      const token = localStorage.getItem('accessToken')
      const role = localStorage.getItem('userRole')
      const user = localStorage.getItem('user')
      if (token && role && user) {
        this.isAuthenticated = true
        this.role = role
        this.user = JSON.parse(user)
      } else {
        this.logoutUser()
      }
    },

    async registerUser(userData) {
      this.isRegistering = true
      this.registrationError = null
      this.registrationSuccess = false
      try {
        const response = await post('/register', userData)
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

    async loginUser(credentials) {
      this.isLoggingIn = true
      this.loginError = null
      try {
        const response = await post('/login', credentials)
        this.isAuthenticated = true
        this.role = response.data.role
        this.user = { name: response.data.name }
        localStorage.setItem('accessToken', response.data.access_token)
        localStorage.setItem('userRole', response.data.role)
        localStorage.setItem('user', JSON.stringify(this.user))
        console.log('Inicio de sesión exitoso:', response.data)
        return true
      } catch (error) {
        this.loginError = error.response?.data?.msg || 'Credenciales inválidas'
        this.isAuthenticated = false
        this.role = null
        this.user = null
        localStorage.removeItem('accessToken')
        localStorage.removeItem('userRole')
        localStorage.removeItem('user')
        console.error('Error al iniciar sesión:', error)
        throw error
      } finally {
        this.isLoggingIn = false
      }
    },

    async logoutUser() {
      try {
        await post('/logout', {})
        console.log('Cierre de sesión exitoso desde el backend')
      } catch (error) {
        console.error('Error al cerrar sesión en el backend:', error)
      }
      this.isAuthenticated = false
      this.role = null
      this.user = null
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')
      localStorage.removeItem('user')
      console.log('Usuario ha cerrado sesión')
    },
  },

  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    userRole: (state) => state.role,
    userName: (state) => state.user?.name || '',
  },
})
