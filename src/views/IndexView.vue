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

<style scoped></style>
