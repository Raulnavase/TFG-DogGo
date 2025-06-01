<template>
  <div class="container">
    <form class="form" @submit.prevent="login">
      <router-link to="/" class="back-link">Volver a inicio</router-link>
      <p class="title">Iniciar sesión</p>
      <input v-model="email" required placeholder="Email" class="email input" type="email" />
      <input
        v-model="password"
        required
        placeholder="Contraseña"
        class="password input"
        type="password"
      />
      <p>
        <router-link to="/forgot-password">¿Has olvidado la contraseña?</router-link>
      </p>
      <button class="btn" type="submit">Entrar</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      <router-link to="/register" class="register-link">¿No tienes cuenta? Registrarse</router-link>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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
      router.push({ name: `${authStore.userRole}-profile` })
    }
  } catch (error) {
    errorMessage.value = authStore.loginError || 'Error al iniciar sesión'
  }
}
</script>

<style scoped>
::selection {
  background-color: gray;
  color: white;
}

.container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #212121;
}

.form {
  width: 30%;
  min-width: 300px;
  height: 95%;
  background-image: linear-gradient(to bottom, #424242, #212121);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 0.5rem;
  padding: 20px;
  position: relative;
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
  color: antiquewhite;
}

.title {
  color: wheat;
  margin: 1.5rem 0;
  font-size: 2rem;
  font-weight: bold;
}

.input {
  margin: 0.5rem 0;
  padding: 0.5rem 0.5rem;
  width: 20rem;
  max-width: 100%;
  background-color: transparent;
  color: wheat;
  border: none;
  border-bottom: 1px solid wheat;
  outline: none;
  transition:
    background-color 0.4s ease,
    border-color 0.4s ease;
}

.input:hover,
.input:focus {
  background-color: #424242;
  border-bottom: 1px solid antiquewhite;
}

.input::placeholder {
  color: whitesmoke;
}

.register-link {
  color: whitesmoke;
  text-decoration: none;
  font-size: 0.9rem;
  margin: 10px 0;
  transition: color 0.4s ease;
}

.register-link:hover {
  color: antiquewhite;
}

.btn {
  height: 3rem;
  width: 20rem;
  max-width: 100%;
  margin-top: 2rem;
  background-color: wheat;
  border-radius: 0.5rem;
  border: none;
  font-size: 1.2rem;
  font-weight: bold;
  cursor: pointer;
  transition:
    background-color 0.4s ease,
    box-shadow 0.4s ease;
  box-shadow:
    0 0 10px antiquewhite,
    0 0 10px antiquewhite;
}

.btn:hover {
  background-color: antiquewhite;
  box-shadow: none;
}

.error-message {
  color: #ff6b6b;
  margin-top: 10px;
  font-size: 0.9rem;
  text-align: center;
}
</style>
