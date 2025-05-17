import { defineStore } from 'pinia'
import { authPost, dogsPost, dogsGet } from '../../api/api'

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
    showAddDogForm: false,
    newDog: {
      name: '',
      breed: '',
      age: '',
    },
    addDogError: null,
    addDogSuccess: null,
    dogs: [],
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
        const response = await authPost('/register', userData)
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
        const response = await authPost('/login', credentials)
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
        await authPost('/logout', {})
        console.log('Cierre de sesión exitoso desde el backend')
      } catch (error) {
        console.error('Error al cerrar sesión en el backend:', error)
      }
      this.isAuthenticated = false
      this.role = null
      this.user = null
      this.dogs = []
      this.showAddDogForm = false
      this.newDog = { name: '', breed: '', age: '' }
      this.addDogError = null
      this.addDogSuccess = null
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')
      localStorage.removeItem('user')
      console.log('Usuario ha cerrado sesión')
    },

    toggleAddDogForm() {
      this.showAddDogForm = !this.showAddDogForm
      this.newDog = { name: '', breed: '', age: '' }
      this.addDogError = null
      this.addDogSuccess = null
    },

    async addDog() {
      this.addDogError = null
      this.addDogSuccess = null
      try {
        const dogData = {
          ...this.newDog,
          age: Number(this.newDog.age),
        }
        const response = await dogsPost('', dogData)
        if (response.status === 201) {
          this.addDogSuccess = response.data.msg || 'Perro agregado exitosamente.'
          this.showAddDogForm = false
          await this.fetchDogs()
        } else {
          this.addDogError = response.data.msg || 'Error al agregar el perro.'
        }
      } catch (error) {
        this.addDogError = error.response?.data?.msg || 'Error de conexión al servidor.'
        console.error('Error al agregar perro:', error)
      }
    },

    async fetchDogs() {
      this.addDogError = null
      this.addDogSuccess = null
      try {
        const response = await dogsGet('')
        if (response.status === 200) {
          this.dogs = response.data
        } else {
          this.addDogError = response.data.msg || 'Error al obtener los perros.'
          console.error('Error al obtener la lista de perros:', response.data.msg)
        }
      } catch (error) {
        this.addDogError = error.response?.data?.msg || 'Error al conectar con el servidor.'
        console.error('Error al conectar con el servidor para obtener los perros:', error)
      }
    },
  },

  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    userRole: (state) => state.role,
    userName: (state) => state.user?.name || '',
  },
})
