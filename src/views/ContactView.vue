<template>
  <div class="wrapper">
    <header class="header">
      <div class="logo">
        <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
        <div>
          <h2>DogGo!</h2>
          <p>Para ti, por ellos.</p>
        </div>
      </div>
      <button class="back-btn" @click="$router.push('/')">Volver</button>
    </header>

    <main class="main-content">
      <section class="contact-box">
        <h1>Contacto</h1>
        <p>
          ¿Tienes dudas, sugerencias o necesitas ayuda?<br />Rellena el formulario y le
          responderemos con la mayor brevedad posible.
        </p>

        <form class="contact-form" @submit.prevent="handleSubmit">
          <input pattern="^\S.*\S$" type="text" v-model="name" placeholder="Tu nombre" required />
          <input
            pattern="^\S.*\S$"
            oninput="this.value = this.value.trim()"
            type="email"
            v-model="email"
            placeholder="Tu email"
            required
          />
          <textarea
            pattern="^\S.*\S$"
            v-model="message"
            placeholder="Tu mensaje"
            required
          ></textarea>
          <button type="submit">Enviar mensaje</button>
        </form>

        <p v-if="submitted" class="success-message">
          ¡Gracias por contactarnos! Te responderemos lo antes posible.
        </p>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const message = ref('')
const submitted = ref(false)

const handleSubmit = () => {
  console.log('Enviando mensaje:', {
    name: name.value,
    email: email.value,
    message: message.value,
  })
  submitted.value = true
  name.value = ''
  email.value = ''
  message.value = ''
  setTimeout(() => (submitted.value = false), 5000)
}
</script>

<style scoped>
.wrapper {
  min-height: 100vh;
  background-color: #f4f8fc;
  display: flex;
  flex-direction: column;
}
.header {
  background-color: #003978;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
}
.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
}
.logo img {
  height: 50px;
  margin-right: 1rem;
}
.logo h2 {
  color: #fecf35;
  margin: 0;
  font-size: 1.5rem;
}
.back-btn {
  background-color: #fecf35;
  color: #003978;
  border: none;
  border-radius: 10px;
  padding: 0.5rem 1rem;
  font-weight: bold;
  cursor: pointer;
}
.main-content {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}
.contact-box {
  background: white;
  padding: 2.5rem;
  border-radius: 1rem;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 600px;
  text-align: center;
  color: #003978;
}
.contact-box h1 {
  margin-bottom: 1rem;
  font-size: 2rem;
  color: #003978;
}
.contact-box p {
  margin-bottom: 1.5rem;
}
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.contact-form input,
.contact-form textarea {
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
}
.contact-form textarea {
  min-height: 120px;
  resize: vertical;
}
.contact-form button {
  background-color: #fecf35;
  color: #003978;
  border: none;
  padding: 0.9rem;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}
.contact-form button:hover {
  background-color: #ffd84c;
}
.success-message {
  margin-top: 1rem;
  color: #28a745;
  font-weight: bold;
}
@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  .contact-box {
    padding: 1.5rem;
  }
  .logo h2 {
    font-size: 1.3rem;
  }
  .back-btn {
    width: auto;
    font-size: 0.9rem;
  }
}
</style>
