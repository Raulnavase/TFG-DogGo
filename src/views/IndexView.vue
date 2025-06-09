<template>
  <div class="wrapper">
    <header class="header">
      <div class="box-logo-img">
        <div class="logo">
          <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
          <div>
            <h2>DogGo!</h2>
            <p>Para ti, por ellos.</p>
          </div>
        </div>
      </div>
      <div class="box-btns-navbar">
        <div class="btns" v-if="!authStore.isLoggedIn">
          <router-link to="/login">Iniciar sesión</router-link>
          <router-link to="/register">Registrarse</router-link>
        </div>
        <div class="btns" v-else>
          <router-link v-if="profileRoute" :to="profileRoute"
            >Perfil <i class="fa-solid fa-shield-dog"></i
          ></router-link>
          <button @click="handleLogout">
            Cerrar sesión <i class="fa-solid fa-right-from-bracket"></i>
          </button>
        </div>
      </div>
    </header>
    <div class="main"></div>
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
  height: 100vh;
  width: 100vw;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #003978;
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 1rem 2rem;
  height: 20%;
  width: 100%;
}

.header .box-logo-img {
  display: flex;
  align-items: center;
  width: 50%;
}

.header .logo {
  display: flex;
  align-items: center;
}

.header .logo img {
  height: 60px;
  margin-right: 1rem;
}

.header .logo h2 {
  color: #fecf35;
  font-weight: 800;
  font-size: 2rem;
  margin: 0;
}

.header .logo p {
  color: white;
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
  text-align: end;
  width: 25vh;
}

.box-btns-navbar {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 40%;
}

.box-btns-navbar div {
  display: flex;
  justify-content: space-around;
  width: 80%;
}

.btns a,
.btns button {
  background-color: #fecf35;
  color: #003978;
  font-weight: 700;
  font-size: 1rem;
  border: 2px solid #fecf35;
  border-radius: 10px;
  padding: 0.6rem 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  text-decoration: none;
  transition: all 0.2s ease-in-out;
}

.btns button {
  background-color: transparent;
  color: #fecf35;
  border: 2px solid #fecf35;
  cursor: pointer;
}

.btns a:hover,
.btns button:hover {
  opacity: 0.85;
}

.wrapper .main {
  display: flex;
  height: 100%;
  width: 100%;
  background-image: url('../assets/index-dog.jpg');
  background-position: center right;
  background-size: contain;
  background-repeat: no-repeat;
  background-color: #39c3e8;
}
</style>
