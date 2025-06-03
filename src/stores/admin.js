import { defineStore } from 'pinia'
import { ref } from 'vue'
import { adminGet, adminPost, adminPut, adminDelete } from '../../api/api'

export const useAdminStore = defineStore('admin', () => {
  const users = ref([])
  const selectedUser = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const success = ref(null)

  const fetchAllUsers = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await adminGet('')
      users.value = response.data
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al cargar usuarios'
      console.error('Error en fetchAllUsers:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchUserDetails = async (userId) => {
    loading.value = true
    error.value = null
    selectedUser.value = null
    try {
      const response = await adminGet(`/${userId}`)
      selectedUser.value = response.data
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al cargar detalles del usuario'
      console.error('Error en fetchUserDetails:', err)
    } finally {
      loading.value = false
    }
  }

  const createUser = async (userData) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminPost('', userData)
      success.value = response.data.msg
      await fetchAllUsers()
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al crear usuario'
      console.error('Error en createUser:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateUser = async (userId, userData) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminPut(`/${userId}`, userData)
      success.value = response.data.msg
      await fetchAllUsers()
      if (selectedUser.value && selectedUser.value.user._id === userId) {
        await fetchUserDetails(userId)
      }
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al actualizar usuario'
      console.error('Error en updateUser:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteUser = async (userId) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminDelete(`/${userId}`)
      success.value = response.data.msg
      await fetchAllUsers()
      if (selectedUser.value && selectedUser.value.user._id === userId) {
        selectedUser.value = null
      }
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al eliminar usuario'
      console.error('Error en deleteUser:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteAdAsAdmin = async (adId) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminDelete(`/advertisements/${adId}`)
      success.value = response.data.msg
      if (selectedUser.value) await fetchUserDetails(selectedUser.value.user._id)
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al eliminar anuncio'
      console.error('Error en deleteAdAsAdmin:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateAdAsAdmin = async (adId, adData) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminPut(`/advertisements/${adId}`, adData)
      success.value = response.data.msg
      if (selectedUser.value) await fetchUserDetails(selectedUser.value.user._id)
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al actualizar anuncio'
      console.error('Error en updateAdAsAdmin:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteDogAsAdmin = async (dogId) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminDelete(`/dogs/${dogId}`)
      success.value = response.data.msg
      if (selectedUser.value) await fetchUserDetails(selectedUser.value.user._id)
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al eliminar perro'
      console.error('Error en deleteDogAsAdmin:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateDogAsAdmin = async (dogId, dogData) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminPut(`/dogs/${dogId}`, dogData)
      success.value = response.data.msg
      if (selectedUser.value) await fetchUserDetails(selectedUser.value.user._id)
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al actualizar perro'
      console.error('Error en updateDogAsAdmin:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const deleteRequestAsAdmin = async (requestId) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminDelete(`/requests/${requestId}`)
      success.value = response.data.msg
      if (selectedUser.value) await fetchUserDetails(selectedUser.value.user._id)
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al eliminar solicitud'
      console.error('Error en deleteRequestAsAdmin:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateRequestAsAdmin = async (requestId, requestData) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adminPut(`/requests/${requestId}`, requestData)
      success.value = response.data.msg
      if (selectedUser.value) await fetchUserDetails(selectedUser.value.user._id)
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al actualizar solicitud'
      console.error('Error en updateRequestAsAdmin:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    users,
    selectedUser,
    loading,
    error,
    success,
    fetchAllUsers,
    fetchUserDetails,
    createUser,
    updateUser,
    deleteUser,
    deleteAdAsAdmin,
    updateAdAsAdmin,
    deleteDogAsAdmin,
    updateDogAsAdmin,
    deleteRequestAsAdmin,
    updateRequestAsAdmin,
  }
})
