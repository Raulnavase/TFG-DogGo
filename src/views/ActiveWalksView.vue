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
        <option value="">Todas las provincias</option>
        <optgroup v-for="comunidad in comunidades" :key="comunidad" :label="comunidad">
          <option
            v-for="provincia in provinciasPorComunidad[comunidad]"
            :key="provincia"
            :value="provincia"
          >
            {{ provincia }}
          </option>
        </optgroup>
      </select>
      <button @click="resetFilters">Quitar filtros</button>
    </div>

    <div v-if="ads.length">
      <div v-for="ad in ads" :key="ad._id" class="ad-card">
        <p>{{ capitalize(ad.walker_name) }} {{ capitalize(ad.walker_lastName) }}</p>
        <p>{{ ad.biography }}</p>
        <p>{{ ad.maxDogs }}</p>
        <p>{{ ad.locality }}</p>
        <p>{{ ad.walker_email }}</p>
        <button>Contactar</button>
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
import provinces from '@/data/provinces.json'

const capitalize = (str) => (str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : '')

const comunidades = Object.keys(provinces)
const provinciasPorComunidad = provinces

const router = useRouter()
const authStore = useAuthStore()
const ads = ref([])
const selectedLocality = ref('')
const loading = ref(false)

const fetchAds = async () => {
  loading.value = true
  try {
    const url = selectedLocality.value
      ? `/all?locality=${encodeURIComponent(selectedLocality.value)}`
      : '/all'
    const response = await adsGet(url)
    ads.value = response.data
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

.contact-btn {
  display: inline-block;
  padding: 8px 16px;
  background-color: #28a745;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  border: none;
  cursor: pointer;
  text-align: center;
}
.contact-btn:hover {
  opacity: 0.9;
}
</style>
