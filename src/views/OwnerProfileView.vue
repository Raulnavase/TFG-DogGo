<template>
  <div v-if="authStore.isLoggedIn && authStore.user">
    <header>
      <h1>¡Hola, {{ authStore.userName }}! - Perfil de Dueño</h1>
      <div class="nav-buttons">
        <button @click="goToHome">Inicio</button>
        <button @click="goToActiveWalks">Paseos Activos</button>
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

    <h2>Tus Perros</h2>
    <div v-if="authStore.dogs.length > 0">
      <ul>
        <li v-for="dog in authStore.dogs" :key="dog._id">
          {{ capitalizeFirstLetter(dog.name) }} ({{ capitalizeFirstLetter(dog.breed) }},
          {{ dog.age }} años)
          <button @click="authStore.toggleEditDogForm(dog)">Editar</button>
          <button @click="authStore.showDeleteConfirmation(dog)">Eliminar</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No tienes perros registrados.</p>
    </div>

    <button @click="authStore.toggleAddDogForm">
      {{ authStore.showAddDogForm ? 'Cancelar Agregar Perro' : 'Agregar Perro' }}
    </button>

    <form v-if="authStore.showAddDogForm" @submit.prevent="validateAndAddDog">
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
          @input="handleBreedChange('add')"
        />
      </div>
      <div>
        <label for="add-age">Edad:</label>
        <input type="number" id="add-age" v-model.number="authStore.newDog.age" required />
      </div>
      <button type="submit">Agregar Perro</button>
      <p v-if="authStore.addDogError" class="error-message">{{ authStore.addDogError }}</p>
      <p v-if="authStore.addDogSuccess" class="success-message">{{ authStore.addDogSuccess }}</p>
    </form>

    <form v-if="authStore.showEditDogForm" @submit.prevent="validateAndUpdateDog">
      <h3>Editar Perro</h3>
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
          @input="handleBreedChange('edit')"
        />
      </div>
      <div>
        <label for="edit-age">Edad:</label>
        <input type="number" id="edit-age" v-model.number="authStore.editDog.age" required />
      </div>
      <button type="submit">Guardar Cambios</button>
      <button type="button" @click="authStore.toggleEditDogForm(null)">Cancelar</button>
      <p v-if="authStore.editDogError" class="error-message">{{ authStore.editDogError }}</p>
      <p v-if="authStore.editDogSuccess" class="success-message">{{ authStore.editDogSuccess }}</p>
    </form>

    <div v-if="authStore.showDeleteConfirm" class="confirm-dialog">
      <p>¿Estás seguro de eliminar a {{ authStore.dogToDelete?.name }}?</p>
      <button @click="authStore.deleteDog">Sí, eliminar</button>
      <button @click="authStore.cancelDelete">Cancelar</button>
    </div>

    <h2>Solicitudes enviadas</h2>
    <div v-if="ownerRequestsLoading">Cargando...</div>
    <div v-else-if="ownerRequestsError">{{ ownerRequestsError }}</div>
    <ul v-else>
      <li v-for="req in ownerRequests" :key="req._id">
        {{ req.date }} - {{ req.status }}
        <button v-if="req.status === 'aceptada'" @click="cancelRequest(req._id)">Cancelar</button>
      </li>
    </ul>
  </div>
  <div v-else>
    <p>Cargando perfil...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useDogStore } from '@/stores/dog'
import { requestsGet, requestsPatch } from '../../api/api'

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
    }
  },
)

const fetchOwnerRequests = async () => {
  ownerRequestsLoading.value = true
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
  await requestsPatch(`/${id}/cancel`)
  fetchOwnerRequests()
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

const goToActiveWalks = () => {
  router.push({ name: 'active-walks' })
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

const capitalizeFirstLetter = (string) => {
  if (!string) return string
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase()
}

const handleBreedChange = (formType) => {
  if (formType === 'add') {
    showCustomBreedAdd.value = selectedBreedAdd.value === 'Otra'
    authStore.newDog.breed = showCustomBreedAdd.value
      ? customBreedAdd.value
      : selectedBreedAdd.value
  } else {
    showCustomBreedEdit.value = selectedBreedEdit.value === 'Otra'
    authStore.editDog.breed = showCustomBreedEdit.value
      ? customBreedEdit.value
      : selectedBreedEdit.value
  }
}

const validateAndAddDog = async () => {
  if (!authStore.newDog.name || !authStore.newDog.age || !authStore.newDog.breed) {
    authStore.addDogError = 'Todos los campos son obligatorios, incluida la raza.'
    return
  }
  await authStore.addDog()
}

const validateAndUpdateDog = async () => {
  if (!authStore.editDog.name || !authStore.editDog.age || !authStore.editDog.breed) {
    authStore.editDogError = 'Todos los campos son obligatorios, incluida la raza.'
    return
  }
  await authStore.updateDog()
}

onMounted(async () => {
  fetchOwnerRequests()
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else {
    await authStore.fetchDogs()
    await fetchBreeds()
  }
})

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'index' })
}
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
.breed-select,
.custom-breed-input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  width: 100%;
}
.breed-select option,
.custom-breed-input {
  background-color: #fff;
  color: #333;
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
</style>
