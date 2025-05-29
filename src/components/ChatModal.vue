<template>
  <div v-if="chatStore.showChat" class="chat-modal">
    <div class="chat-content">
      <h3>Chat con {{ chatStore.walkerName }}</h3>
      <div class="messages">
        <p
          v-for="message in chatStore.messages"
          :key="message.id"
          :class="{ sent: message.sent, received: !message.sent }"
        >
          {{ message.text }}
        </p>
      </div>
      <form @submit.prevent="send">
        <input v-model="newMessage" placeholder="Escribe un mensaje..." required />
        <button type="submit">Enviar</button>
      </form>
      <button @click="chatStore.closeChat">Cerrar</button>
      <p v-if="chatStore.error" class="error-message">{{ chatStore.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useChatStore } from '@/stores/messages'
const chatStore = useChatStore()
const newMessage = ref('')

const send = () => {
  chatStore.sendMessage(newMessage.value)
  newMessage.value = ''
}
</script>
