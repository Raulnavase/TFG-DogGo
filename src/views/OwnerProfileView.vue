<style scoped></style>

<template>
  <div>
    <h1>Perfil de {{ userName }}</h1>
    <button @click="logout">Cerrar sesión</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../../api/api'

const router = useRouter()
const userName = ref(localStorage.getItem('userName') || 'Usuario')

const logout = async () => {
  try {
    const response = await api.post('/logout')
    if (response.status === 200) {
      console.log('Cierre de sesión exitoso desde el backend')
    }
  } catch (error) {
    console.error('Error al cerrar sesión en el backend:', error)
  } finally {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('userRole')
    localStorage.removeItem('userName')
    console.log('Cierre de sesión completado en el frontend')
    router.push('/')
  }
}
</script>
