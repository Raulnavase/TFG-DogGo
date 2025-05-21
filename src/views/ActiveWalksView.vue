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
    <div v-if="ads.length">
      <div v-for="ad in ads" :key="ad._id" class="ad-card">
        <p><strong>Biografía:</strong> {{ ad.biography }}</p>
        <p><strong>Máximo de perros por paseo:</strong> {{ ad.maxDogs }}</p>
        <p><strong>Localidad:</strong> {{ ad.locality }}</p>
      </div>
    </div>
    <p v-else-if="loading">Cargando anuncios...</p>
    <p v-else>No hay anuncios activos disponibles.</p>
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
const loading = ref(false)

onMounted(async () => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else if (authStore.userRole !== 'owner') {
    router.push({ name: 'index' })
  } else {
    loading.value = true
    try {
      const response = await adsGet('/all')
      ads.value = response.data
    } catch (error) {
      console.error('Error al cargar anuncios:', error.response?.data?.msg || error.message)
    } finally {
      loading.value = false
    }
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
button:nth-child(1) {
  background-color: #007bff;
  color: white;
}
button:nth-child(2) {
  background-color: #6c757d;
  color: white;
}
button:nth-child(3) {
  background-color: #dc3545;
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
</style>
