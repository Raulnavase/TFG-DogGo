import { defineStore } from 'pinia'
import { authPost, dogsPost, dogsGet, dogsPut, dogsDelete, authDelete } from '../../api/api'

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
        console.log('Cuenta eliminada correctamente')
      } catch (error) {
        console.error('Error al eliminar la cuenta:', error)
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
      this.showEditDogForm = false
      this.editDog = { _id: '', name: '', breed: '', age: '' }
      this.editDogError = null
      this.editDogSuccess = null
      this.showDeleteConfirm = false
      this.dogToDelete = null
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
        } else {
          this.editDogError = response.data.msg || 'Error al actualizar el perro.'
        }
      } catch (error) {
        this.editDogError = error.response?.data?.msg || 'Error de conexión al servidor.'
        console.error('Error al actualizar perro:', error)
      }
    },

    showDeleteConfirmation(dog) {
      this.showDeleteConfirm = true
      this.dogToDelete = dog
    },

    async deleteDog() {
      if (!this.dogToDelete) return
      this.addDogError = null
      this.addDogSuccess = null
      try {
        const response = await dogsDelete(`/${this.dogToDelete._id}`)
        if (response.status === 200) {
          this.dogs = this.dogs.filter((d) => d._id !== this.dogToDelete._id)
          this.addDogSuccess = 'Perro eliminado exitosamente.'
          this.showDeleteConfirm = false
          this.dogToDelete = null
        } else {
          this.addDogError = response.data.msg || 'Error al eliminar el perro.'
        }
      } catch (error) {
        this.addDogError = error.response?.data?.msg || 'Error de conexión al servidor.'
        console.error('Error al eliminar perro:', error)
      }
    },

    cancelDelete() {
      this.showDeleteConfirm = false
      this.dogToDelete = null
    },
  },

  getters: {
    isLoggedIn: (state) => state.isAuthenticated,
    userRole: (state) => state.role,
    userName: (state) => state.user?.name || '',
  },
})
