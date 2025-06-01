<template>
  <div class="container">
    <h1>404</h1>
    <p>¡Vaya! La página que buscas no existe.</p>
    <router-link to="/" class="btn">Volver al inicio</router-link>
  </div>
</template>

<script setup></script>

<style scoped>
.container {
  height: 80vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: wheat;
  background: #212121;
}
h1 {
  font-size: 5rem;
  margin-bottom: 1rem;
}
.btn {
  margin-top: 2rem;
  color: #212121;
  background: wheat;
  padding: 0.5rem 1.5rem;
  border-radius: 0.5rem;
  text-decoration: none;
  font-weight: bold;
}
</style>
