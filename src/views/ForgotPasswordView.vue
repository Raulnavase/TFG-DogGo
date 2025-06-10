<template>
  <div class="container">
    <div class="box-form">
      <router-link to="/login" class="back-link">
        <i class="fa-solid fa-dog fa-flip-horizontal"></i> Volver
      </router-link>
      <div class="mobile-logo">
        <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
        <div>
          <h2>DogGo!</h2>
          <p>Para ti, por ellos.</p>
        </div>
      </div>

      <div class="mobile-back-link">
        <router-link to="/login" class="back-link-mobile">
          <i class="fa-solid fa-dog fa-flip-horizontal"></i> Volver
        </router-link>
      </div>

      <form class="form" @submit.prevent="submit">
        <p class="title">Recuperar contraseña</p>
        <input
          pattern="^\S.*\S$"
          oninput="this.value = this.value.trim()"
          v-model="email"
          required
          placeholder="Email"
          class="input"
          type="email"
        />
        <button class="btn-registrarse" type="submit">Enviar enlace</button>
        <p v-if="msg" class="info-msg">{{ msg }}</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const BASE_URL = 'http://localhost:5000'
// const BASE_URL = 'https://85ml2msw-5000.uks1.devtunnels.ms'

const email = ref('')
const msg = ref('')

const submit = async () => {
  msg.value = ''
  try {
    await axios.post(`${BASE_URL}/auth/forgot-password`, { email: email.value })
    msg.value = 'Si el email existe, se enviará un enlace de recuperación.'
  } catch (e) {
    msg.value = 'Error al enviar el correo.'
  }
}
</script>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
  padding: 1rem;
  background-color: white;
}

.box-form {
  max-width: 400px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.back-link {
  position: absolute;
  top: 10px;
  left: 10px;
  margin: 1.5rem 4rem;
  text-decoration: none;
  color: black;
  font-size: 25px;
}

.back-link:hover {
  letter-spacing: 2px;
  transition: 0.4s;
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
  width: 100%;
  text-align: center;
  margin: 1rem 0;
}

.back-link-mobile {
  font-size: 16px;
  text-decoration: none;
  color: #003978;
}

.form {
  width: 100%;
  background-color: white;
  padding: 1.5rem;
  border-radius: 15px;
  border: 2px solid #003978;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.title {
  font-size: 28px;
  font-weight: 800;
  color: #003978;
  margin-bottom: 0.5rem;
  text-align: center;
}

.input {
  width: 100%;
  padding: 12px;
  border: 2px solid #003978;
  border-radius: 10px;
  font-size: 16px;
  color: #003978;
}

.btn-registrarse {
  width: 100%;
  background-color: #fecf35;
  border: none;
  border-radius: 999px;
  color: #003978;
  font-weight: 600;
  padding: 12px;
  font-size: 18px;
  cursor: pointer;
}

.btn-registrarse:hover {
  background-color: #003978;
  color: #fecf35;
}

.info-msg {
  font-size: 14px;
  text-align: center;
  color: #003978;
}

@media (min-width: 769px) {
  .mobile-logo,
  .mobile-back-link {
    display: none;
  }
}

@media (max-width: 768px) {
  .back-link {
    display: none;
  }
}
</style>
