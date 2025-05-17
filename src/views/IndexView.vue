<template>
  <div>
    <h1>Bienvenido a DogGo!</h1>
    <div v-if="!authStore.isLoggedIn">
      <router-link to="/login">Iniciar sesión</router-link>
      <router-link to="/register">Registrarse</router-link>
    </div>
    <div v-else>
      <router-link v-if="profileRoute" :to="profileRoute">Perfil</router-link>
      <button @click="handleLogout">Cerrar sesión</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { computed } from 'vue'

const authStore = useAuthStore()
const router = useRouter()

const profileRoute = computed(() => {
  if (authStore.userRole) {
    return '/' + authStore.userRole + '-profile'
  }
  return null
})

const handleLogout = () => {
  authStore.logoutUser()
  router.push('/')
}
</script>

<style scoped>
div {
  text-align: center;
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
}

h1 {
  color: #333;
  font-size: 2.5rem;
  margin-bottom: 20px;
}

a,
button {
  display: inline-block;
  padding: 10px 20px;
  margin: 10px;
  text-decoration: none;
  font-size: 1rem;
  font-weight: bold;
  border-radius: 5px;
  transition: opacity 0.3s ease;
}

a:hover,
button:hover {
  opacity: 0.9;
}

a[to='/login'] {
  background-color: #007bff;
  color: white;
}

a[to='/register'] {
  background-color: #28a745;
  color: white;
}

a[to$='-profile'] {
  background-color: #007bff;
  color: white;
}

button {
  background-color: #dc3545;
  color: white;
  border: none;
  cursor: pointer;
}
</style>
