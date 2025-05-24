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
    } catch (err) {
      walkerAd.value = null
      error.value = err.response?.data?.msg || 'Error al cargar el anuncio'
      console.error('Error en fetchWalkerAd:', error.value)
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
      success.value = response.data.msg
      await fetchWalkerAd()
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al crear el anuncio'
      console.error('Error en createWalkerAd:', error.value)
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
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al actualizar el anuncio'
      console.error('Error en updateWalkerAd:', error.value)
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
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al pausar/activar el anuncio'
      console.error('Error en togglePauseWalkerAd:', error.value)
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
    } catch (err) {
      error.value = err.response?.data?.msg || 'Error al eliminar el anuncio'
      console.error('Error en deleteWalkerAd:', error.value)
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
