<template>
  <div class="chat-modal">
    <div class="chat-content">
      <h3>Tus conversaciones</h3>
      <ul>
        <li v-for="conv in chatStore.conversations" :key="conv.id">
          <button @click="open(conv)">
            {{ conv.name }}
          </button>
        </li>
      </ul>
      <button @click="$emit('close')">Cerrar</button>
      <p v-if="chatStore.error" class="error-message">{{ chatStore.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { useChatStore } from '@/stores/messages'
const chatStore = useChatStore()

const open = (conv) => {
  chatStore.openChat(conv.id, conv.name, conv.id)
  chatStore.showConversations = false
}
</script>
