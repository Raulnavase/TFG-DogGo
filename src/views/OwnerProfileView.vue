<template>
  <div v-if="authStore.isLoggedIn && authStore.user">
    <h1>¡Hola, {{ authStore.userName }}! - Perfil de Dueño</h1>
    <button @click="logout">Cerrar sesión</button>

    <h2>Tus Perros</h2>
    <div v-if="authStore.dogs.length > 0">
      <ul>
        <li v-for="dog in authStore.dogs" :key="dog._id">
          {{ dog.name }} ({{ dog.breed }}, {{ dog.age }} años)
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No tienes perros registrados.</p>
    </div>

    <button @click="authStore.toggleAddDogForm">
      {{ authStore.showAddDogForm ? 'Cancelar Agregar Perro' : 'Agregar Perro' }}
    </button>

    <form v-if="authStore.showAddDogForm" @submit.prevent="authStore.addDog">
      <div>
        <label for="name">Nombre:</label>
        <input type="text" id="name" v-model="authStore.newDog.name" required />
      </div>
      <div>
        <label for="breed">Raza:</label>
        <input type="text" id="breed" v-model="authStore.newDog.breed" required />
      </div>
      <div>
        <label for="age">Edad:</label>
        <input type="number" id="age" v-model.number="authStore.newDog.age" required />
      </div>
      <button type="submit">Agregar Perro</button>
      <p v-if="authStore.addDogError" class="error-message">{{ authStore.addDogError }}</p>
      <p v-if="authStore.addDogSuccess" class="success-message">{{ authStore.addDogSuccess }}</p>
    </form>
  </div>
  <div v-else>
    <p>Cargando perfil...</p>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  } else {
    await authStore.fetchDogs() // Cargar perros al montar
  }
})

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'index' })
}
</script>

<style scoped></style>
