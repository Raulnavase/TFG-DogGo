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
        <button @click="goToActiveWalks">Paseos Activos</button>
        <button @click="logout">
          Cerrar sesión <i class="fa-solid fa-right-from-bracket"></i>
        </button>
        <button @click="showPersonalInfo = true">Información personal</button>
      </div>
    </header>

    <div class="main">
      <div class="wellcome-box">
        <h1>¡Hola, {{ authStore.userName }}! - Perfil de Dueño</h1>
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
              <div class="form-actions">
                <button type="submit">Guardar</button>
                <button type="button" @click="cancelEditPersonal">Cancelar</button>
              </div>
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
              <div class="form-actions">
                <button type="submit">Cambiar contraseña</button>
                <button type="button" @click="showChangePassword = false">Cancelar</button>
              </div>
              <p v-if="passwordError" class="error-message">{{ passwordError }}</p>
              <p v-if="passwordSuccess" class="success-message">{{ passwordSuccess }}</p>
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

      <div class="dogs-requests">
        <div class="box-mydogs">
          <h2>
            Mis Perros
            <button @click="authStore.toggleAddDogForm" class="btn-add-dog">
              {{ authStore.showAddDogForm ? 'Cancelar Agregar Perro' : 'Agregar Perro' }}
            </button>
          </h2>
          <div class="dogs-list-container">
            <div v-if="authStore.dogs.length > 0">
              <ul class="dog-cards-list">
                <li v-for="dog in authStore.dogs" :key="dog._id" class="dog-card">
                  <div class="dog-card-info">
                    <h3>{{ capitalize(dog.name) }}</h3>
                    <p class="dog-breed">{{ capitalize(dog.breed) }}</p>
                    <p class="dog-age">{{ dog.age }} años</p>
                  </div>
                  <div class="dog-card-actions">
                    <button @click="authStore.toggleEditDogForm(dog)">Editar</button>
                    <button @click="authStore.showDeleteConfirmation(dog)">Eliminar</button>
                  </div>
                </li>
              </ul>
            </div>
            <div v-else>
              <p>No tienes perros registrados.</p>
            </div>
          </div>
        </div>

        <form
          v-if="authStore.showAddDogForm"
          @submit.prevent="validateAndAddDog"
          class="add-dog-form"
        >
          <h3>Agregar Nuevo Perro</h3>
          <div>
            <label for="add-name">Nombre:</label>
            <input type="text" id="add-name" v-model="authStore.newDog.name" required />
          </div>
          <div>
            <label for="add-breed">Raza:</label>
            <select
              id="add-breed"
              v-model="selectedBreedAdd"
              class="breed-select"
              @change="handleBreedChange('add')"
            >
              <option value="" disabled>Selecciona una raza</option>
              <option v-for="breed in breeds" :key="breed" :value="breed">{{ breed }}</option>
              <option value="Otra">Otra</option>
            </select>
            <input
              v-if="showCustomBreedAdd"
              type="text"
              id="add-custom-breed"
              v-model="customBreedAdd"
              placeholder="Escribe la raza"
              class="custom-breed-input"
              @input="handleCustomBreedInput('add')"
            />
          </div>
          <div>
            <label for="add-age">Edad:</label>
            <input type="number" id="add-age" v-model.number="authStore.newDog.age" required />
          </div>
          <div class="form-actions">
            <button type="submit">Agregar Perro</button>
          </div>
          <p v-if="authStore.addDogError" class="error-message">{{ authStore.addDogError }}</p>
          <p v-if="authStore.addDogSuccess" class="success-message">
            {{ authStore.addDogSuccess }}
          </p>
        </form>

        <div v-if="authStore.showEditDogForm" class="modal-overlay">
          <div class="modal-content">
            <h3>Editar Perro</h3>
            <form @submit.prevent="validateAndUpdateDog" class="edit-dog-form">
              <div>
                <label for="edit-name">Nombre:</label>
                <input type="text" id="edit-name" v-model="authStore.editDog.name" required />
              </div>
              <div>
                <label for="edit-breed">Raza:</label>
                <select
                  id="edit-breed"
                  v-model="selectedBreedEdit"
                  class="breed-select"
                  @change="handleBreedChange('edit')"
                >
                  <option value="" disabled>Selecciona una raza</option>
                  <option v-for="breed in breeds" :key="breed" :value="breed">{{ breed }}</option>
                  <option value="Otra">Otra</option>
                </select>
                <input
                  v-if="showCustomBreedEdit"
                  type="text"
                  id="edit-custom-breed"
                  v-model="customBreedEdit"
                  placeholder="Escribe la raza"
                  class="custom-breed-input"
                  @input="handleCustomBreedInput('edit')"
                />
              </div>
              <div>
                <label for="edit-age">Edad:</label>
                <input
                  type="number"
                  id="edit-age"
                  v-model.number="authStore.editDog.age"
                  required
                />
              </div>
              <div class="form-actions">
                <button type="submit">Guardar Cambios</button>
                <button type="button" @click="authStore.toggleEditDogForm(null)">Cancelar</button>
              </div>
              <p v-if="authStore.editDogError" class="error-message">
                {{ authStore.editDogError }}
              </p>
              <p v-if="authStore.editDogSuccess" class="success-message">
                {{ authStore.editDogSuccess }}
              </p>
            </form>
          </div>
        </div>

        <div v-if="authStore.showDeleteConfirm" class="modal-overlay confirm-dog-delete">
          <div class="modal-content">
            <p>¿Estás seguro de eliminar a {{ authStore.dogToDelete?.name }}?</p>
            <div class="confirm-dialog-actions">
              <button @click="authStore.deleteDog" class="delete-btn">Sí, eliminar</button>
              <button @click="authStore.cancelDelete">Cancelar</button>
            </div>
          </div>
        </div>

        <div class="box-requests">
          <h2>Solicitudes enviadas</h2>
          <div class="requests-list-container">
            <div v-if="ownerRequestsLoading">Cargando...</div>
            <div v-else-if="ownerRequestsError" class="error-message">{{ ownerRequestsError }}</div>
            <ul v-else-if="ownerRequests.length > 0" class="request-cards-list">
              <li v-for="req in ownerRequests" :key="req._id" class="request-card">
                <div class="request-info">
                  <p>
                    <strong>Paseador:</strong>
                    {{ capitalize(req.walker_info?.name) }}
                    {{ capitalize(req.walker_info?.last_name) }}
                    <span class="walker-email">({{ req.walker_info?.email }})</span>
                  </p>
                  <p>
                    <strong>Fecha:</strong> <span class="request-date">{{ req.date }}</span>
                  </p>
                  <p>
                    <strong>Estado:</strong>
                    <span :class="['request-status', req.status]">{{
                      statusText(req.status)
                    }}</span>
                  </p>
                  <div class="request-dogs">
                    <strong>Perros:</strong>
                    <ul>
                      <li v-for="dog in req.dogs_info" :key="dog._id">
                        {{ capitalize(dog.name) }} ({{ capitalize(dog.breed) }}, {{ dog.age }} años)
                      </li>
                    </ul>
                  </div>
                </div>
                <div class="request-actions">
                  <button v-if="req.status === 'pendiente'" @click="cancelRequest(req._id)">
                    Cancelar
                  </button>
                  <button v-else-if="req.status === 'aceptada'" @click="cancelRequest(req._id)">
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
              <p>No hay solicitudes enviadas.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useDogStore } from '@/stores/dog'
import { requestsGet, requestsPatch, requestsDelete } from '../../api/api'

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

const router = useRouter()
const authStore = useAuthStore()
const dogStore = useDogStore()

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

const breeds = ref([])
const showCustomBreedAdd = ref(false)
const showCustomBreedEdit = ref(false)
const customBreedAdd = ref('')
const customBreedEdit = ref('')
const selectedBreedAdd = ref('')
const selectedBreedEdit = ref('')

const ownerRequests = ref([])
const ownerRequestsLoading = ref(false)
const ownerRequestsError = ref('')

watch(
  () => showPersonalInfo.value,
  (val) => {
    if (val && authStore.user) {
      editName.value = authStore.user.name
      editLastName.value = authStore.user.last_name
      editEmail.value = authStore.user.email
      personalError.value = ''
      personalSuccess.value = ''
      passwordError.value = ''
      passwordSuccess.value = ''
      editPersonal.value = false
      showChangePassword.value = false
    }
  },
)

watch(
  () => authStore.showEditDogForm,
  (val) => {
    if (val && authStore.editDog) {
      const currentBreed = authStore.editDog.breed
      if (breeds.value.includes(currentBreed)) {
        selectedBreedEdit.value = currentBreed
        showCustomBreedEdit.value = false
        customBreedEdit.value = ''
      } else {
        selectedBreedEdit.value = 'Otra'
        showCustomBreedEdit.value = true
        customBreedEdit.value = currentBreed
      }
    } else {
      selectedBreedEdit.value = ''
      customBreedEdit.value = ''
      showCustomBreedEdit.value = false
    }
  },
)

const fetchOwnerRequests = async () => {
  ownerRequestsLoading.value = true
  ownerRequestsError.value = ''
  try {
    const res = await requestsGet('/owner')
    ownerRequests.value = res.data
  } catch (e) {
    ownerRequestsError.value = e?.response?.data?.msg || 'Error al cargar solicitudes'
  } finally {
    ownerRequestsLoading.value = false
  }
}

const cancelRequest = async (id) => {
  try {
    await requestsPatch(`/${id}/cancel`)
    fetchOwnerRequests()
  } catch (e) {
    console.error('Error al cancelar la solicitud:', e)
    alert(e?.response?.data?.msg || 'Error al cancelar la solicitud')
  }
}

const deleteRequest = async (id) => {
  try {
    await requestsDelete(`/${id}`)
    fetchOwnerRequests()
  } catch (e) {
    console.error('Error al eliminar la solicitud:', e)
    alert(e?.response?.data?.msg || 'Error al eliminar la solicitud')
  }
}

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
  editName.value = authStore.user?.name || ''
  editLastName.value = authStore.user?.last_name || ''
  editEmail.value = authStore.user?.email || ''
}

const changePassword = async () => {
  passwordError.value = ''
  passwordSuccess.value = ''
  if (newPassword.value !== repeatNewPassword.value) {
    passwordError.value = 'Las contraseñas nuevas no coinciden'
    return
  }
  if (newPassword.value.length < 6) {
    passwordError.value = 'La nueva contraseña debe tener al menos 6 caracteres.'
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

const goToActiveWalks = () => {
  router.push({ name: 'active-walks' })
}

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'index' })
}

const deleteAccount = async () => {
  try {
    await authStore.deleteUserAccount()
    router.push({ name: 'index' })
  } catch (e) {
    alert(e?.response?.data?.msg || 'Error al eliminar la cuenta')
  } finally {
    confirmDelete.value = false
  }
}

const fetchBreeds = async () => {
  if (dogStore.breeds.length === 0) {
    try {
      const response = await fetch('https://dog.ceo/api/breeds/list/all')
      const data = await response.json()
      const breedList = Object.keys(data.message).map(
        (breed) => breed.charAt(0).toUpperCase() + breed.slice(1).toLowerCase(),
      )
      dogStore.setBreeds(breedList)
    } catch (error) {
      console.error('Error al cargar las razas:', error)
    }
  }
  breeds.value = dogStore.breeds
}

const handleBreedChange = (formType) => {
  if (formType === 'add') {
    showCustomBreedAdd.value = selectedBreedAdd.value === 'Otra'
    if (!showCustomBreedAdd.value) {
      authStore.newDog.breed = selectedBreedAdd.value
      customBreedAdd.value = ''
    } else {
      authStore.newDog.breed = customBreedAdd.value
    }
  } else {
    showCustomBreedEdit.value = selectedBreedEdit.value === 'Otra'
    if (!showCustomBreedEdit.value) {
      authStore.editDog.breed = selectedBreedEdit.value
      customBreedEdit.value = ''
    } else {
      authStore.editDog.breed = customBreedEdit.value
    }
  }
}

const handleCustomBreedInput = (formType) => {
  if (formType === 'add') {
    authStore.newDog.breed = customBreedAdd.value
  } else {
    authStore.editDog.breed = customBreedEdit.value
  }
}

const validateAndAddDog = async () => {
  if (selectedBreedAdd.value === 'Otra') {
    authStore.newDog.breed = customBreedAdd.value
  } else {
    authStore.newDog.breed = selectedBreedAdd.value
  }

  if (!authStore.newDog.name || !authStore.newDog.age || !authStore.newDog.breed) {
    authStore.addDogError = 'Todos los campos son obligatorios, incluida la raza.'
    authStore.addDogSuccess = ''
    return
  }

  if (authStore.newDog.age <= 0) {
    authStore.addDogError = 'La edad debe ser un número positivo.'
    authStore.addDogSuccess = ''
    return
  }

  await authStore.addDog()
  if (authStore.addDogSuccess) {
    selectedBreedAdd.value = ''
    customBreedAdd.value = ''
    showCustomBreedAdd.value = false
  }
}

const validateAndUpdateDog = async () => {
  if (selectedBreedEdit.value === 'Otra') {
    authStore.editDog.breed = customBreedEdit.value
  } else {
    authStore.editDog.breed = selectedBreedEdit.value
  }

  if (!authStore.editDog.name || !authStore.editDog.age || !authStore.editDog.breed) {
    authStore.editDogError = 'Todos los campos son obligatorios, incluida la raza.'
    authStore.editDogSuccess = ''
    return
  }

  if (authStore.editDog.age <= 0) {
    authStore.editDogError = 'La edad debe ser un número positivo.'
    authStore.editDogSuccess = ''
    return
  }

  await authStore.updateDog()
  if (authStore.editDogSuccess) {
    selectedBreedEdit.value = ''
    customBreedEdit.value = ''
    showCustomBreedEdit.value = false
  }
}

const capitalize = (str) => (str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : '')

onMounted(async () => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else {
    await authStore.fetchDogs()
    await fetchBreeds()
    fetchOwnerRequests()
  }
})
</script>

<style scoped>
.wrapper {
  height: 100vh;
  width: 100vw;
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
  overflow: hidden;
}

.dogs-requests {
  display: flex;
  flex-direction: row;
  width: 100%;
  flex-grow: 1;
  gap: 2rem;
  padding: 1rem 2rem;
  overflow: hidden;
}

.box-mydogs,
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

.btn-add-dog {
  background-color: #fecf35;
  color: #003978;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  padding: 0.3rem 0.8rem;
  font-size: 0.9rem;
  cursor: pointer;
  margin: 0;
  transition:
    background-color 0.2s ease,
    transform 0.1s ease;
  white-space: nowrap;
}

.btn-add-dog:hover {
  background-color: #ffda6a;
  transform: translateY(-1px);
}

.dogs-list-container,
.requests-list-container {
  flex-grow: 1;
  overflow-y: auto;
  padding-right: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: #003978 #f0f0f0;
}

.dogs-list-container::-webkit-scrollbar,
.requests-list-container::-webkit-scrollbar {
  width: 8px;
}

.dogs-list-container::-webkit-scrollbar-track,
.requests-list-container::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 10px;
}

.dogs-list-container::-webkit-scrollbar-thumb,
.requests-list-container::-webkit-scrollbar-thumb {
  background-color: #003978;
  border-radius: 10px;
  border: 2px solid #f0f0f0;
}

.dog-cards-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1.5rem;
  padding: 0;
  list-style: none;
  margin-top: 1.5rem;
}

.dog-card {
  background-color: #f0f8ff;
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  transition:
    transform 0.2s ease-in-out,
    box-shadow 0.2s ease-in-out;
  padding: 1rem;
}

.dog-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.dog-card-info {
  padding: 0.5rem 0;
  flex-grow: 1;
}

.dog-card-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  color: #003978;
  border-bottom: none;
  width: auto;
}

.dog-card-info .dog-breed {
  font-size: 0.9rem;
  color: #555;
  margin-bottom: 0.3rem;
}

.dog-card-info .dog-age {
  font-size: 0.8rem;
  color: #777;
  margin-bottom: 0;
}

.dog-card-actions {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  padding-top: 0.5rem;
  width: 100%;
}

.dog-card-actions button {
  flex: 1;
  padding: 0.4rem 0.8rem;
  font-size: 0.85rem;
  margin: 0;
  background-color: #fecf35;
  color: #003978;
  border-radius: 8px;
}

.dog-card-actions button:last-child {
  background-color: #dc3545;
  color: white;
}
.dog-card-actions button:last-child:hover {
  background-color: #c82333;
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
select {
  padding: 0.7rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: 100%;
  box-sizing: border-box;
}

.breed-select,
.custom-breed-input {
  margin-top: 0.5rem;
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
}

.request-info strong {
  color: #003978;
  font-weight: 600;
  margin-right: 0.3rem;
}

.request-info .walker-email {
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

  .dogs-requests {
    flex-direction: column;
    padding: 1rem;
    gap: 1.5rem;
    overflow-y: auto;
  }

  .box-mydogs,
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

  h2 .btn-add-dog {
    margin-top: 0.8rem;
    width: 100%;
    max-width: 250px;
    align-self: center;
  }

  .dog-cards-list {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .dog-card {
    padding: 0.8rem;
  }

  .dog-card-actions {
    flex-direction: column;
    gap: 0.8rem;
  }

  .dog-card-actions button {
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

  .dogs-requests {
    flex-direction: column;
    padding: 1rem 1.5rem;
    gap: 1.5rem;
  }

  .box-mydogs,
  .box-requests {
    min-width: auto;
  }

  .dog-cards-list {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
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

  .dogs-requests {
    padding: 1rem 3rem;
  }
}
</style>
