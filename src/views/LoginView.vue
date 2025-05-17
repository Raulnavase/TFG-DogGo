<style scoped>
::selection {
  background-color: gray;
}

.container {
  height: 100vh;
  width: 100vw;
  display: flex;
  justify-content: center;
  align-items: center;
}

.form {
  width: 30%;
  height: 95%;
  background-image: linear-gradient(to bottom, #424242, #212121);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  border-radius: 0.5rem;
}

.title {
  color: wheat;
  margin: 1.5rem 0;
  font-size: 2rem;
}

.input {
  margin: 0.5rem 0;
  padding: 0.5rem 0;
  width: 20rem;
  background-color: inherit;
  color: wheat;
  border: none;
  outline: none;
  border-bottom: 1px solid wheat;
  transition: all 400ms;
}
.input:hover {
  background-color: #424242;
  border: none;
  border-radius: 0.5rem;
}

.btn {
  height: 3rem;
  width: 20rem;
  margin-top: 3rem;
  background-color: wheat;
  border-radius: 0.5rem;
  border: none;
  font-size: 1.2rem;
  transition: all 400ms;
  cursor: pointer;
  box-shadow:
    0 0 10px antiquewhite,
    0 0 10px antiquewhite;
}
.btn:hover {
  background-color: antiquewhite;
  box-shadow: none;
}
</style>

<template>
  <div class="container">
    <form class="form" @submit.prevent="login">
      <p class="title">Iniciar sesión</p>
      <input v-model="email" required placeholder="Email" class="email input" type="email" />
      <input
        v-model="password"
        required
        placeholder="Contraseña"
        class="password input"
        type="password"
      />
      <button class="btn" type="submit">Entrar</button>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../../api/api'
import router from '@/router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')

const login = async () => {
  errorMessage.value = ''
  try {
    const response = await api.post('/login', {
      email: email.value,
      password: password.value,
    })
    console.log('Respuesta del login:', response.data)
    if (response.status === 200) {
      const accessToken = response.data.access_token
      const userRole = response.data.role
      const userName = response.data.name

      localStorage.setItem('accessToken', accessToken)
      localStorage.setItem('userRole', userRole)
      localStorage.setItem('userName', userName)

      console.log(
        'Inicio de sesión exitoso. Token:',
        accessToken,
        'Rol:',
        userRole,
        'Nombre:',
        userName,
      )

      router.push('/' + userRole + '-profile')
    } else {
      errorMessage.value = 'Error al iniciar sesión. Credenciales inválidas.'
      console.error('Error en la respuesta del login:', response)
    }
  } catch (error) {
    console.error('Error al iniciar sesión:', error)
    errorMessage.value = 'Error al iniciar sesión. Verifica tus credenciales o intenta de nuevo.'
  } finally {
    // Opcional: Limpiar los campos del formulario después del intento
    // email.value = '';
    // password.value = '';
  }
}
</script>
