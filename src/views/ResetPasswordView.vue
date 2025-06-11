<template>
  <div class="container">
    <form class="form" @submit.prevent="submit">
      <p class="title">Restablecer contraseña</p>
      <input
        pattern="^(?=.*[A-Z])(?=.*\d)\S{8,}$"
        v-model="password"
        required
        placeholder="Nueva contraseña"
        class="input"
        type="password"
        @focus="showPasswordHint = true"
        @blur="showPasswordHint = false"
      />
      <p v-if="showPasswordHint" class="password-hint">
        La contraseña debe tener al menos 8 caracteres, una mayúscula y un número.
      </p>
      <input
        pattern="^(?=.*[A-Z])(?=.*\d)\S{8,}$"
        v-model="repPassword"
        required
        placeholder="Repite la contraseña"
        class="input"
        type="password"
      />
      <button class="btn" type="submit">Restablecer</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
const password = ref('')
const repPassword = ref('')
const route = useRoute()
const router = useRouter()
const toast = useToast()
const token = ref('')
const showPasswordHint = ref(false)

onMounted(() => {
  token.value = route.query.token
  if (!token.value) {
    toast.error('Token de restablecimiento no encontrado en la URL.')
  }
})

const submit = async () => {
  if (password.value !== repPassword.value) {
    toast.error('Las contraseñas no coinciden.')
    return
  }

  if (!token.value) {
    toast.error('No se puede restablecer la contraseña sin un token válido.')
    return
  }

  try {
    const response = await axios.post(
      `https://tfg-doggo.onrender.com/auth/reset-password/${token.value}`,
      {
        password: password.value,
      },
    )
    toast.success(response.data.msg)
    setTimeout(() => router.push({ name: 'login' }), 2000)
  } catch (e) {
    toast.error(e.response?.data?.msg || 'Error al restablecer la contraseña.')
    console.error('Error en el restablecimiento de contraseña:', e)
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

.form {
  max-width: 400px;
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

.btn {
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

.btn:hover {
  background-color: #003978;
  color: #fecf35;
}

.success-msg {
  font-size: 14px;
  text-align: center;
  color: #28a745;
}

.password-hint {
  font-size: 0.85rem;
  color: #003978;
  margin-top: -5px;
  margin-bottom: 5px;
  width: 60%;
  text-align: center;
}
</style>
