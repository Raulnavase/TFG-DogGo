import { defineStore } from 'pinia'
import { ref } from 'vue'
import { adsGet, adsPost, adsPut, adsPatch, adsDelete } from '../../api/api'

export const useWalkerAdStore = defineStore('walkerAd', () => {
  const walkerAd = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const success = ref(null)

  const fetchWalkerAd = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await adsGet('/walker')
      walkerAd.value = response.data
      console.log('Anuncio cargado en store:', walkerAd.value)
      return true
    } catch (err) {
      walkerAd.value = null
      const msg = err.response?.data?.msg || 'Error al cargar el anuncio'
      if (msg.toLowerCase().includes('no tienes un anuncio')) {
        error.value = null
      } else {
        error.value = msg
        console.error('Error en fetchWalkerAd:', error.value)
      }
      return false
    } finally {
      loading.value = false
    }
  }

  const createWalkerAd = async (adData) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adsPost('/create', adData)
      if (response.status === 201) {
        success.value = response.data?.msg || 'Anuncio creado correctamente'
        await fetchWalkerAd()
        return true
      } else {
        error.value = 'No se pudo crear el anuncio'
        return false
      }
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al crear el anuncio'
      console.error('Error en createWalkerAd:', error.value)
      return false
    } finally {
      loading.value = false
    }
  }

  const updateWalkerAd = async (adData) => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adsPut('/update', adData)
      success.value = response.data.msg
      await fetchWalkerAd()
      return true
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al actualizar el anuncio'
      console.error('Error en updateWalkerAd:', error.value)
      return false
    } finally {
      loading.value = false
    }
  }

  const togglePauseWalkerAd = async () => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adsPatch('/toggle-pause')
      success.value = response.data.msg
      await fetchWalkerAd()
      return true
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al pausar/activar el anuncio'
      console.error('Error en togglePauseWalkerAd:', error.value)
      return false
    } finally {
      loading.value = false
    }
  }

  const deleteWalkerAd = async () => {
    loading.value = true
    error.value = null
    success.value = null
    try {
      const response = await adsDelete('/delete')
      success.value = response.data.msg
      walkerAd.value = null
      return true
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al eliminar el anuncio'
      console.error('Error en deleteWalkerAd:', error.value)
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    walkerAd,
    loading,
    error,
    success,
    fetchWalkerAd,
    createWalkerAd,
    updateWalkerAd,
    togglePauseWalkerAd,
    deleteWalkerAd,
  }
})
