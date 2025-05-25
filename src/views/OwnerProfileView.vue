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
        <ul>
          <li><strong>Nombre:</strong> {{ authStore.user?.name }}</li>
          <li><strong>Apellido:</strong> {{ authStore.user?.last_name }}</li>
          <li><strong>Email:</strong> {{ authStore.user?.email }}</li>
          <li><strong>Rol:</strong> {{ authStore.user?.role }}</li>
        </ul>
        <button class="delete-btn" @click="confirmDelete = true">Eliminar cuenta</button>
        <button @click="showPersonalInfo = false">Cerrar</button>
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

    <h2>Paseos Programados</h2>
    <div v-if="bookings.length > 0">
      <ul>
        <li v-for="booking in bookings" :key="booking._id">
          Paseo con {{ booking.walker_name }} el {{ formatDate(booking.date) }} para
          {{ booking.dog_name }}
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No tienes paseos programados.</p>
      <button @click="goToActiveWalks">Buscar paseos</button>
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
import { useDogStore } from '@/stores/dog'
import { bookingsGet } from '../../api/api'

const router = useRouter()
const authStore = useAuthStore()
const dogStore = useDogStore()
const showPersonalInfo = ref(false)
const confirmDelete = ref(false)

const breeds = ref([])
const showCustomBreedAdd = ref(false)
const showCustomBreedEdit = ref(false)
const customBreedAdd = ref('')
const customBreedEdit = ref('')
const selectedBreedAdd = ref('')
const selectedBreedEdit = ref('')
const bookings = ref([])

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

const fetchBookings = async () => {
  try {
    const response = await bookingsGet('/owner')
    bookings.value = response.data
  } catch (error) {
    console.error('Error al cargar paseos:', error.response?.data?.msg || error.message)
  }
}

const capitalizeFirstLetter = (string) => {
  if (!string) return string
  return string.charAt(0).toUpperCase() + string.slice(1).toLowerCase()
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long', year: 'numeric' })
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
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else {
    await authStore.fetchDogs()
    await fetchBreeds()
    await fetchBookings()
  }
})

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'index' })
}
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
