<template>
  <div class="container"></div>
  <div class="wrapper">
    <header class="header">
      <div class="box-logo-img">
        <div class="logo" @click="goToHome">
          <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
          <div>
            <h2>DogGo!</h2>
            <p>Para ti, por ellos.</p>
          </div>
        </div>
      </div>
      <div class="nav-buttons">
        <button @click="goToProfile">Perfil</button>
        <button @click="goToHome">Inicio</button>
        <button @click="logout">
          Cerrar sesión <i class="fa-solid fa-right-from-bracket"></i>
        </button>
      </div>
    </header>

    <div class="main">
      <div class="title-filter">
        <h2>Paseadores disponibles</h2>
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
      </div>
      <div class="box-ads">
        <div v-if="ads.length" class="ads-grid-container">
          <div v-for="ad in ads" :key="ad._id" class="ad-card">
            <p>{{ capitalize(ad.walker_name) }} {{ capitalize(ad.walker_lastName) }}</p>
            <p><strong>Biografía:</strong></p>
            <div class="bio-content">
              {{ ad.biography }}
            </div>
            <p>Máximo de perros: {{ ad.maxDogs }}</p>
            <p>Localidad: {{ ad.locality }}</p>
            <p>Email: {{ ad.walker_email }}</p>
            <br />
            <button @click="openRequestPanel(ad)">Solicitar servicio</button>
          </div>
        </div>
        <p v-else-if="loading">Cargando anuncios...</p>
        <p style="color: white" v-else>No hay anuncios activos disponibles.</p>

        <div v-if="showRequestPanel" class="modal-overlay">
          <div class="modal-content">
            <h2>Solicitar Paseo</h2>
            <form @submit.prevent="submitRequest">
              <div class="form-group">
                <label for="requestDate">Día:</label>
                <input type="date" id="requestDate" v-model="requestDate" required />
              </div>
              <div class="form-group">
                <label for="locality">Localidad:</label>
                <input type="text" id="locality" :value="selectedAd.locality" disabled />
              </div>
              <div class="form-group modal-dogs">
                <label>Perros:</label>
                <div v-if="authStore.dogs.length" class="dog-list">
                  <div v-for="dog in authStore.dogs" :key="dog._id" class="dog-item">
                    <input
                      class="checkbox"
                      type="checkbox"
                      :id="dog._id"
                      :value="dog._id"
                      v-model="selectedDogs"
                    />
                    <label :for="dog._id"
                      >{{ capitalize(dog.name) }} ({{ capitalize(dog.breed) }})</label
                    >
                  </div>
                </div>
                <div v-else class="info-message">
                  <p>No tienes perros registrados. <br />No puedes solicitar el servicio.</p>
                </div>
              </div>
              <div class="form-actions">
                <button type="submit" :disabled="!authStore.dogs.length || !selectedDogs.length">
                  Enviar solicitud
                </button>
                <button type="button" @click="closeRequestPanel" class="cancel-button">
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
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
import { useToast } from 'vue-toastification'

const toast = useToast()
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

const fetchAds = async () => {
  loading.value = true
  try {
    const url = selectedLocality.value
      ? `/all?locality=${encodeURIComponent(selectedLocality.value)}`
      : '/all'
    const response = await adsGet(url)
    ads.value = response.data
  } catch (error) {
    toast.error(error.response?.data?.msg || 'Error al cargar anuncios.')
  } finally {
    loading.value = false
  }
}

const openRequestPanel = (ad) => {
  selectedAd.value = ad
  showRequestPanel.value = true
  requestDate.value = ''
  selectedDogs.value = []
}

const closeRequestPanel = () => {
  showRequestPanel.value = false
}

const submitRequest = async () => {
  if (!requestDate.value || !selectedDogs.value.length) {
    toast.error('Debes seleccionar un día y al menos un perro.')
    return
  }
  try {
    await requestsPost('', {
      walker_id: selectedAd.value.walker_id || selectedAd.value.walkerId || selectedAd.value.walker,
      ad_id: selectedAd.value._id,
      date: requestDate.value,
      dogs: selectedDogs.value,
    })
    toast.success('Solicitud enviada correctamente.')
    setTimeout(() => {
      showRequestPanel.value = false
    }, 1500)
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al enviar la solicitud.')
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
    await authStore.fetchDogs()
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
  toast.info('Sesión cerrada correctamente.')
}
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  box-sizing: border-box;
}

*,
*::before,
*::after {
  box-sizing: inherit;
}

.wrapper {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  background: #021a37;
}

.header {
  background-color: #003978;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  width: 100%;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
}

.header .box-logo-img {
  display: flex;
  align-items: center;
  width: 60%;
}

.header .logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  width: 20vh;
}

.header .logo img {
  height: 60px;
  margin-right: 1rem;
  cursor: pointer;
}

.header .logo h2 {
  color: #fecf35;
  font-weight: 800;
  font-size: 2.5rem;
  margin: 0;
  cursor: pointer;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.header .logo p {
  color: white;
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  text-align: end;
  width: 30vh;
  cursor: pointer;
}

.nav-buttons {
  display: flex;
  gap: 1rem;
}

.nav-buttons button {
  background-color: #fecf35;
  color: #003978;
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.nav-buttons button:hover {
  background-color: #ffda6a;
}

.main {
  flex-grow: 1;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title-filter {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1200px;
  margin-bottom: 2rem;
}

.title-filter h2 {
  color: #fecf35;
  font-size: 2rem;
  font-weight: 700;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
}

.filters {
  display: flex;
  gap: 1rem;
}

.filters select,
.filters button {
  padding: 0.7rem 1.2rem;
  border: none;
  border-radius: 10px;
  background-color: #003978;
  color: #fecf35;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

.filters select {
  width: 30vh;
  outline: none;
}

.filters button:hover {
  background-color: #002a5e;
}

.box-ads {
  width: 100%;
  max-width: 1200px;
  padding: 1rem;
}

.ads-grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 2rem;
  justify-content: center;
  align-items: start;
}

.ad-card {
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
  height: 100%;
}

.ad-card p {
  margin: 0.5rem 0;
  font-size: 1rem;
  text-align: center;
  color: #333;
}

.ad-card button {
  background-color: #003978;
  color: #fecf35;
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  margin-top: auto;
  transition: background-color 0.2s;
}

.ad-card button:hover {
  background-color: #002a5e;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background-color: #002a5c;
  padding: 2.5rem;
  border-radius: 10px;
  width: 90%;
  max-width: 500px;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  animation: modal-fade-in 0.3s ease-out forwards;
}

@keyframes modal-fade-in {
  from {
    opacity: 0;
    transform: translateY(-30px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-content h2 {
  color: #fecf35;
  font-size: 2rem;
  margin-bottom: 1rem;
  text-align: center;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.modal-content .form-group {
  margin-bottom: 1.2rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.modal-content label {
  font-weight: 600;
  color: #fecf35;
  font-size: 1.05rem;
  margin-bottom: 0.4rem;
}

.modal-content input[type='date'],
.modal-content input[type='text'] {
  width: 100%;
  padding: 0.9rem;
  border: 1px solid white;
  border-radius: 5px;
  font-size: 1rem;
  transition:
    border-color 0.3s ease,
    box-shadow 0.3s ease;
}

.modal-content input[type='date']:focus,
.modal-content input[type='text']:focus {
  border-color: #fecf35;
  box-shadow: 0 0 0 3px rgba(254, 207, 53, 0.3);
  outline: none;
}

.modal-content input[type='text'][disabled] {
  background-color: #eef2f5;
  cursor: not-allowed;
  opacity: 0.8;
}

.modal-dogs {
  margin-bottom: 1.2rem;
}

.modal-dogs label {
  width: auto;
}

.modal-dogs .dog-list {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 1rem;
  max-height: 150px;
  overflow-y: auto;
  background-color: #fcfcfc;
  box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

.dog-item {
  display: flex;
  align-items: center;
  margin-bottom: 0.8rem;
  gap: 0.8rem;
}

.dog-item:last-child {
  margin-bottom: 0;
}

.checkbox {
  transform: scale(1.3);
  cursor: pointer;
  accent-color: #003978;
}

.dog-item label {
  font-weight: 500;
  color: #444;
  cursor: pointer;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 2rem;
}

.modal-content button {
  padding: 0.9rem 1.8rem;
  border-radius: 10px;
  font-size: 1.05rem;
  font-weight: 700;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease,
    box-shadow 0.3s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  border: none;
}

.modal-content button[type='submit'] {
  background-color: #003978;
  color: #ffffff;
}

.modal-content button[type='submit']:disabled {
  background-color: #b0c4de;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.modal-content button[type='submit']:not(:disabled):hover {
  background-color: #002a5c;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
}

.modal-content .cancel-button {
  background-color: #dc3545;
  color: #ffffff;
}

.modal-content .cancel-button:hover {
  background-color: #c82333;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
}

.success-message {
  color: #28a745;
  background-color: #d4edda;
  padding: 0.8rem;
  border-radius: 8px;
  margin-top: 1.5rem;
  text-align: center;
  font-weight: 600;
  border: 1px solid #c3e6cb;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  padding: 0.8rem;
  border-radius: 8px;
  margin-top: 1.5rem;
  text-align: center;
  font-weight: 600;
  border: 1px solid #f5c6cb;
}

.ad-card .bio-content {
  max-height: 120px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.4;
  font-size: 0.95rem;
  color: #444;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  text-align: left;
  width: 100%;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    padding: 1rem;
    gap: 1rem;
  }

  .header .box-logo-img {
    width: 100%;
    justify-content: center;
  }

  .header .logo {
    flex-direction: column;
    text-align: center;
  }

  .header .logo img {
    margin-right: 0;
    margin-bottom: 0.5rem;
  }

  .header .logo p {
    text-align: center;
    width: auto;
  }

  .nav-buttons {
    flex-direction: column;
    width: 100%;
  }

  .nav-buttons button {
    width: 100%;
    justify-content: center;
  }

  .main {
    padding: 1rem;
  }

  .title-filter {
    flex-direction: column;
    width: 95%;
    padding: 1.2rem;
    text-align: center;
    margin-bottom: 2rem;
  }

  .title-filter h2 {
    font-size: 2rem;
    margin-bottom: 1rem;
  }

  .filters {
    flex-direction: column;
    width: 100%;
    gap: 0.8rem;
  }

  .filters select,
  .filters button {
    width: 100%;
    padding: 0.9rem;
    font-size: 0.95rem;
  }

  .box-ads {
    padding: 0 0.5rem;
  }

  .ads-grid-container {
    grid-template-columns: 1fr;
  }

  .ad-card {
    width: auto;
    padding: 1.5rem;
  }

  .modal-content {
    width: 95%;
    padding: 1.8rem;
    gap: 1.5rem;
  }

  .modal-content h2 {
    font-size: 1.7rem;
  }

  .modal-content button {
    padding: 0.8rem 1.5rem;
    font-size: 0.95rem;
  }

  .modal-content .form-actions {
    flex-direction: column-reverse;
    gap: 0.8rem;
  }

  .modal-content .form-actions button {
    width: 100%;
  }
}
</style>
