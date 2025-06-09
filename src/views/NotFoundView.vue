<template>
  <div class="not-found-container">
    <div class="content-wrapper">
      <div class="dog-illustration">
        <span class="oops-text">¡Oops!</span>
        <img src="../assets/gif-dog.gif" alt="Perro perdido buscando" class="lost-dog-img" />
      </div>
      <h1 class="title">404 - Página Perdida</h1>
      <p class="message">
        Parece que esta página se ha extraviado como un perrito juguetón.<br />
        ¡No te preocupes, la encontraremos!
      </p>
      <router-link to="/" class="home-button">Volver a casa</router-link>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.not-found-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #021a37;
  color: #fefefe;
  padding: 2rem;
  text-align: center;
  overflow: hidden;
}

.content-wrapper {
  background-color: #003978;
  border-radius: 20px;
  padding: 3rem 2rem;
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.4);
  max-width: 600px;
  width: 95%;
  position: relative;
  overflow: hidden;
}

.dog-illustration {
  position: relative;
  margin-bottom: 2rem;
}

.lost-dog-img {
  width: 180px;
  margin-top: 3rem;
  filter: drop-shadow(5px 5px 10px rgba(0, 0, 0, 0.3));
}

.oops-text {
  position: absolute;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 2rem;
  font-weight: bold;
  color: #fecf35;
  text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.5);
  animation: bounce 1s infinite ease-out;
  z-index: 1;
}

@keyframes movePaws {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

@keyframes bounce {
  0%,
  100% {
    transform: translateX(-50%) translateY(0);
  }
  50% {
    transform: translateX(-50%) translateY(-15px);
  }
}

.title {
  font-size: 3rem;
  font-weight: 900;
  color: #fecf35;
  margin-bottom: 1rem;
  text-shadow: 3px 3px 7px rgba(0, 0, 0, 0.3);
}

.message {
  font-size: 1.2rem;
  line-height: 1.6;
  margin-bottom: 2.5rem;
  color: #e0f2f7;
  max-width: 400px;
  margin-left: auto;
  margin-right: auto;
}

.home-button {
  display: inline-block;
  background-color: #fecf35;
  color: #003978;
  padding: 0.9rem 2.2rem;
  border-radius: 12px;
  text-decoration: none;
  font-weight: bold;
  font-size: 1.1rem;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease,
    box-shadow 0.3s ease;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
  border: none;
  cursor: pointer;
}

.home-button:hover {
  background-color: #ffda6a;
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}

@media (max-width: 600px) {
  .not-found-container {
    padding: 1rem;
  }

  .content-wrapper {
    padding: 2rem 1rem;
  }

  .title {
    font-size: 2.5rem;
  }

  .message {
    font-size: 1rem;
  }

  .lost-dog-img {
    width: 150px;
  }

  .oops-text {
    font-size: 1.8rem;
    top: 10px;
  }

  .paws {
    font-size: 2rem;
  }
}

@media (max-width: 400px) {
  .title {
    font-size: 2rem;
  }

  .lost-dog-img {
    width: 120px;
  }

  .oops-text {
    font-size: 1.5rem;
  }

  .home-button {
    padding: 0.8rem 1.8rem;
    font-size: 1rem;
  }
}
</style>
