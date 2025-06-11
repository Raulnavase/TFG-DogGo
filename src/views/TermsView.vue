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
      <h1>Términos y Condiciones</h1>
      <br />
      <p>
        Bienvenido/a a <strong>DogGo!</strong>, la plataforma digital que conecta dueños de perros
        con paseadores de confianza. Al registrarte y usar nuestra aplicación o sitio web, aceptas
        estos Términos y Condiciones.
      </p>
      <br /><br />

      <h2>1. Objeto del servicio</h2>
      <br />
      <p>
        DogGo! permite a usuarios crear perfiles como <strong>dueños</strong> o
        <strong>paseadores</strong> para publicar o aceptar solicitudes de paseo canino.
      </p>
      <br /><br />

      <h2>2. Requisitos de uso</h2>
      <br />
      <ul>
        <li>Debes ser mayor de edad (18+ años).</li>
        <li>Estás obligado a proporcionar información veraz y actualizada.</li>
        <li>Aceptas usar la plataforma de forma legal, ética y respetuosa.</li>
      </ul>
      <br /><br />

      <h2>3. Responsabilidades</h2>
      <br />
      <ul>
        <li>
          <strong>DogGo!</strong> no es parte de los acuerdos entre usuarios. Actúa únicamente como
          intermediario tecnológico.
        </li>
        <li>Los usuarios son responsables de su comportamiento y del contenido que publican.</li>
        <li>Paseadores deben asegurarse de tratar adecuadamente a los perros bajo su cuidado.</li>
      </ul>
      <br /><br />

      <h2>4. Contenido de los usuarios</h2>
      <br />
      <p>
        No está permitido subir contenido ofensivo, discriminatorio o ilegal. DogGo! se reserva el
        derecho de eliminar cuentas o contenidos que violen estas normas.
      </p>
      <br /><br />

      <h2>5. Limitación de responsabilidad</h2>
      <br />
      <p>
        DogGo! no garantiza que los servicios estén libres de errores o interrupciones. No nos
        hacemos responsables de incidentes entre usuarios o del uso indebido de la plataforma.
      </p>
      <br /><br />

      <h2>6. Cancelación de cuentas</h2>
      <br />
      <p>
        Puedes cancelar tu cuenta en cualquier momento desde tu perfil. DogGo! podrá suspender o
        eliminar cuentas por uso fraudulento o incumplimiento de estos términos.
      </p>
      <br /><br />

      <h2>7. Propiedad intelectual</h2>
      <br />
      <p>
        Todos los elementos visuales, código y contenidos del sitio y la app son propiedad de DogGo!
        o de sus licenciantes. Está prohibida su reproducción sin permiso.
      </p>
      <br /><br />

      <h2>8. Modificaciones</h2>
      <br />
      <p>
        Nos reservamos el derecho de modificar estos términos. Si lo hacemos, te informaremos antes
        de que entren en vigor.
      </p>
      <br /><br />

      <h2>9. Contacto</h2>
      <br />
      <p>
        Para cualquier duda o consulta, puedes contactarnos desde
        <RouterLink to="/contact">contacto</RouterLink>.
      </p>
    </main>
  </div>
</template>

<script setup></script>

<style scoped>
.wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #fff;
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
  padding: 2rem;
  color: #003978;
}

ul li {
  list-style: none;
}

@media (max-width: 768px) {
  .header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .logo {
    flex-direction: row;
    justify-content: center;
    width: 100%;
  }

  .logo h2 {
    font-size: 1.3rem;
  }

  .back-btn {
    width: 100%;
    max-width: 200px;
    align-self: center;
  }

  .main-content {
    padding: 1rem;
    font-size: 0.95rem;
  }

  .contact-form {
    width: 100%;
    max-width: 100%;
  }
}
</style>
