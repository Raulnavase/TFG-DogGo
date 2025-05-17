<template>
  <div class="container">
    <form class="form" @submit.prevent="register">
      <router-link to="/" class="back-link">Volver a inicio</router-link>
      <p class="title">Registrarse</p>
      <input v-model="name" required placeholder="Nombre" class="name input" type="text" />
      <input
        v-model="lastName"
        required
        placeholder="Apellido"
        class="last_name input"
        type="text"
      />
      <input v-model="email" required placeholder="Email" class="email input" type="email" />
      <input
        v-model="password"
        required
        placeholder="Contraseña"
        class="password input"
        type="password"
      />
      <input
        v-model="repPassword"
        required
        placeholder="Repite contraseña"
        class="rep_password input"
        type="password"
      />
      <p class="consent">
        Al crear una cuenta, aceptas nuestros Términos de uso. Para saber cómo tratamos tus datos,
        consulta nuestra Política de privacidad.
      </p>
      <div class="box-role">
        <legend>¿Qué rol te define?</legend>
        <div>
          <input v-model="role" type="radio" name="role" value="walker" id="walker" />
          <label for="walker">Paseador de perro/s</label>
        </div>
        <div>
          <input v-model="role" type="radio" name="role" value="owner" id="owner" />
          <label for="owner">Dueño de perro/s</label>
        </div>
      </div>
      <router-link to="/login" class="login-link">¿Ya tienes cuenta? Iniciar sesión</router-link>
      <button class="btn" type="submit">Crear cuenta</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import router from '@/router'

const authStore = useAuthStore()

const name = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const repPassword = ref('')
const role = ref('')

const register = async () => {
  if (!role.value) {
    console.error('Hay que introducir un rol.')
    return
  } else if (password.value !== repPassword.value) {
    console.error('Las contraseñas no coinciden.')
    return
  }

  const userData = {
    name: name.value,
    last_name: lastName.value,
    email: email.value,
    password: password.value,
    role: role.value,
  }

  try {
    await authStore.registerUser(userData)

    if (authStore.registrationSuccess) {
      console.log('Registro completado con éxito!')
      router.push('/login')
    }
  } catch (error) {
    console.error('Error en el registro desde el componente:', authStore.registrationError)
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
  position: relative; /* Para posicionar el back-link */
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

.consent {
  color: whitesmoke;
  width: 20rem;
  max-width: 100%;
  margin-block: 10px;
  font-size: 0.9rem;
  text-align: center;
}

.box-role {
  width: 20rem;
  max-width: 100%;
  margin: 1rem 0;
}

.box-role legend {
  margin-bottom: 5px;
  color: wheat;
  font-size: 20px;
}

.box-role label {
  color: whitesmoke;
  margin-left: 5px;
}

.box-role div {
  margin: 5px 0;
}

.login-link {
  color: whitesmoke;
  text-decoration: none;
  font-size: 0.9rem;
  margin: 10px 0;
  transition: color 0.4s ease;
}

.login-link:hover {
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
</style>
