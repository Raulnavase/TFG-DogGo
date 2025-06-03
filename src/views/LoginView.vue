<template>
  <div class="container">
    <div class="box-form">
      <form class="form" @submit.prevent="login">
        <router-link to="/" class="back-link">Volver a inicio</router-link>
        <p class="title">Iniciar sesión</p>
        <input
          class="input"
          v-model="email"
          type="email"
          name="email"
          id="email"
          placeholder="Correo electrónico"
        />
        <input
          class="input"
          type="password"
          name="password"
          id="password"
          v-model="password"
          placeholder="Contraseña"
        />
        <p>
          <router-link to="/forgot-password">¿Has olvidado la contraseña?</router-link>
        </p>
        <BaseButton type="submit" class="btn">Entrar</BaseButton>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <router-link to="/register" class="register-link"
          >¿No tienes cuenta? Registrarse</router-link
        >
      </form>
    </div>
    <div class="box-logo-img">
      <div class="logo">
        <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
        <div>
          <h2>DogGo!</h2>
          <p>Para ti, por ellos.</p>
        </div>
      </div>
      <div class="img-login">
        <img src="../assets/chicha-paseo.png" alt="Chica paseando perros" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import BaseInput from '@/components/BaseInput.vue'
import BaseButton from '@/components/BaseButton.vue'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()
const authStore = useAuthStore()

const login = async () => {
  errorMessage.value = ''
  try {
    const success = await authStore.loginUser({ email: email.value, password: password.value })
    if (success) {
      if (authStore.userRole === 'admin') {
        router.push({ name: 'admin-panel' })
      } else if (authStore.userRole === 'owner') {
        router.push({ name: 'owner-profile' })
      } else if (authStore.userRole === 'walker') {
        router.push({ name: 'walker-profile' })
      } else {
        router.push('/')
      }
    }
  } catch (error) {
    errorMessage.value = authStore.loginError || 'Error desconocido al iniciar sesión.'
    console.error('Error en el componente de login:', error)
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.box-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 100%;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.box-logo-img {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 100%;
  background-color: #003978;
}
.logo {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 40vw;
  height: 30%;
  margin-top: 5%;
  margin-bottom: 3%;
}

.logo img {
  height: 25vh;
}
.logo h2 {
  color: #fecf35;
  font-weight: bold;
  font-size: 50px;
  margin-top: 10px;
}
.logo p {
  color: white;
  font-size: 30px;
  text-align: right;
  font-weight: bold;
  margin-block: 0.5rem;
  width: 20vw;
}

.img-login {
  height: 70%;
}
.img-login img {
  height: 65vh;
}

.input {
}

.form {
}

.back-link {
  position: absolute;
  top: 10px;
  left: 10px;
  color: whitesmoke;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.4s ease;
}

.back-link:hover {
}

.title {
}

.register-link {
}

.register-link:hover {
}

.btn {
}

.btn:hover {
}

.error-message {
  color: #ff6b6b;
  margin-top: 10px;
  font-size: 0.9rem;
  text-align: center;
}
</style>
