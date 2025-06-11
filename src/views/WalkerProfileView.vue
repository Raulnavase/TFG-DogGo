<template>
  <div class="wrapper" v-if="authStore.isLoggedIn && authStore.user">
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
      <div class="box-btns-navbar">
        <button @click="goToHome">Inicio</button>
        <button @click="logout">
          Cerrar sesión <i class="fa-solid fa-right-from-bracket"></i>
        </button>
        <button @click="showPersonalInfo = true">Información personal</button>
      </div>
    </header>

    <div class="main">
      <div class="wellcome-box">
        <h1>¡Hola, {{ authStore.userName }}! - Perfil de Paseador</h1>
      </div>

      <div v-if="showPersonalInfo" class="modal-overlay">
        <div class="modal-content">
          <h2>Información personal</h2>
          <template v-if="!editPersonal">
            <ul>
              <li><strong>Nombre:</strong> {{ capitalize(authStore.user?.name) }}</li>
              <li><strong>Apellido:</strong> {{ capitalize(authStore.user?.last_name) }}</li>
              <li><strong>Email:</strong> {{ authStore.user?.email }}</li>
            </ul>
            <div class="form-actions">
              <button @click="editPersonal = true">Editar datos</button>
              <button @click="showChangePassword = true">Cambiar contraseña</button>
              <button class="delete-btn" @click="confirmDelete = true">Eliminar cuenta</button>
              <button @click="showPersonalInfo = false">Cerrar</button>
            </div>
          </template>
          <template v-else>
            <form @submit.prevent="savePersonalData">
              <div>
                <label>Nombre:</label>
                <input pattern="^\S.*\S$" v-model="editName" required />
              </div>
              <div>
                <label>Apellido:</label>
                <input pattern="^\S.*\S$" v-model="editLastName" required />
              </div>
              <div>
                <label>Email:</label>
                <input
                  pattern="^\S.*\S$"
                  oninput="this.value = this.value.trim()"
                  v-model="editEmail"
                  type="email"
                  required
                />
              </div>
              <div class="form-actions">
                <button type="submit">Guardar</button>
                <button type="button" @click="cancelEditPersonal">Cancelar</button>
              </div>
            </form>
          </template>
          <div v-if="showChangePassword">
            <form @submit.prevent="changePassword">
              <div>
                <label>Contraseña actual:</label>
                <input pattern="^\S.*\S$" v-model="oldPassword" type="password" required />
              </div>
              <div>
                <label>Nueva contraseña:</label>
                <input
                  pattern="^(?=.*[A-Z])(?=.*\d)\S{8,}$"
                  v-model="newPassword"
                  type="password"
                  required
                  @focus="showPasswordHint = true"
                  @blur="showPasswordHint = false"
                />
                <p v-if="showPasswordHint" class="password-hint">
                  La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.
                </p>
              </div>
              <div>
                <label>Repite nueva contraseña:</label>
                <input pattern="^\S.*\S$" v-model="repeatNewPassword" type="password" required />
              </div>
              <div class="form-actions">
                <button type="submit">Cambiar contraseña</button>
                <button type="button" @click="showChangePassword = false">Cancelar</button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div v-if="confirmDelete" class="modal-overlay">
        <div class="modal-content">
          <p>¿Seguro que quieres eliminar tu cuenta? Esta acción es irreversible.</p>
          <div class="confirm-dialog-actions">
            <button class="delete-btn" @click="deleteAccount">Sí, eliminar</button>
            <button @click="confirmDelete = false">Cancelar</button>
          </div>
        </div>
      </div>

      <div class="ad-requests">
        <div class="box-myad">
          <h2>Tu Anuncio</h2>
          <div class="ad-container">
            <div v-if="walkerAdStore.walkerAd" class="ad-card">
              <p class="ad-name">
                {{ capitalize(authStore.user?.name) }}
                {{ capitalize(authStore.user?.last_name) }}
              </p>
              <p><strong>Biografía:</strong> {{ walkerAdStore.walkerAd.biography }}</p>
              <p>
                <strong>Máximo de perros por paseo:</strong> {{ walkerAdStore.walkerAd.maxDogs }}
              </p>
              <p><strong>Localidad:</strong> {{ walkerAdStore.walkerAd.locality }}</p>
              <p>
                <strong>Estado:</strong>
                <span :class="['ad-status', walkerAdStore.walkerAd.paused ? 'paused' : 'active']">
                  {{ walkerAdStore.walkerAd.paused ? 'Pausado' : 'Activo' }}
                </span>
              </p>
              <div class="ad-actions">
                <button @click="handlePauseToggle">
                  {{ walkerAdStore.walkerAd.paused ? 'Activar Anuncio' : 'Pausar Anuncio' }}
                </button>
                <button @click="toggleEditAdForm(walkerAdStore.walkerAd)">Editar Anuncio</button>
                <button class="delete-btn" @click="showDeleteConfirmation">Eliminar Anuncio</button>
              </div>
            </div>
            <div v-else>
              <p>No tienes un anuncio creado.</p>
              <button @click="toggleAddAdForm">Crear Anuncio</button>
            </div>
          </div>
        </div>

        <form v-if="showAddAdForm" @submit.prevent="validateAndCreateAd" class="add-ad-form">
          <h3>Crear Nuevo Anuncio</h3>
          <div>
            <label for="add-biography">Biografía:</label>
            <textarea id="add-biography" v-model="newAd.biography" required></textarea>
          </div>
          <div>
            <label for="add-maxDogs">Máximo de perros por paseo:</label>
            <input
              type="number"
              id="add-maxDogs"
              v-model.number="newAd.maxDogs"
              required
              min="1"
              max="10"
            />
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
          <div class="form-actions">
            <button type="submit">Crear Anuncio</button>
            <button type="button" @click="toggleAddAdForm">Cancelar</button>
          </div>
        </form>

        <div v-if="showEditAdForm" class="modal-overlay">
          <div class="modal-content">
            <h3>Editar Anuncio</h3>
            <form @submit.prevent="validateAndUpdateAd" class="edit-ad-form">
              <div>
                <label for="edit-biography">Biografía:</label>
                <textarea id="edit-biography" v-model="editAd.biography" required></textarea>
              </div>
              <div>
                <label for="edit-maxDogs">Máximo de perros por paseo:</label>
                <input
                  type="number"
                  id="edit-maxDogs"
                  v-model.number="editAd.maxDogs"
                  required
                  min="1"
                  max="10"
                />
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
              <div class="form-actions">
                <button type="submit">Guardar Cambios</button>
                <button type="button" @click="toggleEditAdForm(null)">Cancelar</button>
              </div>
            </form>
          </div>
        </div>

        <div v-if="showDeleteConfirm" class="modal-overlay confirm-ad-delete">
          <div class="modal-content">
            <p>¿Estás seguro de eliminar tu anuncio?</p>
            <div class="confirm-dialog-actions">
              <button @click="deleteAd" class="delete-btn">Sí, eliminar</button>
              <button @click="cancelDelete">Cancelar</button>
            </div>
          </div>
        </div>

        <div class="box-requests">
          <h2>Solicitudes recibidas</h2>
          <div class="requests-list-container">
            <div v-if="walkerRequestsLoading">Cargando...</div>
            <div v-else-if="walkerRequestsError" class="error-message">
              {{ walkerRequestsError }}
            </div>
            <ul v-else-if="walkerRequests.length > 0" class="request-cards-list">
              <li
                v-for="req in walkerRequests.filter((r) => r.status !== 'rechazada')"
                :key="req._id"
                class="request-card"
              >
                <div class="request-info">
                  <p>
                    <strong>Dueño:</strong> {{ capitalize(req.owner_info?.name) }}
                    {{ capitalize(req.owner_info?.last_name) }}
                    <span class="owner-email">({{ req.owner_info?.email }})</span>
                  </p>
                  <div class="request-dogs">
                    <strong>Perros:</strong>
                    <ul>
                      <li v-for="dog in req.dogs_info" :key="dog._id">
                        {{ capitalize(dog.name) }} ({{ capitalize(dog.breed) }}, {{ dog.age }} años)
                      </li>
                    </ul>
                  </div>
                  <p>
                    <strong>Fecha:</strong> <span class="request-date">{{ req.date }}</span> -
                    <strong>Estado:</strong>
                    <span :class="['request-status', req.status]">{{
                      statusText(req.status)
                    }}</span>
                  </p>
                </div>
                <div class="request-actions">
                  <button v-if="req.status === 'pendiente'" @click="acceptRequest(req._id)">
                    Aceptar
                  </button>
                  <button v-if="req.status === 'pendiente'" @click="rejectRequest(req._id)">
                    Rechazar
                  </button>
                  <button v-if="req.status === 'aceptada'" @click="cancelRequest(req._id)">
                    Cancelar
                  </button>
                  <button
                    v-if="
                      ['rechazada', 'cancelada_por_owner', 'cancelada_por_walker'].includes(
                        req.status,
                      )
                    "
                    @click="deleteRequest(req._id)"
                    class="delete-btn"
                  >
                    Eliminar
                  </button>
                </div>
              </li>
            </ul>
            <div v-else>
              <p>No hay solicitudes recibidas.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useWalkerAdStore } from '@/stores/walkerAd'
import { requestsGet, requestsPatch, requestsDelete } from '../../api/api'
import provinces from '@/data/provinces.json'
import { useToast } from 'vue-toastification'

const toast = useToast()
const statusText = (status) => {
  switch (status) {
    case 'pendiente':
      return 'Pendiente'
    case 'aceptada':
      return 'Aceptada'
    case 'rechazada':
      return 'Rechazada'
    case 'cancelada_por_owner':
      return 'Cancelada por el dueño'
    case 'cancelada_por_walker':
      return 'Cancelada por el paseador'
    default:
      return status
  }
}

const capitalize = (str) => (str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : '')

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

const oldPassword = ref('')
const newPassword = ref('')
const repeatNewPassword = ref('')
const showPasswordHint = ref(false)

const showAddAdForm = ref(false)
const showEditAdForm = ref(false)
const showDeleteConfirm = ref(false)
const newAd = ref({ biography: '', maxDogs: '', locality: '' })
const editAd = ref({ biography: '', maxDogs: '', locality: '' })

const walkerRequests = ref([])
const walkerRequestsLoading = ref(false)
const walkerRequestsError = ref('')

watch(
  () => showPersonalInfo.value,
  (val) => {
    if (val && authStore.user) {
      editName.value = authStore.user.name
      editLastName.value = authStore.user.last_name
      editEmail.value = authStore.user.email
      editPersonal.value = false
      showChangePassword.value = false
    }
  },
)

const fetchWalkerRequests = async () => {
  walkerRequestsLoading.value = true
  walkerRequestsError.value = ''
  try {
    const res = await requestsGet('/walker')
    walkerRequests.value = res.data
  } catch (e) {
    walkerRequestsError.value = e?.response?.data?.msg || 'Error al cargar solicitudes'
    toast.error(walkerRequestsError.value)
  } finally {
    walkerRequestsLoading.value = false
  }
}

const acceptRequest = async (id) => {
  try {
    await requestsPatch(`/${id}/accept`)
    toast.success('Solicitud aceptada correctamente.')
    fetchWalkerRequests()
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al aceptar la solicitud.')
  }
}

const rejectRequest = async (id) => {
  try {
    await requestsPatch(`/${id}/reject`)
    toast.success('Solicitud rechazada correctamente.')
    fetchWalkerRequests()
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al rechazar la solicitud.')
  }
}

const cancelRequest = async (id) => {
  try {
    await requestsPatch(`/${id}/cancel`)
    toast.success('Solicitud cancelada correctamente.')
    fetchWalkerRequests()
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al cancelar la solicitud.')
  }
}

const deleteRequest = async (id) => {
  try {
    await requestsDelete(`/${id}`)
    toast.success('Solicitud eliminada correctamente.')
    fetchWalkerRequests()
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al eliminar la solicitud.')
  }
}

const savePersonalData = async () => {
  try {
    await authStore.updatePersonalData({
      name: editName.value,
      last_name: editLastName.value,
      email: editEmail.value,
    })
    toast.success('Datos actualizados correctamente.')
    editPersonal.value = false
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al actualizar los datos.')
  }
}

const cancelEditPersonal = () => {
  editPersonal.value = false
  editName.value = authStore.user?.name || ''
  editLastName.value = authStore.user?.last_name || ''
  editEmail.value = authStore.user?.email || ''
}

const changePassword = async () => {
  if (newPassword.value !== repeatNewPassword.value) {
    toast.error('Las contraseñas nuevas no coinciden.')
    return
  }
  const passwordPattern = /^(?=.*[A-Z])(?=.*\d)\S{8,}$/
  if (!passwordPattern.test(newPassword.value)) {
    toast.error('La nueva contraseña debe tener al menos 8 caracteres, una mayúscula y un número.')
    return
  }
  try {
    await authStore.changePassword({
      oldPassword: oldPassword.value,
      newPassword: newPassword.value,
    })
    toast.success('Contraseña cambiada correctamente.')
    oldPassword.value = ''
    newPassword.value = ''
    repeatNewPassword.value = ''
    showChangePassword.value = false
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al cambiar la contraseña.')
  }
}

const goToHome = () => {
  router.push({ name: 'index' })
}

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'index' })
  toast.info('Sesión cerrada correctamente.')
}

const deleteAccount = async () => {
  try {
    await authStore.deleteUserAccount()
    toast.success('Cuenta eliminada correctamente.')
    router.push({ name: 'index' })
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al eliminar la cuenta.')
  } finally {
    confirmDelete.value = false
  }
}

const toggleAddAdForm = () => {
  showAddAdForm.value = !showAddAdForm.value
  newAd.value = { biography: '', maxDogs: '', locality: '' }
  showEditAdForm.value = false
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
  }
}

const validateAndCreateAd = async () => {
  if (!newAd.value.biography || !newAd.value.maxDogs || !newAd.value.locality) {
    toast.error('Todos los campos son obligatorios para crear un anuncio.')
    return
  }
  if (newAd.value.maxDogs < 1) {
    toast.error('El número máximo de perros debe ser al menos 1.')
    return
  }
  const success = await walkerAdStore.updateWalkerAd(data)
  if (success) {
    toast.success('Anuncio actualizado correctamente')
  } else {
    toast.error(walkerAdStore.error)
  }
}

const validateAndUpdateAd = async () => {
  if (!editAd.value.biography || !editAd.value.maxDogs || !editAd.value.locality) {
    toast.error('Todos los campos son obligatorios para editar el anuncio.')
    return
  }
  if (editAd.value.maxDogs < 1) {
    toast.error('El número máximo de perros debe ser al menos 1.')
    return
  }
  const success = await walkerAdStore.updateWalkerAd(editAd.value)
  if (success) {
    toast.success('Anuncio actualizado correctamente.')
    showEditAdForm.value = false
  } else {
    toast.error(walkerAdStore.error || 'Error al actualizar el anuncio.')
  }
}

const showDeleteConfirmation = () => {
  showDeleteConfirm.value = true
  showEditAdForm.value = false
  showAddAdForm.value = false
}

const handlePauseToggle = async () => {
  showEditAdForm.value = false
  const success = await walkerAdStore.togglePauseWalkerAd()
  if (success) {
    toast.success(
      walkerAdStore.walkerAd.paused
        ? 'Anuncio pausado correctamente.'
        : 'Anuncio activado correctamente.',
    )
  } else {
    toast.error(walkerAdStore.error || 'Error al cambiar el estado del anuncio.')
  }
}

const deleteAd = async () => {
  try {
    const success = await walkerAdStore.deleteWalkerAd()
    if (success) {
      toast.success('Anuncio eliminado correctamente.')
    } else {
      toast.error(walkerAdStore.error || 'Error al eliminar el anuncio.')
    }
  } catch (e) {
    toast.error(e?.response?.data?.msg || 'Error al eliminar el anuncio.')
  } finally {
    showDeleteConfirm.value = false
  }
}

const cancelDelete = () => {
  showDeleteConfirm.value = false
}

onMounted(async () => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else if (authStore.userRole === 'walker') {
    await walkerAdStore.fetchWalkerAd()
    fetchWalkerRequests()
  } else {
    router.push({ name: 'index' })
  }
})
</script>

<style scoped>
.password-hint {
  font-size: 0.85rem;
  color: #555;
  margin-top: 5px;
  margin-bottom: 10px;
  text-align: left;
}

.wrapper {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.header {
  background-color: #003978;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  flex-shrink: 0;
}

.header .box-logo-img {
  display: flex;
  align-items: center;
  width: 30%;
}

.header .logo {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.header .logo img {
  height: 60px;
  margin-right: 1rem;
  cursor: pointer;
}

.header .logo h2 {
  color: #fecf35;
  font-weight: 800;
  font-size: 2rem;
  margin: 0;
  cursor: pointer;
}

.header .logo p {
  color: white;
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  text-align: end;
  width: 25vh;
  cursor: pointer;
}

.box-btns-navbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.5rem;
}

.box-btns-navbar button {
  background-color: #fecf35;
  color: #003978;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  padding: 0.5rem 1rem;
  cursor: pointer;
  white-space: nowrap;
}

.box-btns-navbar button:hover {
  opacity: 0.9;
}

.wellcome-box h1 {
  margin: 1rem 2rem;
  padding: 1rem 2rem;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.main {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  overflow-y: auto;
}

.ad-requests {
  display: flex;
  flex-direction: row;
  width: 100%;
  flex-grow: 1;
  gap: 2rem;
  padding: 1rem 2rem;
}

.box-myad,
.box-requests {
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 1rem;
  flex: 1;
  min-width: 300px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  display: flex;
  flex-direction: column;
}

h2 {
  font-size: 1.4rem;
  margin: 0 0 1rem 0;
  border-bottom: 2px solid #003978;
  width: fit-content;
  padding-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-shrink: 0;
  flex-wrap: wrap;
}

button {
  background-color: #fecf35;
  color: #003978;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  margin: 0.5rem;
  transition: background-color 0.2s ease;
}

button:hover {
  background-color: #ffda6a;
}

.requests-list-container {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: #003978 #f0f0f0;
}

.requests-list-container::-webkit-scrollbar {
  width: 8px;
}

.requests-list-container::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 10px;
}

.requests-list-container::-webkit-scrollbar-thumb {
  background-color: #003978;
  border-radius: 10px;
  border: 2px solid #f0f0f0;
}

form {
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
  max-width: 400px;
  width: 100%;
  margin-top: 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex-shrink: 0;
  box-sizing: border-box;
}

.modal-content > form {
  background-color: transparent;
  box-shadow: none;
  margin-top: 0;
  padding: 0;
}

form div {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

input,
textarea,
select {
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

textarea {
  resize: vertical;
}

.success-message {
  color: #28a745;
  font-size: 0.9rem;
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
  padding: 0.7rem;
  border-radius: 5px;
  margin-top: 0.5rem;
}

.error-message {
  color: #dc3545;
  font-size: 0.9rem;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 0.7rem;
  border-radius: 5px;
  margin-top: 0.5rem;
}

.form-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-top: 1rem;
}

.form-actions button {
  flex-grow: 1;
  max-width: 150px;
  min-width: 120px;
  margin: 0;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  box-sizing: border-box;
}

.modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: 1rem;
  min-width: 350px;
  max-width: 90vw;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  position: relative;
  transform: none;
}

.modal-content h2,
.modal-content h3 {
  text-align: center;
  margin-bottom: 1.5rem;
  border-bottom: none;
  width: auto;
  font-size: 1.4rem;
}

.modal-content ul {
  padding: 0;
  display: block;
  text-align: left;
}

.modal-content ul li {
  background-color: transparent;
  padding: 0.5rem 0;
  width: auto;
  align-items: flex-start;
  box-shadow: none;
}

.modal-content button {
  width: fit-content;
  align-self: center;
  margin-top: 1rem;
}

.modal-content .delete-btn {
  background-color: #dc3545;
  color: white;
}

.modal-content .delete-btn:hover {
  background-color: #c82333;
}

.confirm-dialog-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.confirm-dialog-actions button {
  margin: 0;
  flex-grow: 1;
  max-width: 150px;
  min-width: 120px;
}

.confirm-dialog-actions .delete-btn {
  background-color: #dc3545;
  color: white;
}

.confirm-dialog-actions .delete-btn:hover {
  background-color: #c82333;
}

.confirm-dialog-actions button:not(.delete-btn) {
  background-color: #6c757d;
  color: white;
}

.confirm-dialog-actions button:not(.delete-btn):hover {
  background-color: #5a6268;
}

.ad-container {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: #003978 #f0f0f0;
}

.ad-card {
  background-color: #f0f8ff;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
  margin-top: 1.5rem;
}

.ad-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.ad-card p {
  margin: 0.5rem 0;
  font-size: 1rem;
  line-height: 1.4;
  text-align: left;
}

.ad-card p strong {
  color: #003978;
  font-weight: 600;
  margin-right: 0.3rem;
}

.ad-card .ad-name {
  font-size: 1.2rem;
  font-weight: bold;
  color: #003978;
  margin-bottom: 1rem;
  border-bottom: 1px solid #cce5ff;
  padding-bottom: 0.5rem;
}

.ad-card .ad-status {
  font-weight: bold;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  font-size: 0.85rem;
  display: inline-block;
  margin-left: 0.5rem;
}

.ad-status.active {
  background-color: #28a745;
  color: white;
}
.ad-status.paused {
  background-color: #ffc107;
  color: #333;
}

.ad-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.8rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #cce5ff;
}

.ad-actions button {
  flex-grow: 1;
  max-width: 180px;
  min-width: 120px;
  margin: 0;
  font-size: 0.9rem;
}

.request-cards-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
  padding: 0;
  list-style: none;
  margin-top: 1.5rem;
}

.request-card {
  background-color: #e0f7fa;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  padding: 1.2rem;
  padding-bottom: 2.2rem;
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
}

.request-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.request-info {
  flex-grow: 1;
  margin-bottom: 1rem;
}

.request-info p {
  margin: 0.5rem 0;
  font-size: 0.95rem;
  line-height: 1.4;
  text-align: left;
}

.request-info strong {
  color: #003978;
  font-weight: 600;
  margin-right: 0.3rem;
}

.request-info .owner-email {
  font-size: 0.85rem;
  color: #666;
}

.request-info .request-date {
  font-weight: normal;
}

.request-info .request-status {
  font-weight: bold;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  font-size: 0.85rem;
  display: inline-block;
  margin-left: 0.5rem;
}

.request-status.pendiente {
  background-color: #ffc107;
  color: #333;
}
.request-status.aceptada {
  background-color: #28a745;
  color: white;
}
.request-status.rechazada,
.request-status.cancelada_por_owner,
.request-status.cancelada_por_walker {
  background-color: #dc3545;
  color: white;
}

.request-dogs {
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px dashed #b3e0e9;
}

.request-dogs ul {
  padding-left: 1.2rem;
  list-style: disc;
  margin-top: 0.5rem;
}

.request-dogs ul li {
  background-color: transparent;
  padding: 0.2rem 0;
  font-size: 0.9rem;
  box-shadow: none;
  margin-left: 0;
  list-style-type: disc;
  align-items: baseline;
}

.request-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid #cce5ff;
  flex-wrap: wrap;
}

.request-actions button {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  margin: 0;
  border-radius: 8px;
}

.request-actions .delete-btn {
  background-color: #dc3545;
  color: white;
}
.request-actions .delete-btn:hover {
  background-color: #c82333;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    padding: 1rem;
    align-items: flex-start;
  }

  .header .box-logo-img {
    width: 100%;
    justify-content: center;
    margin-bottom: 1rem;
  }

  .header .logo h2 {
    font-size: 1.5rem;
  }

  .header .logo p {
    font-size: 0.8rem;
    width: auto;
    text-align: start;
  }

  .box-btns-navbar {
    width: 100%;
    flex-direction: column;
    gap: 0.8rem;
    align-items: center;
  }

  .box-btns-navbar button {
    width: 90%;
    max-width: 300px;
    margin: 0.2rem 0;
  }

  .wellcome-box h1 {
    margin: 1rem;
    padding: 1rem;
    font-size: 1.2rem;
    text-align: center;
  }

  .ad-requests {
    flex-direction: column;
    padding: 1rem;
    gap: 1.5rem;
    overflow-y: auto;
  }

  .box-myad,
  .box-requests {
    min-width: auto;
    padding: 1rem;
  }

  h2 {
    font-size: 1.2rem;
    flex-direction: column;
    align-items: flex-start;
    width: 100%;
    border-bottom: none;
    padding-bottom: 0;
  }

  .ad-container > button {
    margin-top: 0.8rem;
    width: 100%;
    max-width: 250px;
    align-self: center;
  }

  .ad-card {
    padding: 1rem;
  }

  .ad-actions {
    flex-direction: column;
    gap: 0.8rem;
  }

  .ad-actions button {
    width: 90%;
    max-width: 200px;
    align-self: center;
  }

  form {
    padding: 1rem;
    margin-top: 1rem;
    max-width: none;
  }

  .form-actions {
    flex-direction: column;
    gap: 0.8rem;
  }

  .form-actions button {
    width: 90%;
    max-width: 250px;
    align-self: center;
  }

  .modal-content {
    min-width: unset;
    width: 95%;
    padding: 1.5rem;
    max-height: 95vh;
  }

  .modal-content h2,
  .modal-content h3 {
    font-size: 1.2rem;
    margin-bottom: 1rem;
  }

  .confirm-dialog-actions {
    flex-direction: column;
    gap: 0.8rem;
  }

  .confirm-dialog-actions button {
    width: 90%;
    max-width: 250px;
    align-self: center;
  }

  .request-cards-list {
    grid-template-columns: 1fr;
  }

  .request-card {
    padding: 1rem;
    padding-bottom: 1.5rem;
  }

  .request-actions {
    flex-direction: column;
    gap: 0.8rem;
  }

  .request-actions button {
    width: 90%;
    max-width: 200px;
    align-self: center;
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  .header {
    padding: 1rem 1.5rem;
  }

  .header .logo h2 {
    font-size: 1.8rem;
  }

  .header .logo p {
    font-size: 0.9rem;
  }

  .box-btns-navbar {
    gap: 0.8rem;
  }

  .box-btns-navbar button {
    padding: 0.4rem 0.8rem;
    font-size: 0.9rem;
  }

  .wellcome-box h1 {
    margin: 1rem 1.5rem;
    padding: 1rem 1.5rem;
    font-size: 1.4rem;
  }

  .ad-requests {
    flex-direction: column;
    padding: 1rem 1.5rem;
    gap: 1.5rem;
    overflow-y: auto;
  }

  .box-myad,
  .box-requests {
    min-width: auto;
  }

  .request-cards-list {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  }

  .modal-content {
    min-width: 400px;
    max-width: 80vw;
    padding: 2rem;
  }
}

@media (min-width: 1025px) {
  .header {
    padding: 1rem 3rem;
  }

  .wellcome-box h1 {
    margin: 1rem 3rem;
    padding: 1rem 3rem;
    font-size: 1.8rem;
  }

  .ad-requests {
    padding: 1rem 3rem;
  }
}
</style>
