<template>
  <div class="container">
    <div class="box-form">
      <div class="mobile-header">
        <div class="mobile-logo">
          <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
          <div>
            <h2>DogGo!</h2>
            <p>Para ti, por ellos.</p>
          </div>
        </div>

        <div class="mobile-back-link">
          <router-link to="/" class="back-link">
            <i class="fa-solid fa-dog fa-flip-horizontal"></i> Volver
          </router-link>
        </div>
      </div>

      <form class="form" @submit.prevent="register">
        <p class="title">Regístrate</p>
        <div class="inputs">
          <input
            pattern="^\S.*\S$"
            class="input"
            v-model="name"
            required
            type="text"
            placeholder="Nombre"
          />
          <input
            pattern="^\S.*\S$"
            class="input"
            v-model="lastName"
            required
            type="text"
            placeholder="Apellido"
          />
          <input
            pattern="^\S.*\S$"
            oninput="this.value = this.value.trim()"
            class="input"
            v-model="email"
            required
            type="email"
            placeholder="Email"
          />
          <input
            pattern="^(?=.*[A-Z])(?=.*\d)\S{8,}$"
            class="input"
            v-model="password"
            required
            type="password"
            placeholder="Contraseña"
            @focus="showPasswordHint = true"
            @blur="showPasswordHint = false"
          />
          <p v-if="showPasswordHint" class="password-hint">
            La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.
          </p>
          <input
            pattern="^(?=.*[A-Z])(?=.*\d)\S{8,}$"
            class="input"
            v-model="repPassword"
            required
            type="password"
            placeholder="Repite contraseña"
          />
        </div>

        <button type="submit" class="btn-registrarse">Registrarse</button>

        <p class="login-text">
          ¿Ya tienes cuenta?
          <router-link to="/login" class="login-link">Iniciar sesión</router-link>
        </p>

        <p class="legend-role">Selecciona tu rol</p>
        <div class="box-role">
          <input
            v-model="role"
            type="radio"
            name="role"
            value="owner"
            id="owner"
            class="hidden-radio"
            required
          />
          <label for="owner" class="role-button">Dueño</label>

          <input
            v-model="role"
            type="radio"
            name="role"
            value="walker"
            id="walker"
            class="hidden-radio"
            required
          />
          <label for="walker" class="role-button">Paseador</label>
        </div>

        <p class="consent">
          Al registrarse, aceptas nuestros <br />
          <router-link to="/terms" class="terms-link">términos y condiciones</router-link>
        </p>
      </form>
    </div>

    <div class="box-logo-img">
      <div class="box-back-link">
        <router-link to="/" class="back-link">
          <i class="fa-solid fa-dog fa-flip-horizontal"></i> Volver
        </router-link>
      </div>
      <div class="logo">
        <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
        <div>
          <h2>DogGo!</h2>
          <p>Para ti, por ellos.</p>
        </div>
      </div>
      <div class="img-register">
        <img src="../assets/chico-paseo.webp" alt="Chico paseando perros" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const authStore = useAuthStore()
const router = useRouter()
const toast = useToast()

const name = ref('')
const lastName = ref('')
const email = ref('')
const password = ref('')
const repPassword = ref('')
const role = ref('')
const showPasswordHint = ref(false)

const register = async () => {
  if (!role.value) {
    toast.error('Debes seleccionar un rol (Paseador o Dueño).')
    return
  } else if (password.value !== repPassword.value) {
    toast.error('Las contraseñas no coinciden.')
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
    toast.success('¡Registro exitoso! Ahora puedes iniciar sesión.')
    router.push({ name: 'login' })
  } catch (error) {
    toast.error('Error al registrarse. Inténtalo de nuevo más tarde.')
    console.error('Error en el registro desde el componente:', error)
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row-reverse;
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
  background-color: white;
}

.box-logo-img {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 100%;
  background-color: #003978;
  position: relative;
}

.box-back-link {
  position: absolute;
  top: 10px;
  left: 10px;
  margin: 1.5rem 4rem;
  z-index: 10;
}

.back-link {
  text-decoration: none;
  color: #02b1e0;
  font-size: 25px;
  display: flex;
  align-items: center;
  gap: 5px;
}

.back-link:hover {
  letter-spacing: 2px;
  transition: 0.4s;
}

.logo {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 30%;
  margin-top: 5%;
  margin-bottom: 3%;
}

.logo img {
  height: 20vh;
  margin-right: 15px;
}

.logo h2 {
  color: #fecf35;
  font-weight: 800;
  font-size: 60px;
  margin: 0;
}

.logo p {
  color: white;
  font-size: 25px;
  font-weight: bold;
  margin-block: 0.5rem;
  text-align: end;
  width: 20vw;
}

.img-register {
  height: 70%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.img-register img {
  height: 60vh;
  max-width: 100%;
}

.form {
  border-radius: 15px;
  height: 95%;
  width: 70%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 5px;
  border: 2px solid #003978;
}

.form .title {
  font-size: 40px;
  color: #003978;
  font-weight: 500;
  letter-spacing: 1px;
  margin-bottom: 20px;
}

.form .inputs {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  gap: 10px;
  margin-bottom: 20px;
}

.form .inputs input {
  border: 1px solid #003978;
  color: #003978;
  border-radius: 8px;
  outline: none;
  width: 60%;
  height: 5vh;
  padding: 0 15px;
}

.form .inputs input::placeholder {
  color: #003978;
  font-size: 15px;
  letter-spacing: 1px;
}

.btn-registrarse {
  border: none;
  background-color: #fecf35;
  color: #003978;
  width: 60%;
  height: 5vh;
  border-radius: 15px;
  font-size: 18px;
  font-weight: 500;
  letter-spacing: 1px;
  cursor: pointer;
}

.btn-registrarse:hover {
  background-color: #003978;
  color: #fecf35;
  transition: 0.3s;
}

.login-text {
  color: black;
  font-size: 1rem;
  margin-top: 10px;
}

.login-link {
  color: #02b1e0;
  text-decoration: underline;
}

.legend-role {
  color: black;
  font-size: 1.1rem;
  font-weight: bold;
  margin-top: 15px;
}

.box-role {
  width: 60%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1.5px solid #02b1e0;
  border-radius: 8px;
  padding: 5px;
  margin-bottom: 10px;
}

.hidden-radio {
  display: none;
}

.role-button {
  flex: 1;
  text-align: center;
  padding: 10px 0;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  color: #003978;
  background-color: white;
}

.hidden-radio:checked + .role-button {
  background-color: #02b1e0;
  color: white;
}

.role-button:hover {
  background-color: #e0f2f7;
}

.hidden-radio:checked + .role-button:hover {
  background-color: #02b1e0;
  color: white;
}

.consent {
  color: black;
  width: 60%;
  margin-block: 10px;
  font-size: 20px;
  text-align: center;
  line-height: 1.3;
}

.terms-link {
  color: #02b1e0;
  text-decoration: underline;
}

.password-hint {
  font-size: 0.85rem;
  color: #003978;
  margin-top: -5px;
  margin-bottom: 5px;
  width: 60%;
  text-align: center;
}

.mobile-header {
  display: none;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    height: auto;
    padding: 2rem 1rem;
    margin-top: 5vh;
  }

  .box-logo-img {
    display: none;
  }

  .box-form {
    width: 100%;
    max-width: 400px;
    padding: 0 1rem;
  }

  .mobile-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 1rem;
  }

  .mobile-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 0.5rem;
    justify-content: center;
    flex-wrap: wrap;
    text-align: center;
  }

  .mobile-logo img {
    width: 50px;
    height: 50px;
  }

  .mobile-logo h2 {
    font-size: 24px;
    font-weight: 800;
    color: #fecf35;
    margin: 0;
    width: 100%;
  }

  .mobile-logo p {
    font-size: 14px;
    font-weight: bold;
    color: #003978;
    margin: 0;
    width: 100%;
  }

  .mobile-back-link {
    margin-top: 0.8rem;
  }

  .back-link {
    font-size: 16px;
    color: #003978;
  }

  .form {
    width: 100%;
    border: none;
    gap: 1rem;
    padding: 1rem 0;
  }

  .form .title {
    font-size: 28px;
    text-align: center;
  }

  .form .inputs input {
    width: 100%;
    height: 40px;
    font-size: 16px;
  }

  .form .inputs input::placeholder {
    color: #003978;
    font-size: 15px;
    letter-spacing: 1px;
  }

  .btn-registrarse {
    width: 100%;
    height: 50px;
    border-radius: 999px;
  }

  .box-role,
  .consent,
  .login-text,
  .error-message {
    width: 100%;
    text-align: center;
    font-size: 14px;
  }

  .box-role {
    gap: 10px;
  }

  .role-button {
    font-size: 14px;
    padding: 8px;
  }
}
</style>
