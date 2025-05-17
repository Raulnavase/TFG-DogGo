<template>
  <div>
    <h1>Index Page</h1>

    <div>
      <h3>¿Qué quieres hacer?</h3>
      <span>
        <p>
          <RouterLink to="/login">Iniciar sesión</RouterLink>
        </p>
        <p>
          <RouterLink to="/register">Crear cuenta</RouterLink>
        </p>
      </span>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped></style>
