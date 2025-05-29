import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chatGet, chatPost } from '../../api/api'

export const useChatStore = defineStore('chat', {
  state: () => ({
    showChat: false,
    showConversations: false,
    messages: [],
    conversations: [],
    walkerId: null,
    walkerName: '',
    ownerId: null,
    loading: false,
    error: null,
    pollingInterval: null,
  }),
  actions: {
    async fetchConversations() {
      this.loading = true
      this.error = null
      try {
        const res = await chatGet('/conversations')
        this.conversations = res.data
      } catch (e) {
        this.error = e.response?.data?.msg || 'Error al cargar conversaciones'
      } finally {
        this.loading = false
      }
    },
    async openChat(userId, userName, ownerId = null) {
      this.showChat = true
      this.walkerId = userId
      this.walkerName = userName
      this.ownerId = ownerId
      await this.fetchMessages()
      this.startPolling()
    },
    async fetchMessages() {
      if (!this.walkerId) return
      this.loading = true
      this.error = null
      try {
        const res = await chatGet(`/messages/${this.walkerId}`)
        this.messages = res.data
      } catch (e) {
        this.error = e.response?.data?.msg || 'Error al cargar mensajes'
        this.messages = []
      } finally {
        this.loading = false
      }
    },
    async sendMessage(text) {
      if (!text.trim()) return
      try {
        const payload = {
          walkerId: this.walkerId,
          text,
        }
        if (this.ownerId) payload.ownerId = this.ownerId
        const res = await chatPost('/send', payload)
        this.messages.push(res.data.message)
        this.error = null
      } catch (e) {
        this.error = e.response?.data?.msg || 'Error al enviar mensaje'
      }
    },
    startPolling() {
      if (this.pollingInterval) clearInterval(this.pollingInterval)
      this.pollingInterval = setInterval(() => {
        this.fetchMessages()
      }, 5000)
    },
    stopPolling() {
      if (this.pollingInterval) {
        clearInterval(this.pollingInterval)
        this.pollingInterval = null
      }
    },
    closeChat() {
      this.showChat = false
      this.walkerId = null
      this.walkerName = ''
      this.ownerId = null
      this.messages = []
      this.error = null
      this.stopPolling()
    },
    receiveMessage(msg) {
      this.messages.push({
        text: msg,
        sent: false,
        id: Date.now(),
        timestamp: new Date().toISOString(),
      })
    },
  },
})
