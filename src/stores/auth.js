import { defineStore } from 'pinia'
import {
  authPost,
  dogsPost,
  dogsGet,
  dogsPut,
  dogsDelete,
  authDelete,
  authGet,
} from '../../api/api'

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
    newDog: { name: '', breed: '', age: '' },
    addDogError: null,
    addDogSuccess: null,
    dogs: [],
    showEditDogForm: false,
    editDog: { _id: '', name: '', breed: '', age: '' },
    editDogError: null,
    editDogSuccess: null,
    showDeleteConfirm: false,
    dogToDelete: null,
  }),

  actions: {
    async initializeAuth() {
      const token = localStorage.getItem('accessToken')
      if (token) {
        try {
          const response = await authGet('/current_user')
          this.isAuthenticated = true
          this.role = response.data.role
          this.user = {
            id: response.data.id,
            name: response.data.name,
            last_name: response.data.last_name,
            email: response.data.email,
          }
          localStorage.setItem('userRole', this.role)
          localStorage.setItem('user', JSON.stringify(this.user))
        } catch (error) {
          console.error('Error al inicializar autenticación:', error)
          this.logoutUser()
        }
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
      } catch (error) {
        this.registrationError = error.response?.data?.msg || 'Error al registrar el usuario'
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
        this.user = {
          id: response.data.id,
          name: response.data.name,
          last_name: response.data.last_name,
          email: response.data.email,
        }
        localStorage.setItem('accessToken', response.data.access_token)
        localStorage.setItem('userRole', response.data.role)
        localStorage.setItem('user', JSON.stringify(this.user))
        return true
      } catch (error) {
        this.loginError = error.response?.data?.msg || 'Credenciales inválidas o error de conexión.'
        this.isAuthenticated = false
        this.role = null
        this.user = null
        localStorage.removeItem('accessToken')
        localStorage.removeItem('userRole')
        localStorage.removeItem('user')
        return false
      } finally {
        this.isLoggingIn = false
      }
    },

    async updatePersonalData(data) {
      try {
        const response = await authPost('/update', data)
        if (response.status === 200) {
          this.user = { ...this.user, ...data }
          localStorage.setItem('user', JSON.stringify(this.user))
        } else {
          throw new Error(response.data.msg || 'Error al actualizar datos')
        }
      } catch (error) {
        throw error
      }
    },

    async changePassword({ oldPassword, newPassword }) {
      try {
        const response = await authPost('/change-password', { oldPassword, newPassword })
        if (response.status !== 200) {
          throw new Error(response.data.msg || 'Error al cambiar la contraseña')
        }
      } catch (error) {
        throw error
      }
    },

    async deleteUserAccount() {
      try {
        await authDelete('/user')
        this.isAuthenticated = false
        this.role = null
        this.user = null
        this.dogs = []
        this.showAddDogForm = false
        this.newDog = { name: '', breed: '', age: '' }
        this.addDogError = null
        this.addDogSuccess = null
        this.showEditDogForm = false
        this.editDog = { _id: '', name: '', breed: '', age: '' }
        this.editDogError = null
        this.editDogSuccess = null
        this.showDeleteConfirm = false
        this.dogToDelete = null
        localStorage.removeItem('accessToken')
        localStorage.removeItem('userRole')
        localStorage.removeItem('user')
      } catch (error) {
        throw error
      }
    },

    cancelDelete() {
      this.showDeleteConfirm = false
      this.dogToDelete = null
    },

    async logoutUser() {
      try {
        await authPost('/logout', {})
      } catch (error) {
        console.warn('Error during logout, but proceeding with client-side cleanup:', error)
      }
      this.isAuthenticated = false
      this.role = null
      this.user = null
      this.dogs = []
      this.showAddDogForm = false
      this.newDog = { name: '', breed: '', age: '' }
      this.addDogError = null
      this.addDogSuccess = null
      this.showEditDogForm = false
      this.editDog = { _id: '', name: '', breed: '', age: '' }
      this.editDogError = null
      this.editDogSuccess = null
      this.showDeleteConfirm = false
      this.dogToDelete = null
      localStorage.removeItem('accessToken')
      localStorage.removeItem('userRole')
      localStorage.removeItem('user')
    },

    toggleAddDogForm() {
      this.showAddDogForm = !this.showAddDogForm
      this.newDog = { name: '', breed: '', age: '' }
      this.addDogError = null
      this.addDogSuccess = null
      this.showEditDogForm = false
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
          this.dogs.push(response.data.dog)
          this.showAddDogForm = false
          this.newDog = { name: '', breed: '', age: '' }
          return true
        } else {
          this.addDogError = response.data.msg || 'Error al agregar el perro.'
          return false
        }
      } catch (error) {
        this.addDogError = error.response?.data?.msg || 'Error de conexión al servidor.'
        return false
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
        }
      } catch (error) {
        this.addDogError = error.response?.data?.msg || 'Error al conectar con el servidor.'
      }
    },

    toggleEditDogForm(dog) {
      this.showEditDogForm = !this.showEditDogForm
      if (dog) {
        this.editDog = { ...dog, age: dog.age.toString() }
        this.showAddDogForm = false
      } else {
        this.editDog = { _id: '', name: '', breed: '', age: '' }
        this.editDogError = null
        this.editDogSuccess = null
      }
    },

    async updateDog() {
      this.editDogError = null
      this.editDogSuccess = null
      try {
        const dogData = {
          name: this.editDog.name,
          breed: this.editDog.breed,
          age: Number(this.editDog.age),
        }
        const response = await dogsPut(`/${this.editDog._id}`, dogData)
        if (response.status === 200) {
          this.editDogSuccess = response.data.msg || 'Perro actualizado exitosamente.'
          this.dogs = this.dogs.map((d) => (d._id === this.editDog._id ? { ...d, ...dogData } : d))
          this.showEditDogForm = false
          this.editDog = { _id: '', name: '', breed: '', age: '' }
          return true
        } else {
          this.editDogError = response.data.msg || 'Error al actualizar el perro.'
          return false
        }
      } catch (error) {
        this.editDogError = error.response?.data?.msg || 'Error de conexión al servidor.'
        return false
      }
    },

    showDeleteConfirmation(dog) {
      this.showDeleteConfirm = true
      this.dogToDelete = dog
    },

    async deleteDog() {
      if (!this.dogToDelete) return false

      this.addDogError = null
      this.addDogSuccess = null
      try {
        const response = await dogsDelete(`/${this.dogToDelete._id}`)
        if (response.status === 200) {
          this.dogs = this.dogs.filter((d) => d._id !== this.dogToDelete._id)
          this.addDogSuccess = 'Perro eliminado exitosamente.'
          this.showDeleteConfirm = false
          this.dogToDelete = null
          return true
        } else {
          this.addDogError = response.data.msg || 'Error al eliminar el perro.'
          return false
        }
      } catch (error) {
        this.addDogError = error.response?.data?.msg || 'Error de conexión al servidor.'
        return false
      }
    },
  },

  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    userRole: (state) => state.role,
    userName: (state) => state.user?.name || '',
    userLastName: (state) => state.user?.last_name || '',
    userEmail: (state) => state.user?.email || '',
    userId: (state) => state.user?.id || null,
  },
})
