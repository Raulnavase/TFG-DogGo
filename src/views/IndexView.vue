<template>
  <div class="wrapper">
    <div class="circle"></div>
    <div class="text-box">
      <h1>DogGo!</h1>
      <h3>Para ti, por ellos.</h3>
      <div v-if="!authStore.isLoggedIn">
        <router-link to="/login">Iniciar sesión</router-link>
        <router-link to="/register">Registrarse</router-link>
      </div>
      <div v-else>
        <router-link v-if="profileRoute" :to="profileRoute">Perfil</router-link>
        <button @click="handleLogout">Cerrar sesión</button>
      </div>
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
  if (authStore.userRole !== 'admin') {
    return '/' + authStore.userRole + '-profile'
  } else if (authStore.user) {
    return '/admin-panel'
  }
  return null
})

const handleLogout = () => {
  authStore.logoutUser()
  router.push('/')
}
</script>

<style scoped>
.wrapper {
  background-color: rgb(1 213 236);
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  position: relative;
  display: flex;
  justify-content: space-around;
  flex-direction: row;
  text-align: center;
  align-items: center;
}
.circle {
  position: absolute;
  top: 0;
  right: 0;
  width: 50vw;
  height: 100vh;
  background-color: rgb(255 204 1);
  border-top-left-radius: 50vw;
  border-bottom-left-radius: 50vw;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  z-index: 0;
}
.wrapper img {
  top: 0;
  z-index: 1;
  height: 110vh;
  width: 50%;
  margin-bottom: 2rem;
}

.text-box {
  position: relative;
  z-index: 1;
  width: 40%;
  height: 60%;
  padding: 20px;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
}

.wrapper > *:not(.circle) {
  position: relative;
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
