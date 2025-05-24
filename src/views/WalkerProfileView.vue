<template>
  <div v-if="authStore.isLoggedIn && authStore.user">
    <header>
      <h1>¡Hola, {{ authStore.userName }}! - Perfil de Paseador</h1>
      <div class="nav-buttons">
        <button @click="goToHome">Inicio</button>
        <button @click="logout">Cerrar sesión</button>
      </div>
    </header>

    <h2>Tu Anuncio</h2>
    <!-- <div v-if="walkerAdStore.loading">
      <p>Cargando anuncio...</p>
    </div> -->
    <div v-if="walkerAdStore.walkerAd">
      <div class="ad-card">
        <p><strong>Biografía:</strong> {{ walkerAdStore.walkerAd.biography }}</p>
        <p><strong>Máximo de perros por paseo:</strong> {{ walkerAdStore.walkerAd.maxDogs }}</p>
        <p><strong>Localidad:</strong> {{ walkerAdStore.walkerAd.locality }}</p>
        <p><strong>Estado:</strong> {{ walkerAdStore.walkerAd.paused ? 'Pausado' : 'Activo' }}</p>
        <button @click="handlePauseToggle">
          {{ walkerAdStore.walkerAd.paused ? 'Activar Anuncio' : 'Pausar Anuncio' }}
        </button>
        <button @click="toggleEditAdForm(walkerAdStore.walkerAd)">Editar Anuncio</button>
        <button @click="showDeleteConfirmation">Eliminar Anuncio</button>
      </div>
    </div>
    <div v-else>
      <p>No tienes un anuncio creado.</p>
      <p v-if="walkerAdStore.error" class="error-message">{{ walkerAdStore.error }}</p>
      <button @click="toggleAddAdForm">Crear Anuncio</button>
    </div>

    <form v-if="showAddAdForm" @submit.prevent="validateAndCreateAd">
      <div>
        <label for="add-biography">Biografía:</label>
        <textarea id="add-biography" v-model="newAd.biography" required></textarea>
      </div>
      <div>
        <label for="add-maxDogs">Máximo de perros por paseo:</label>
        <input type="number" id="add-maxDogs" v-model.number="newAd.maxDogs" required min="1" />
      </div>
      <div>
        <label for="add-locality">Localidad:</label>
        <input type="text" id="add-locality" v-model="newAd.locality" required />
      </div>
      <button type="submit">Crear Anuncio</button>
      <p v-if="walkerAdStore.error" class="error-message">{{ walkerAdStore.error }}</p>
      <p v-if="walkerAdStore.success" class="success-message">{{ walkerAdStore.success }}</p>
    </form>

    <form v-if="showEditAdForm" @submit.prevent="validateAndUpdateAd">
      <h3>Editar Anuncio</h3>
      <div>
        <label for="edit-biography">Biografía:</label>
        <textarea id="edit-biography" v-model="editAd.biography" required></textarea>
      </div>
      <div>
        <label for="edit-maxDogs">Máximo de perros por paseo:</label>
        <input type="number" id="edit-maxDogs" v-model.number="editAd.maxDogs" required min="1" />
      </div>
      <div>
        <label for="edit-locality">Localidad:</label>
        <input type="text" id="edit-locality" v-model="editAd.locality" required />
      </div>
      <button type="submit">Guardar Cambios</button>
      <button type="button" @click="toggleEditAdForm(null)">Cancelar</button>
      <p v-if="walkerAdStore.error" class="error-message">{{ walkerAdStore.error }}</p>
      <p v-if="walkerAdStore.success" class="success-message">{{ walkerAdStore.success }}</p>
    </form>

    <div v-if="showDeleteConfirm" class="confirm-dialog">
      <p>¿Estás seguro de eliminar tu anuncio?</p>
      <button @click="deleteAd">Sí, eliminar</button>
      <button @click="cancelDelete">Cancelar</button>
    </div>

    <h2>Paseos Programados</h2>
    <div v-if="loadingBookings">
      <p>Cargando paseos...</p>
    </div>
    <div v-else-if="bookings.length > 0">
      <ul>
        <li v-for="booking in bookings" :key="booking._id">
          Paseo con {{ booking.owner_name }} el {{ formatDate(booking.date) }} para
          {{ booking.dog_name }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No tienes paseos programados.</p>
      <p v-if="bookingsError" class="error-message">{{ bookingsError }}</p>
    </div>
  </div>
  <div v-else>
    <p>Cargando perfil...</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWalkerAdStore } from '@/stores/walkerAd'
import { bookingsGet } from '../../api/api'

const router = useRouter()
const authStore = useAuthStore()
const walkerAdStore = useWalkerAdStore()

const showAddAdForm = ref(false)
const showEditAdForm = ref(false)
const showDeleteConfirm = ref(false)
const newAd = ref({ biography: '', maxDogs: '', locality: '' })
const editAd = ref({ biography: '', maxDogs: '', locality: '' })
const bookings = ref([])
const loadingBookings = ref(false)
const bookingsError = ref(null)

const goToHome = () => {
  router.push({ name: 'index' })
}

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'index' })
}

const toggleAddAdForm = () => {
  showAddAdForm.value = !showAddAdForm.value
  newAd.value = { biography: '', maxDogs: '', locality: '' }
  showEditAdForm.value = false
  walkerAdStore.error = null
  walkerAdStore.success = null
}

const toggleEditAdForm = (ad) => {
  showEditAdForm.value = !showEditAdForm.value
  if (ad) {
    editAd.value = {
      biography: ad.biography || '',
      maxDogs: ad.maxDogs || 1,
      locality: ad.locality || '',
    }
    showAddAdForm.value = false
  } else {
    editAd.value = { biography: '', maxDogs: '', locality: '' }
    walkerAdStore.error = null
    walkerAdStore.success = null
  }
}

const validateAndCreateAd = async () => {
  if (!newAd.value.biography || !newAd.value.maxDogs || !newAd.value.locality) {
    walkerAdStore.error = 'Todos los campos son obligatorios'
    return
  }
  if (newAd.value.maxDogs < 1) {
    walkerAdStore.error = 'El número máximo de perros debe ser al menos 1'
    return
  }
  await walkerAdStore.createWalkerAd(newAd.value)
}

const validateAndUpdateAd = async () => {
  if (!editAd.value.biography || !editAd.value.maxDogs || !editAd.value.locality) {
    walkerAdStore.error = 'Todos los campos son obligatorios'
    return
  }
  if (editAd.value.maxDogs < 1) {
    walkerAdStore.error = 'El número máximo de perros debe ser al menos 1'
    return
  }
  await walkerAdStore.updateWalkerAd(editAd.value)
  if (!walkerAdStore.error) {
    showEditAdForm.value = false
  }
}

const showDeleteConfirmation = () => {
  showDeleteConfirm.value = true
  showEditAdForm.value = false
  showAddAdForm.value = false
}

const handlePauseToggle = async () => {
  showEditAdForm.value = false
  await walkerAdStore.togglePauseWalkerAd()
}

const deleteAd = async () => {
  await walkerAdStore.deleteWalkerAd()
  showDeleteConfirm.value = false
}

const cancelDelete = () => {
  showDeleteConfirm.value = false
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })
}

const fetchBookings = async () => {
  loadingBookings.value = true
  try {
    const response = await bookingsGet('/walker')
    bookings.value = response.data
    bookingsError.value = null
  } catch (error) {
    bookingsError.value = error.response?.data?.msg || 'Error al cargar paseos'
    console.error('Error al cargar paseos:', bookingsError.value)
  } finally {
    loadingBookings.value = false
  }
}

onMounted(async () => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else if (authStore.userRole === 'walker') {
    await walkerAdStore.fetchWalkerAd()
    console.log('Anuncio en vista:', walkerAdStore.walkerAd)
    await fetchBookings()
  } else {
    router.push({ name: 'index' })
  }
})
</script>

<style scoped>
header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.nav-buttons {
  display: flex;
  gap: 10px;
}
h1,
h2,
h3 {
  color: #333;
}
button {
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin: 5px;
}
button:hover {
  opacity: 0.9;
}
.nav-buttons button:nth-child(1) {
  background-color: #6c757d;
  color: white;
}
.nav-buttons button:nth-child(2) {
  background-color: #dc3545;
  color: white;
}
.ad-card {
  border: 1px solid #ccc;
  padding: 15px;
  margin: 10px 0;
  border-radius: 5px;
}
.ad-card button:nth-child(1) {
  background-color: #007bff;
  color: white;
}
.ad-card button:nth-child(2) {
  background-color: #28a745;
  color: white;
}
.ad-card button:nth-child(3) {
  background-color: #dc3545;
  color: white;
}
form {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 300px;
}
label {
  font-weight: bold;
}
input,
textarea {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}
textarea {
  height: 100px;
}
.error-message {
  color: #dc3545;
  margin-top: 10px;
}
.success-message {
  color: #28a745;
  margin-top: 10px;
}
.confirm-dialog {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  z-index: 1000;
}
.confirm-dialog button {
  margin: 10px 5px;
}
.confirm-dialog button:first-child {
  background-color: #dc3545;
  color: white;
}
.confirm-dialog button:last-child {
  background-color: #6c757d;
  color: white;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  padding: 10px 0;
}
</style>
