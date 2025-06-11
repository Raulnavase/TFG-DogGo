<template>
  <div class="container">
    <div class="box-form">
      <div class="mobile-logo">
        <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
        <div>
          <h2>DogGo!</h2>
          <p>Para ti, por ellos.</p>
        </div>
      </div>

      <div class="box-back-link mobile-back-link">
        <router-link to="/" class="back-link">
          <i class="fa-solid fa-dog fa-flip-horizontal"></i> Volver
        </router-link>
      </div>

      <form class="form" @submit.prevent="login">
        <p class="title">Iniciar sesión</p>
        <div class="inputs">
          <input
            pattern="^\S.*\S$"
            oninput="this.value = this.value.trim()"
            class="input"
            v-model="email"
            type="email"
            name="email"
            id="email"
            placeholder="Correo electrónico"
          />
          <input
            pattern="^\S.*\S$"
            class="input"
            type="password"
            name="password"
            id="password"
            v-model="password"
            placeholder="Contraseña"
          />
        </div>
        <p class="box-forgot-password">
          <router-link class="forgot-password" to="/forgot-password">
            ¿Has olvidado la contraseña?
          </router-link>
        </p>
        <button type="submit" class="btn-entrar">Entrar</button>
        <p>
          ¿No tienes cuenta?
          <router-link to="/register" class="register-link">Registrarse</router-link>
        </p>
      </form>
    </div>

    <div class="box-logo-img">
      <div class="logo">
        <img src="../assets/logo-DogGo-blanco.png" alt="Logo DogGo" />
        <div>
          <h2>DogGo!</h2>
          <p>Para ti, por ellos.</p>
        </div>
      </div>
      <div class="img-login">
        <img src="../assets/chicha-paseo.png" alt="Chica paseando perros" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useToast } from 'vue-toastification'

const email = ref('')
const password = ref('')
const router = useRouter()
const authStore = useAuthStore()
const toast = useToast()

const login = async () => {
  try {
    const success = await authStore.loginUser({ email: email.value, password: password.value })
    if (success) {
      toast.success('¡Sesión iniciada correctamente!')
      if (authStore.userRole === 'admin') {
        router.push({ name: 'admin-panel' })
      } else if (authStore.userRole === 'owner') {
        router.push({ name: 'owner-profile' })
      } else if (authStore.userRole === 'walker') {
        router.push({ name: 'walker-profile' })
      } else {
        router.push('/')
      }
    } else {
      toast.error(authStore.loginError || 'Error desconocido al iniciar sesión.')
    }
  } catch (error) {
    toast.error('Error al intentar iniciar sesión. Por favor, inténtalo de nuevo.')
    console.error('Error en el componente de login:', error)
  }
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: row;
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

.form {
  border-radius: 15px;
  height: 80%;
  width: 70%;
  margin-top: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  border: 2px solid #003978;
}

.form .title {
  font-size: 40px;
  color: #003978;
  font-weight: 500;
  letter-spacing: 1px;
  height: 15%;
  line-height: 75px;
}

.form .inputs input {
  border: 1.5px solid #003978;
  color: #003978;
  border-radius: 8px;
  outline: none;
  width: 60%;
  height: 5vh;
  padding-left: 7px;
}

.form .inputs input::placeholder {
  color: #003978;
  font-size: 15px;
  letter-spacing: 1px;
}

.form .inputs {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 15%;
}

.forgot-password,
.register-link {
  color: #02b1e0;
}

.btn-entrar {
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

.btn-entrar:hover {
  background-color: #003978;
  color: #fecf35;
  transition: 0.3s;
}

.box-logo-img {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  width: 50%;
  height: 100%;
  background-color: #003978;
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
  height: 25vh;
}
.logo h2 {
  color: #fecf35;
  font-weight: 800;
  font-size: 50px;
  margin-top: 10px;
}
.logo p {
  color: white;
  font-size: 25px;
  text-align: right;
  font-weight: bold;
  margin-block: 0.5rem;
  text-align: end;
  width: 20vw;
}

.img-login {
  height: 70%;
}
.img-login img {
  height: 65vh;
}

.mobile-logo {
  display: none;
}

@media (max-width: 768px) {
  .container {
    flex-direction: column;
    height: auto;
    padding: 2rem 1rem;
    margin-top: 10vh;
  }

  .box-logo-img {
    display: none;
  }

  .box-form {
    width: 100%;
    max-width: 400px;
    height: auto;
    padding: 0 1rem;
    margin-top: 0;
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

  .back-link {
    position: static;
    font-size: 16px;
    text-decoration: none;
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

  .form .inputs {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    gap: 10px;
    margin-bottom: 20px;
    margin-top: 15px;
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

  .box-forgot-password {
    width: 100%;
    text-align: center;
    font-size: 14px;
  }

  .btn-entrar {
    width: 100%;
    height: 50px;
    border-radius: 999px;
    font-size: 18px;
    font-weight: 600;
    margin-top: 10px;
  }

  .form p {
    font-size: 14px;
    text-align: center;
    margin: 0;
  }

  .register-link {
    font-weight: 600;
    margin-left: 5px;
  }

  .error-message {
    text-align: center;
    font-size: 14px;
    margin-top: 10px;
  }
}
</style>
