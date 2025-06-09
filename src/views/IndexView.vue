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
    <div class="box-content">
      <div class="box-text">
        <h2>Conecta paseadores<br />con dueños de perros</h2>
        <p>Encuentra fácilmente paseadores de<br />perros de confianza en tu área.</p>
        <div class="box-btn-empezar">
          <button @click="goToProfile">Empezar 🐾</button>
        </div>
      </div>
      <div class="footer">
        <span>Privacidad</span>
        <span>Términos</span>
        <span>Contacto</span>
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

const goToProfile = () => {
  if (authStore.isLoggedIn && profileRoute.value) {
    router.push(profileRoute.value)
  } else {
    router.push('/login')
  }
}

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

.box-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: start;
  height: 100%;
  width: 100%;
  background-image: url('../assets/index-dog.jpg');
  background-position: center right;
  background-size: contain;
  background-repeat: no-repeat;
  background-color: #39c3e8;
}

.box-text {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 90%;
  width: 50%;
  text-align: center;
  gap: 1rem;
}

.box-text h2 {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 30%;
  font-weight: bold;
  font-size: 50px;
  color: #003978;
  letter-spacing: 1px;
}

.box-text p {
  display: flex;
  justify-content: center;
  align-items: center;
  color: #003978;
  font-size: 25px;
  width: 100%;
  height: 15%;
  letter-spacing: 1px;
}

.box-text .box-btn-empezar {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 20%;
}

.box-btn-empezar button {
  border: none;
  font-size: 20px;
  border-radius: 10px;
  height: 45%;
  width: 25%;
  font-weight: bold;
  color: #003978;
  background-color: #fecf35;
  cursor: pointer;
}

.box-btn-empezar button:hover {
  scale: 1.1;
  box-shadow: #fecf35 2px 2px 10px 2px;
  transition: 0.4s;
}

.footer {
  height: 10%;
  width: 50%;
  text-align: center;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  text-align: center;
  flex-direction: row;
  font-weight: bold;
  color: white;
}

.footer span {
  cursor: pointer;
}

.footer span:hover {
  opacity: 60%;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    height: 30%;
    padding: 1rem;
  }

  .header .box-logo-img,
  .box-btns-navbar {
    width: 100%;
    justify-content: center;
  }

  .header .logo p {
    font-size: 0.9rem;
    width: 100%;
    text-align: center;
  }

  .box-btns-navbar div {
    width: 100%;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }

  .btns a,
  .btns button {
    width: 80%;
    justify-content: center;
    font-size: 0.95rem;
  }

  .box-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    background-position: center bottom;
    background-size: cover;
    padding: 1rem;
    width: 100%;
  }

  .box-text {
    width: 100%;
    padding: 1rem;
    background: rgba(99, 99, 99, 0.175);
    backdrop-filter: blur(6px);
    border-radius: 15px;
    text-align: center;
    color: white;
    gap: 1rem;
  }

  .box-text h2 {
    font-size: 1.5rem;
    height: auto;
    width: 100%;
    color: white;
  }

  .box-text p {
    font-size: 1.1rem;
    height: auto;
    color: white;
  }

  .box-btn-empezar {
    height: auto;
  }

  .box-btn-empezar button {
    width: 60%;
    height: 40px;
    font-size: 1rem;
  }

  .footer {
    width: 100%;
    height: 50px;
    border-radius: 10px;
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.6);
    color: white;
    font-weight: bold;
    font-size: 0.85rem;
    margin-top: auto;
  }
}
</style>
