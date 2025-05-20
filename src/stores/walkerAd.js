import { defineStore } from 'pinia'
import { adsPost, adsGet, adsPut, adsDelete, adsPatch } from '../../api/api'

export const useWalkerAdStore = defineStore('walkerAd', {
  state: () => ({
    walkerAd: null,
    loading: false,
    error: null,
    success: null,
  }),
  actions: {
    async fetchWalkerAd() {
      this.loading = true
      this.error = null
      try {
        const response = await adsGet('')
        this.walkerAd = response.data
      } catch (error) {
        this.error = error.response?.data?.msg || 'Error al cargar el anuncio'
        console.error(this.error)
      } finally {
        this.loading = false
      }
    },
    async createWalkerAd(adData) {
      this.loading = true
      this.error = null
      this.success = null
      try {
        const response = await adsPost('', adData)
        this.walkerAd = response.data.advertisement
        this.success = response.data.msg || 'Anuncio creado exitosamente'
      } catch (error) {
        this.error = error.response?.data?.msg || 'Error al crear el anuncio'
        throw error
      } finally {
        this.loading = false
      }
    },
    async updateWalkerAd(adData) {
      this.loading = true
      this.error = null
      this.success = null
      try {
        const response = await adsPut('', adData)
        this.walkerAd = response.data.advertisement
        this.success = response.data.msg || 'Anuncio actualizado exitosamente'
      } catch (error) {
        this.error = error.response?.data?.msg || 'Error al actualizar el anuncio'
        throw error
      } finally {
        this.loading = false
      }
    },
    async deleteWalkerAd() {
      this.loading = true
      this.error = null
      this.success = null
      try {
        const response = await adsDelete('')
        this.walkerAd = null
        this.success = response.data.msg || 'Anuncio eliminado exitosamente'
      } catch (error) {
        this.error = error.response?.data?.msg || 'Error al eliminar el anuncio'
        throw error
      } finally {
        this.loading = false
      }
    },
    async togglePauseWalkerAd() {
      this.loading = true
      this.error = null
      this.success = null
      try {
        const response = await adsPatch('/pause', {})
        this.walkerAd = response.data.advertisement
        this.success =
          response.data.msg ||
          `Anuncio ${this.walkerAd.paused ? 'pausado' : 'activado'} exitosamente`
      } catch (error) {
        this.error = error.response?.data?.msg || 'Error al pausar/activar el anuncio'
        throw error
      } finally {
        this.loading = false
      }
    },
  },
})
