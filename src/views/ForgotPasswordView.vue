<template>
  <div class="container">
    <form class="form" @submit.prevent="submit">
      <p class="title">Recuperar contraseña</p>
      <input v-model="email" required placeholder="Email" class="input" type="email" />
      <button class="btn" type="submit">Enviar enlace</button>
      <p v-if="msg">{{ msg }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const email = ref('')
const msg = ref('')

const submit = async () => {
  msg.value = ''
  try {
    await axios.post('http://localhost:5000/auth/forgot-password', { email: email.value })
    msg.value = 'Si el email existe, se enviará un enlace de recuperación.'
  } catch (e) {
    msg.value = 'Error al enviar el correo.'
  }
}
</script>
