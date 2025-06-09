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
        <button @click="logout">Cerrar sesión</button>
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

        <form v-if="authStore.showAddDogForm" @submit.prevent="validateAndAddDog">
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
            <form @submit.prevent="validateAndUpdateDog">
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

// --- Status Text Helper ---
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

// --- Vue Router and Stores ---
const router = useRouter()
const authStore = useAuthStore()
const dogStore = useDogStore()

// --- Personal Info Modal State ---
const showPersonalInfo = ref(false)
const editPersonal = ref(false)
const showChangePassword = ref(false)
const confirmDelete = ref(false) // Para la eliminación de cuenta

// --- Personal Info Data ---
const editName = ref(authStore.user?.name || '')
const editLastName = ref(authStore.user?.last_name || '')
const editEmail = ref(authStore.user?.email || '')
const personalError = ref('')
const personalSuccess = ref('')

// --- Password Change Data ---
const passwordError = ref('')
const passwordSuccess = ref('')
const oldPassword = ref('')
const newPassword = ref('')
const repeatNewPassword = ref('')

// --- Dog Breed Data and State ---
const breeds = ref([])
const showCustomBreedAdd = ref(false)
const showCustomBreedEdit = ref(false)
const customBreedAdd = ref('')
const customBreedEdit = ref('')
const selectedBreedAdd = ref('')
const selectedBreedEdit = ref('')

// --- Owner Requests Data ---
const ownerRequests = ref([])
const ownerRequestsLoading = ref(false)
const ownerRequestsError = ref('')

// --- Watcher for Personal Info Modal ---
watch(
  () => showPersonalInfo.value,
  (val) => {
    if (val && authStore.user) {
      editName.value = authStore.user.name
      editLastName.value = authStore.user.last_name
      editEmail.value = authStore.user.email
      // Reset success/error messages when opening modal
      personalError.value = ''
      personalSuccess.value = ''
      passwordError.value = ''
      passwordSuccess.value = ''
      editPersonal.value = false // Ensure personal info view is default
      showChangePassword.value = false // Ensure password change view is hidden
    }
  },
)

// --- Watcher for Edit Dog Form ---
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
      // Reset when edit dog form is closed
      selectedBreedEdit.value = ''
      customBreedEdit.value = ''
      showCustomBreedEdit.value = false
    }
  },
)

// --- Fetch Owner Requests ---
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

// --- Request Actions ---
const cancelRequest = async (id) => {
  try {
    await requestsPatch(`/${id}/cancel`)
    fetchOwnerRequests() // Refresh requests after cancellation
  } catch (e) {
    console.error('Error al cancelar la solicitud:', e)
    alert(e?.response?.data?.msg || 'Error al cancelar la solicitud')
  }
}

const deleteRequest = async (id) => {
  try {
    await requestsDelete(`/${id}`)
    fetchOwnerRequests() // Refresh requests after deletion
  } catch (e) {
    console.error('Error al eliminar la solicitud:', e)
    alert(e?.response?.data?.msg || 'Error al eliminar la solicitud')
  }
}

// --- Personal Data Actions ---
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
  // Reset fields to current user data if canceled
  editName.value = authStore.user?.name || ''
  editLastName.value = authStore.user?.last_name || ''
  editEmail.value = authStore.user?.email || ''
}

// --- Password Change Actions ---
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

// --- Navigation ---
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

// --- Account Deletion ---
const deleteAccount = async () => {
  try {
    await authStore.deleteUserAccount()
    router.push({ name: 'index' })
  } catch (e) {
    alert(e?.response?.data?.msg || 'Error al eliminar la cuenta')
  } finally {
    confirmDelete.value = false // Close confirmation dialog
  }
}

// --- Breed Management ---
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
      customBreedAdd.value = '' // Clear custom breed if not 'Otra'
    } else {
      authStore.newDog.breed = customBreedAdd.value // Set to custom breed if 'Otra' is selected
    }
  } else {
    showCustomBreedEdit.value = selectedBreedEdit.value === 'Otra'
    if (!showCustomBreedEdit.value) {
      authStore.editDog.breed = selectedBreedEdit.value
      customBreedEdit.value = '' // Clear custom breed if not 'Otra'
    } else {
      authStore.editDog.breed = customBreedEdit.value // Set to custom breed if 'Otra' is selected
    }
  }
}

// Update the dog breed reactivity when the custom breed input changes.
const handleCustomBreedInput = (formType) => {
  if (formType === 'add') {
    authStore.newDog.breed = customBreedAdd.value
  } else {
    authStore.editDog.breed = customBreedEdit.value
  }
}

// --- Dog Form Validations ---
const validateAndAddDog = async () => {
  // Ensure the breed is set correctly from either the select or the custom input
  if (selectedBreedAdd.value === 'Otra') {
    authStore.newDog.breed = customBreedAdd.value
  } else {
    authStore.newDog.breed = selectedBreedAdd.value
  }

  if (!authStore.newDog.name || !authStore.newDog.age || !authStore.newDog.breed) {
    authStore.addDogError = 'Todos los campos son obligatorios, incluida la raza.'
    authStore.addDogSuccess = '' // Clear success message on error
    return
  }

  // Basic validation for age
  if (authStore.newDog.age <= 0) {
    authStore.addDogError = 'La edad debe ser un número positivo.'
    authStore.addDogSuccess = ''
    return
  }

  await authStore.addDog()
  if (authStore.addDogSuccess) {
    // Reset form fields after successful addition
    selectedBreedAdd.value = ''
    customBreedAdd.value = ''
    showCustomBreedAdd.value = false
  }
}

const validateAndUpdateDog = async () => {
  // Ensure the breed is set correctly from either the select or the custom input
  if (selectedBreedEdit.value === 'Otra') {
    authStore.editDog.breed = customBreedEdit.value
  } else {
    authStore.editDog.breed = selectedBreedEdit.value
  }

  if (!authStore.editDog.name || !authStore.editDog.age || !authStore.editDog.breed) {
    authStore.editDogError = 'Todos los campos son obligatorios, incluida la raza.'
    authStore.editDogSuccess = '' // Clear success message on error
    return
  }

  // Basic validation for age
  if (authStore.editDog.age <= 0) {
    authStore.editDogError = 'La edad debe ser un número positivo.'
    authStore.editDogSuccess = ''
    return
  }

  await authStore.updateDog()
  if (authStore.editDogSuccess) {
    // Reset form fields after successful update
    selectedBreedEdit.value = ''
    customBreedEdit.value = ''
    showCustomBreedEdit.value = false
  }
}

// --- Utility: Capitalize First Letter ---
const capitalize = (str) => (str ? str.charAt(0).toUpperCase() + str.slice(1).toLowerCase() : '')

// --- On Mounted Lifecycle Hook ---
onMounted(async () => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else {
    await authStore.fetchDogs()
    await fetchBreeds()
    fetchOwnerRequests() // Fetch requests once the user is logged in
  }
})
</script>

<style scoped>
/* Reseteo para el scroll global */
html,
body {
  margin: 0;
  padding: 0;
  overflow: hidden; /* ¡Importante! Elimina el scroll del html y body */
  height: 100%; /* Asegura que ocupen toda la altura */
  width: 100%; /* Asegura que ocupen todo el ancho */
}

/* GENERAL LAYOUT & HEADER */
.wrapper {
  height: 100vh; /* Ocupa el 100% del viewport height */
  width: 100vw; /* Ocupa el 100% del viewport width */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* ¡Importante! Elimina el scroll del wrapper */
}

.header {
  background-color: #003978;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  flex-shrink: 0; /* Asegura que el header no se encoja */
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

.box-btns-navbar button {
  background-color: #fecf35;
  color: #003978;
  border: none;
  border-radius: 10px;
  font-weight: bold;
  margin-left: 0.5rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
}

.box-btns-navbar button:hover {
  opacity: 0.9;
}

.wellcome-box h1 {
  margin: 1rem 2rem;
  padding: 1rem 2rem;
  font-size: 1.5rem;
  flex-shrink: 0; /* Asegura que el título no se encoja */
}

.main {
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* Permite que el main ocupe el espacio restante */
  overflow: hidden; /* Evita el scroll en el main, el scroll estará en sub-elementos */
}

.dogs-requests {
  display: flex;
  flex-direction: row;
  width: 100%;
  flex-grow: 1; /* Asegura que esta sección ocupe el espacio disponible */
  gap: 2rem;
  padding: 1rem 2rem;
  overflow: hidden; /* Evita scroll en este contenedor, el scroll estará en sub-elementos */
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
  flex-shrink: 0; /* Asegura que el título no se encoja */
}

/* Estilo para el botón "Agregar Perro" dentro del h2 (estilo corporativo) */
.btn-add-dog {
  background-color: #fecf35; /* Color amarillo corporativo */
  color: #003978; /* Color azul corporativo */
  border: none;
  border-radius: 10px;
  font-weight: bold;
  padding: 0.3rem 0.8rem;
  font-size: 0.9rem;
  cursor: pointer;
  margin: 0; /* Asegura que no tenga márgenes adicionales */
  transition:
    background-color 0.2s ease,
    transform 0.1s ease;
}

.btn-add-dog:hover {
  background-color: #ffda6a; /* Amarillo más claro al pasar el ratón */
  transform: translateY(-1px); /* Efecto ligero de levantamiento */
}

/* Contenedor para la lista de perros con scroll */
.dogs-list-container,
.requests-list-container {
  flex-grow: 1; /* Permite que este contenedor ocupe el espacio restante */
  overflow-y: auto; /* Habilita el scroll vertical si es necesario */
  padding-right: 0.5rem; /* Pequeño padding para el scrollbar */
  scrollbar-width: thin; /* Para Firefox */
  scrollbar-color: #003978 #f0f0f0; /* Para Firefox */
}

/* Estilos para el scrollbar en Webkit (Chrome, Safari, Edge) */
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

/* --- Estilos para las Tarjetas de Perro --- */
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

/* --- FIN Estilos para las Tarjetas de Perro --- */

/* General button styling */
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
  margin-top: 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  flex-shrink: 0; /* Evita que el formulario se encoja */
}

/* Ajuste específico para formularios dentro de modales, para que no tengan el background y box-shadow del formulario por defecto */
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

/* Estilos para el nuevo div de botones dentro del formulario */
.form-actions {
  display: flex;
  justify-content: center; /* Centra los botones horizontalmente */
  gap: 1rem; /* Espacio entre los botones */
  margin-top: 1rem; /* Margen superior para separarlo de los inputs */
}

.form-actions button {
  flex-grow: 1; /* Permite que los botones ocupen el espacio disponible de forma equitativa */
  max-width: 150px; /* Limita el ancho máximo para que no sean demasiado grandes */
  margin: 0; /* Elimina los márgenes predeterminados para que `gap` funcione */
}

/* MODALES */
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
}

.modal-content {
  background: white;
  padding: 2.5rem;
  border-radius: 1rem;
  min-width: 350px;
  max-width: 90vw;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
  gap: 1rem;
  /* Propiedades para centrado absoluto */
  position: absolute; /* Usamos absolute dentro de fixed para que se posicione respecto al overlay */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.modal-content h2,
.modal-content h3 {
  /* Añadido h3 para los títulos de formularios dentro de modales */
  text-align: center;
  margin-bottom: 1.5rem;
  border-bottom: none;
  width: auto;
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

/* Este modal también debe centrarse. Lo unificamos con .modal-overlay */
/* He cambiado la clase del diálogo de confirmación de perro de `confirm-dialog` a `modal-overlay confirm-dog-delete` para que use la misma base de centrado */
.confirm-dog-delete .modal-content {
  /* No necesitamos redefinir el centrado aquí, ya lo hereda de .modal-content */
}

/* Nuevo estilo para los botones del modal de confirmación de eliminación de perro */
.confirm-dialog-actions {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem; /* Espacio superior para separarlo del texto */
}

.confirm-dialog-actions button {
  margin: 0; /* Elimina los márgenes predeterminados del botón */
  flex-grow: 1;
  max-width: 150px;
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

/* LISTA DE SOLICITUDES */
.request-cards-list {
  display: grid;
  grid-template-columns: repeat(
    auto-fill,
    minmax(280px, 1fr)
  ); /* Más ancho para contenido de solicitud */
  gap: 1.5rem;
  padding: 0;
  list-style: none;
  margin-top: 1.5rem;
}

.request-card {
  background-color: #e0f7fa; /* Un tono diferente para diferenciarlas */
  border-radius: 15px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  padding: 1.2rem;
  padding-bottom: 2.2rem; /* Aumentado aún más el padding inferior */
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
  font-weight: normal; /* Para que la fecha no sea negrita por defecto */
}

.request-info .request-status {
  font-weight: bold;
  padding: 0.2rem 0.6rem;
  border-radius: 8px;
  font-size: 0.85rem;
  display: inline-block; /* Para que el padding funcione bien */
  margin-left: 0.5rem;
}

/* Colores de estado */
.request-status.pendiente {
  background-color: #ffc107; /* Amarillo */
  color: #333;
}
.request-status.aceptada {
  background-color: #28a745; /* Verde */
  color: white;
}
.request-status.rechazada,
.request-status.cancelada_por_owner,
.request-status.cancelada_por_walker {
  background-color: #dc3545; /* Rojo */
  color: white;
}

.request-dogs {
  margin-top: 1rem;
  padding-top: 0.8rem;
  border-top: 1px dashed #b3e0e9;
}

.request-dogs ul {
  padding-left: 1.2rem;
  list-style: disc; /* Vuelven los puntos para las listas de perros */
  margin-top: 0.5rem;
}

.request-dogs ul li {
  background-color: transparent; /* Anula el background de la tarjeta principal */
  padding: 0.2rem 0;
  font-size: 0.9rem;
  box-shadow: none;
  margin-left: 0; /* Asegura que la lista interna no tenga sangría adicional */
  list-style-type: disc; /* Asegura que se vean los bullets */
  align-items: baseline; /* Alinea el texto con el bullet */
}

.request-actions {
  display: flex;
  justify-content: flex-end; /* Alinea los botones a la derecha */
  gap: 0.5rem;
  margin-top: auto; /* Empuja los botones al final de la tarjeta */
  padding-top: 1rem;
  border-top: 1px solid #cce5ff;
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
</style>
