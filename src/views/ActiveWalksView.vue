<template>
  <div>
    <header>
      <h1>Anuncios de Paseadores Activos</h1>
      <div class="nav-buttons">
        <button @click="goToProfile">Perfil</button>
        <button @click="goToHome">Inicio</button>
        <button @click="logout">Cerrar sesión</button>
      </div>
    </header>

    <div class="filters">
      <select v-model="selectedLocality" @change="fetchAds">
        <option value="">Todas las ciudades</option>
        <option v-for="locality in localities" :key="locality" :value="locality">
          {{ locality }}
        </option>
      </select>
      <button @click="resetFilters">Quitar filtros</button>
    </div>

    <div v-if="ads.length">
      <div v-for="ad in ads" :key="ad._id" class="ad-card">
        <p><strong>Biografía:</strong> {{ ad.biography }}</p>
        <p><strong>Máximo de perros por paseo:</strong> {{ ad.maxDogs }}</p>
        <p><strong>Localidad:</strong> {{ ad.locality }}</p>
        <button @click="openChat(ad.walker_id)">Contactar</button>
      </div>
    </div>
    <p v-else-if="loading">Cargando anuncios...</p>
    <p v-else>No hay anuncios activos disponibles.</p>

    <div v-if="showChat" class="chat-modal">
      <div class="chat-content">
        <h3>Chat con paseador</h3>
        <div class="messages">
          <p
            v-for="message in messages"
            :key="message.id"
            :class="{ sent: message.sent, received: !message.sent }"
          >
            {{ message.text }}
          </p>
        </div>
        <form @submit.prevent="sendMessage">
          <input v-model="newMessage" placeholder="Escribe un mensaje..." required />
          <button type="submit">Enviar</button>
        </form>
        <button @click="closeChat">Cerrar</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { adsGet } from '../../api/api'

const router = useRouter()
const authStore = useAuthStore()
const ads = ref([])
const localities = ref([])
const selectedLocality = ref('')
const loading = ref(false)
const showChat = ref(false)
const currentWalkerId = ref(null)
const messages = ref([])
const newMessage = ref('')

const fetchAds = async () => {
  loading.value = true
  try {
    const url = selectedLocality.value
      ? `/all?locality=${encodeURIComponent(selectedLocality.value)}`
      : '/all'
    const response = await adsGet(url)
    ads.value = response.data
    if (!localities.value.length) {
      const uniqueLocalities = [...new Set(response.data.map((ad) => ad.locality))].sort()
      localities.value = uniqueLocalities
    }
  } catch (error) {
    console.error('Error al cargar anuncios:', error.response?.data?.msg || error.message)
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  selectedLocality.value = ''
  fetchAds()
}

const openChat = (walkerId) => {
  currentWalkerId.value = walkerId
  messages.value = [] // Simula carga de mensajes (necesita endpoint)
  showChat.value = true
}

const closeChat = () => {
  showChat.value = false
  currentWalkerId.value = null
  newMessage.value = ''
}

const sendMessage = () => {
  if (newMessage.value.trim()) {
    messages.value.push({ id: Date.now(), text: newMessage.value, sent: true })
    // Simula respuesta (necesita endpoint)
    setTimeout(() => {
      messages.value.push({
        id: Date.now() + 1,
        text: '¡Hola! Gracias por contactarme.',
        sent: false,
      })
    }, 1000)
    newMessage.value = ''
  }
}

onMounted(async () => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else if (authStore.userRole !== 'owner') {
    router.push({ name: 'index' })
  } else {
    await fetchAds()
  }
})

const goToProfile = () => {
  router.push({ name: 'owner-profile' })
}

const goToHome = () => {
  router.push({ name: 'index' })
}

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'login' })
}
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}
select,
input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}
h1 {
  color: #333;
}
.nav-buttons {
  display: flex;
  gap: 10px;
}
button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  opacity: 0.9;
}
.nav-buttons button:nth-child(1) {
  background-color: #007bff;
  color: white;
}
.nav-buttons button:nth-child(2) {
  background-color: #6c757d;
  color: white;
}
.nav-buttons button:nth-child(3) {
  background-color: #dc3545;
  color: white;
}
.filters button,
.ad-card button {
  background-color: #28a745;
  color: white;
}
.ad-card {
  border: 1px solid #ccc;
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
}
p {
  margin: 5px 0;
}
.chat-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.chat-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 400px;
  max-height: 80%;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.messages {
  max-height: 300px;
  overflow-y: auto;
  border: 1px solid #ccc;
  padding: 10px;
}
.sent {
  text-align: right;
  color: #007bff;
}
.received {
  text-align: left;
  color: #333;
}
form {
  display: flex;
  gap: 10px;
}
form input {
  flex: 1;
}
</style>
