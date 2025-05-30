<template>
  <div v-if="authStore.isLoggedIn && authStore.user">
    <header>
      <h1>¡Hola, {{ authStore.userName }}! - Perfil de Paseador</h1>
      <div class="nav-buttons">
        <button @click="goToHome">Inicio</button>
        <button @click="logout">Cerrar sesión</button>
        <button @click="showPersonalInfo = true">Información personal</button>
      </div>
    </header>

    <div v-if="showPersonalInfo" class="modal-overlay">
      <div class="modal-content">
        <h2>Información personal</h2>
        <template v-if="!editPersonal">
          <ul>
            <li><strong>Nombre:</strong> {{ authStore.user?.name }}</li>
            <li><strong>Apellido:</strong> {{ authStore.user?.last_name }}</li>
            <li><strong>Email:</strong> {{ authStore.user?.email }}</li>
          </ul>
          <button @click="editPersonal = true">Editar datos</button>
          <button @click="showChangePassword = true">Cambiar contraseña</button>
          <button class="delete-btn" @click="confirmDelete = true">Eliminar cuenta</button>
          <button @click="showPersonalInfo = false">Cerrar</button>
        </template>
        <template v-else>
          <form @submit.prevent="savePersonalData">
            <div>
              <label>Nombre:</label>
              <input v-model="editName" required />
            </div>
            <div>
              <label>Apellido:</label>
              <input v-model="editLastName" required />
            </div>
            <div>
              <label>Email:</label>
              <input v-model="editEmail" type="email" required />
            </div>
            <button type="submit">Guardar</button>
            <button type="button" @click="cancelEditPersonal">Cancelar</button>
            <p v-if="personalError" class="error-message">{{ personalError }}</p>
            <p v-if="personalSuccess" class="success-message">{{ personalSuccess }}</p>
          </form>
        </template>
        <div v-if="showChangePassword">
          <form @submit.prevent="changePassword">
            <div>
              <label>Contraseña actual:</label>
              <input v-model="oldPassword" type="password" required />
            </div>
            <div>
              <label>Nueva contraseña:</label>
              <input v-model="newPassword" type="password" required />
            </div>
            <div>
              <label>Repite nueva contraseña:</label>
              <input v-model="repeatNewPassword" type="password" required />
            </div>
            <button type="submit">Cambiar contraseña</button>
            <button type="button" @click="showChangePassword = false">Cancelar</button>
            <p v-if="passwordError" class="error-message">{{ passwordError }}</p>
            <p v-if="passwordSuccess" class="success-message">{{ passwordSuccess }}</p>
          </form>
        </div>
      </div>
    </div>

    <div v-if="confirmDelete" class="modal-overlay">
      <div class="modal-content">
        <p>¿Seguro que quieres eliminar tu cuenta? Esta acción es irreversible.</p>
        <button class="delete-btn" @click="deleteAccount">Sí, eliminar</button>
        <button @click="confirmDelete = false">Cancelar</button>
      </div>
    </div>

    <h2>Tu Anuncio</h2>
    <div v-if="walkerAdStore.walkerAd">
      <div class="ad-card">
        <p>{{ authStore.user?.name }} {{ authStore.user?.last_name }}</p>
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
        <select id="add-locality" v-model="newAd.locality" required>
          <option value="" disabled>Selecciona una provincia</option>
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
        <select id="edit-locality" v-model="editAd.locality" required>
          <option value="" disabled>Selecciona una provincia</option>
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

    <h2>Solicitudes recibidas</h2>
    <div v-if="walkerRequestsLoading">Cargando...</div>
    <div v-else-if="walkerRequestsError">{{ walkerRequestsError }}</div>
    <ul v-else>
      <li v-for="req in walkerRequests" :key="req._id">
        <div>
          <strong>Dueño:</strong> {{ req.owner_info?.name }} {{ req.owner_info?.last_name }} ({{
            req.owner_info?.email
          }})
        </div>
        <div>
          <strong>Perros:</strong>
          <ul>
            <li v-for="dog in req.dogs_info" :key="dog._id">
              {{ dog.name }} ({{ dog.breed }}, {{ dog.age }} años)
            </li>
          </ul>
        </div>
        <div>
          <strong>Fecha:</strong> {{ req.date }} - <strong>Estado:</strong> {{ req.status }}
        </div>
        <button v-if="req.status === 'pendiente'" @click="acceptRequest(req._id)">Aceptar</button>
        <button v-if="req.status === 'pendiente'" @click="rejectRequest(req._id)">Rechazar</button>
        <button v-if="req.status === 'aceptada'" @click="cancelRequest(req._id)">Cancelar</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWalkerAdStore } from '@/stores/walkerAd'
import { requestsGet, requestsPatch } from '../../api/api'
import provinces from '@/data/provinces.json'

const comunidades = Object.keys(provinces)
const provinciasPorComunidad = provinces

const router = useRouter()
const authStore = useAuthStore()
const walkerAdStore = useWalkerAdStore()
const showPersonalInfo = ref(false)
const editPersonal = ref(false)
const showChangePassword = ref(false)
const confirmDelete = ref(false)
const editName = ref(authStore.user?.name || '')
const editLastName = ref(authStore.user?.last_name || '')
const editEmail = ref(authStore.user?.email || '')
const personalError = ref('')
const personalSuccess = ref('')
const passwordError = ref('')
const passwordSuccess = ref('')
const oldPassword = ref('')
const newPassword = ref('')
const repeatNewPassword = ref('')

const showAddAdForm = ref(false)
const showEditAdForm = ref(false)
const showDeleteConfirm = ref(false)
const newAd = ref({ biography: '', maxDogs: '', locality: '' })
const editAd = ref({ biography: '', maxDogs: '', locality: '' })

const walkerRequests = ref([])
const walkerRequestsLoading = ref(false)
const walkerRequestsError = ref('')

const fetchWalkerRequests = async () => {
  walkerRequestsLoading.value = true
  try {
    const res = await requestsGet('/walker')
    walkerRequests.value = res.data
  } catch (e) {
    walkerRequestsError.value = e?.response?.data?.msg || 'Error al cargar solicitudes'
  } finally {
    walkerRequestsLoading.value = false
  }
}

const acceptRequest = async (id) => {
  await requestsPatch(`/${id}/accept`)
  fetchWalkerRequests()
}
const rejectRequest = async (id) => {
  await requestsPatch(`/${id}/reject`)
  fetchWalkerRequests()
}
const cancelRequest = async (id) => {
  await requestsPatch(`/${id}/cancel`)
  fetchWalkerRequests()
}

watch(
  () => showPersonalInfo.value,
  (val) => {
    if (val && authStore.user) {
      editName.value = authStore.user.name
      editLastName.value = authStore.user.last_name
      editEmail.value = authStore.user.email
    }
  },
)

const savePersonalData = async () => {
  personalError.value = ''
  personalSuccess.value = ''
  try {
    await authStore.updatePersonalData({
      name: editName.value,
      last_name: editLastName.value,
      email: editEmail.value,
    })
    personalSuccess.value = 'Datos actualizados correctamente'
    editPersonal.value = false
  } catch (e) {
    personalError.value = e?.response?.data?.msg || 'Error al actualizar los datos'
  }
}

const cancelEditPersonal = () => {
  editPersonal.value = false
  personalError.value = ''
  personalSuccess.value = ''
}

const changePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = ''
  if (newPassword.value !== repeatNewPassword.value) {
    passwordError.value = 'Las contraseñas nuevas no coinciden'
    return
  }
  try {
    await authStore.changePassword({
      oldPassword: oldPassword.value,
      newPassword: newPassword.value,
    })
    passwordSuccess.value = 'Contraseña cambiada correctamente'
    oldPassword.value = ''
    newPassword.value = ''
    repeatNewPassword.value = ''
    showChangePassword.value = false
  } catch (e) {
    passwordError.value = e?.response?.data?.msg || 'Error al cambiar la contraseña'
  }
}

const goToHome = () => {
  router.push({ name: 'index' })
}

const deleteAccount = async () => {
  try {
    await authStore.deleteUserAccount()
    router.push({ name: 'index' })
  } catch (e) {
    alert('Error al eliminar la cuenta')
  }
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

onMounted(async () => {
  authStore.initializeAuth()
  fetchWalkerRequests()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else if (authStore.userRole === 'walker') {
    await walkerAdStore.fetchWalkerAd()
  } else {
    router.push({ name: 'index' })
  }
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 1rem;
  min-width: 300px;
  color: #333;
  text-align: center;
}
.delete-btn {
  background: #c0392b;
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 0.5rem;
  cursor: pointer;
  margin: 1rem 0.5rem 0 0.5rem;
  font-weight: bold;
}
.delete-btn:hover {
  background: #e74c3c;
}
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
  background-color: #007bff;
  color: white;
}
.nav-buttons button:nth-child(3) {
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
textarea,
select {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}
.error-message {
  color: #dc3545;
  margin-top: 10px;
}
.success-message {
  color: #28a745;
  margin-top: 10px;
}
ul {
  list-style: none;
  padding: 0;
}
li {
  padding: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
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
.ad-card {
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  background: #fafafa;
}
</style>
