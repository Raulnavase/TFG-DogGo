import { RouterView } from 'vue-router';
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
      <h1>Política de Privacidad</h1>
      <br />
      <p>
        En <strong>DogGo!</strong>, nos comprometemos a proteger la privacidad y seguridad de
        nuestros usuarios. Esta Política de Privacidad describe cómo recopilamos, usamos,
        almacenamos y protegemos tus datos personales cuando accedes y utilizas nuestra plataforma.
      </p>
      <br /><br />

      <h2>1. Información que recopilamos</h2>
      <br />
      <p>Podemos recopilar los siguientes datos personales:</p>
      <ul>
        <li>
          Información de cuenta: nombre, correo electrónico, contraseña cifrada, rol (dueño o
          paseador).
        </li>
        <li>Información del perfil: foto, descripción, ubicación aproximada.</li>
        <li>Información sobre tus perros: nombre, raza, edad, imagen y notas.</li>
        <li>Comunicaciones: mensajes, solicitudes, y respuestas entre usuarios.</li>
        <li>
          Datos técnicos: tipo de dispositivo, navegador, dirección IP, cookies y datos de
          navegación.
        </li>
      </ul>
      <br /><br />

      <h2>2. Finalidad del tratamiento</h2>
      <br />
      <p>Utilizamos tus datos para:</p>
      <ul>
        <li>Crear y gestionar tu cuenta.</li>
        <li>Facilitar la conexión entre dueños y paseadores.</li>
        <li>Mostrar anuncios y solicitudes.</li>
        <li>Enviar comunicaciones relacionadas con el servicio.</li>
        <li>
          Mejorar la experiencia de usuario y garantizar el correcto funcionamiento de la
          plataforma.
        </li>
        <li>Cumplir con obligaciones legales o contractuales.</li>
      </ul>
      <br /><br />

      <h2>3. Base legal del tratamiento</h2>
      <br />
      <p>
        Tratamos tus datos con base en tu consentimiento al registrarte, la ejecución de un contrato
        (prestación del servicio DogGo!), el cumplimiento de obligaciones legales y nuestro interés
        legítimo en mejorar el servicio.
      </p>
      <br /><br />

      <h2>4. Compartición de datos</h2>
      <br />
      <p>
        Tus datos no serán vendidos ni cedidos a terceros sin tu consentimiento, salvo cuando sea
        necesario para:
      </p>
      <ul>
        <li>Cumplir con obligaciones legales.</li>
        <li>
          Gestionar servicios técnicos (como hosting o analítica) bajo acuerdos de confidencialidad.
        </li>
      </ul>
      <br /><br />

      <h2>5. Seguridad</h2>
      <br />
      <p>
        Aplicamos medidas de seguridad técnicas y organizativas para proteger tus datos personales
        contra accesos no autorizados, pérdidas o alteraciones.
      </p>
      <br /><br />

      <h2>6. Tus derechos</h2>
      <br />
      <p>
        Puedes ejercer tus derechos de acceso, rectificación, cancelación, oposición, limitación y
        portabilidad escribiéndonos desde <RouterLink to="/contact">contacto</RouterLink>. También
        puedes modificar o eliminar tus datos desde tu perfil en la plataforma.
      </p>
      <br /><br />

      <h2>7. Conservación de los datos</h2>
      <br />
      <p>
        Tus datos se conservarán mientras mantengas una cuenta activa o durante el tiempo necesario
        para cumplir con obligaciones legales. Puedes solicitar la eliminación definitiva de tus
        datos cuando lo desees.
      </p>
      <br /><br />

      <h2>8. Cambios en la política</h2>
      <br />
      <p>
        Podemos actualizar esta política. En caso de cambios relevantes, te lo notificaremos
        claramente.
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
