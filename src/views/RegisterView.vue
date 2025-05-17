<style scoped>
::selection {
  background-color: gray;
}

.container {
  border: 2px solid red;
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

.consent {
  color: whitesmoke;
  width: 20rem;
  margin-block: 10px;
}

.box-role {
  width: 20rem;
}

.box-role legend {
  margin-bottom: 5px;
  color: wheat;
  font-size: 20px;
}

.box-role label {
  color: whitesmoke;
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
    <form class="form" @submit.prevent="register">
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
          <label for="walker"> Paseador de perro/s</label>
        </div>
        <div>
          <input v-model="role" type="radio" name="role" value="owner" id="owner" />
          <label for="owner"> Dueño de perro/s</label>
        </div>
      </div>
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
    console.error('Hay quwe introducir un rol.')
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
