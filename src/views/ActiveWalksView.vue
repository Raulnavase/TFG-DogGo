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
        <button @click="openRequestPanel(ad)">Solicitar servicio</button>
      </div>
    </div>
    <p v-else-if="loading">Cargando anuncios...</p>
    <p v-else>No hay anuncios activos disponibles.</p>

    <div v-if="showRequestPanel" class="modal-overlay">
      <div class="modal-content">
        <h2>Solicitar Paseo</h2>
        <form @submit.prevent="submitRequest">
          <div>
            <label>Día:</label>
            <input type="date" v-model="requestDate" required />
          </div>
          <div>
            <label>Localidad:</label>
            <input type="text" :value="selectedAd.locality" disabled />
          </div>
          <div>
            <label>Perros:</label>
            <div v-if="authStore.dogs.length">
              <div v-for="dog in authStore.dogs" :key="dog._id">
                <input type="checkbox" :id="dog._id" :value="dog._id" v-model="selectedDogs" />
                <label :for="dog._id"
                  >{{ capitalize(dog.name) }} ({{ capitalize(dog.breed) }})</label
                >
              </div>
            </div>
            <div v-else>
              <p>No tienes perros registrados. <br />No puedes solicitar el servicio.</p>
            </div>
          </div>
          <button type="submit" :disabled="!authStore.dogs.length || !selectedDogs.length">
            Enviar solicitud
          </button>
          <button type="button" @click="closeRequestPanel">Cancelar</button>
          <p v-if="requestError" class="error-message">{{ requestError }}</p>
          <p v-if="requestSuccess" class="success-message">{{ requestSuccess }}</p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { adsGet } from '../../api/api'
import provinces from '@/data/provinces.json'
import { requestsPost } from '../../api/api'

const capitalize = (str) => (str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : '')

const comunidades = Object.keys(provinces)
const provinciasPorComunidad = provinces

const router = useRouter()
const authStore = useAuthStore()
const ads = ref([])
const selectedLocality = ref('')
const loading = ref(false)

const showRequestPanel = ref(false)
const selectedAd = ref(null)
const requestDate = ref('')
const selectedDogs = ref([])
const requestError = ref('')
const requestSuccess = ref('')

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

const openRequestPanel = (ad) => {
  selectedAd.value = ad
  showRequestPanel.value = true
  requestDate.value = ''
  selectedDogs.value = []
  requestError.value = ''
  requestSuccess.value = ''
}

const closeRequestPanel = () => {
  showRequestPanel.value = false
}

const submitRequest = async () => {
  requestError.value = ''
  requestSuccess.value = ''
  if (!requestDate.value || !selectedDogs.value.length) {
    requestError.value = 'Debes seleccionar un día y al menos un perro.'
    return
  }
  try {
    await requestsPost('', {
      walker_id: selectedAd.value.walker_id || selectedAd.value.walkerId || selectedAd.value.walker,
      ad_id: selectedAd.value._id,
      date: requestDate.value,
      dogs: selectedDogs.value,
    })
    requestSuccess.value = 'Solicitud enviada correctamente.'
    setTimeout(() => {
      showRequestPanel.value = false
    }, 1500)
  } catch (e) {
    requestError.value = e?.response?.data?.msg || 'Error al enviar la solicitud.'
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
