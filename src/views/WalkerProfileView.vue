<style scoped></style>

<template>
  <div v-if="authStore.isLoggedIn && authStore.user">
    <h1>¡Hola, {{ authStore.userName }}! - Perfil de Paseador</h1>
    <button @click="logout">Cerrar sesión</button>
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

onMounted(() => {
  authStore.initializeAuth()
  if (!authStore.isLoggedIn) {
    router.push({ name: 'login' })
  }
})

const logout = async () => {
  await authStore.logoutUser()
  router.push({ name: 'index' })
}
</script>
