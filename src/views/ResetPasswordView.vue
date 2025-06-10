<template>
  <div class="container">
    <form class="form" @submit.prevent="submit">
      <p class="title">Restablecer contraseña</p>
      <input
        v-model="password"
        required
        placeholder="Nueva contraseña"
        class="input"
        type="password"
      />
      <input
        v-model="repPassword"
        required
        placeholder="Repite la contraseña"
        class="input"
        type="password"
      />
      <button class="btn" type="submit">Restablecer</button>
      <p v-if="msg">{{ msg }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'

const password = ref('')
const repPassword = ref('')
const msg = ref('')
const route = useRoute()
const router = useRouter()

const submit = async () => {
  msg.value = ''
  if (password.value !== repPassword.value) {
    msg.value = 'Las contraseñas no coinciden.'
    return
  }
  try {
    await axios.post('https://tfg-doggo.onrender.com/auth/reset-password', {
      token: route.params.token,
      password: password.value,
    })
    msg.value = 'Contraseña restablecida correctamente. Redirigiendo...'
    setTimeout(() => router.push({ name: 'login' }), 2000)
  } catch (e) {
    msg.value = e.response?.data?.msg || 'Error al restablecer la contraseña.'
  }
}
</script>
