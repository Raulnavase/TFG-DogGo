<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAdminStore } from '@/stores/admin'
import { useAuthStore } from '@/stores/auth'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import Loader from '@/components/Loader.vue'
import Modal from '@/components/Modal.vue'
import { useRouter } from 'vue-router'

const adminStore = useAdminStore()
const authStore = useAuthStore()
const router = useRouter()

const showCreateUserModal = ref(false)
const newUserData = ref({
  name: '',
  last_name: '',
  email: '',
  password: '',
  role: 'owner',
})

const showEditUserModal = ref(false)
const editingUser = ref(null)
const editUserData = ref({
  name: '',
  last_name: '',
  email: '',
  password: '',
  role: '',
})

const showUserDetailsModal = ref(false)
const selectedUser = computed(() => adminStore.selectedUser)

const showConfirmModal = ref(false)
const confirmMessage = ref('')
const confirmAction = ref(null)

const currentPage = ref(1)
const itemsPerPage = 10

const paginatedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return adminStore.users.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(adminStore.users.length / itemsPerPage)
})

const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

const userRoles = [
  { value: 'owner', label: 'Dueño' },
  { value: 'walker', label: 'Paseador' },
  { value: 'admin', label: 'Administrador' },
]

onMounted(() => {
  adminStore.fetchAllUsers()
})

const capitalizeFirstLetter = (string) => {
  if (!string) return ''
  return string.charAt(0).toUpperCase() + string.slice(1)
}

const openCreateUserModal = () => {
  newUserData.value = { name: '', last_name: '', email: '', password: '', role: 'owner' }
  showCreateUserModal.value = true
}

const handleCreateUser = async () => {
  try {
    await adminStore.createUser(newUserData.value)
    showCreateUserModal.value = false
    alert(adminStore.success)
    currentPage.value = 1
  } catch (error) {
    alert(adminStore.error)
  }
}

const openEditUserModal = (user) => {
  if (user._id === authStore.user?.id) {
    alert('No puedes editar tu propio perfil de administrador desde este panel.')
    return
  }
  editingUser.value = user
  editUserData.value = { ...user, password: '' }
  showEditUserModal.value = true
}

const handleUpdateUser = async () => {
  try {
    const dataToSend = { ...editUserData.value }
    if (!dataToSend.password) {
      delete dataToSend.password
    }
    await adminStore.updateUser(editingUser.value._id, dataToSend)
    showEditUserModal.value = false
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const handleDeleteUser = (userId) => {
  if (userId === authStore.user?.id) {
    alert('No puedes eliminar tu propio perfil de administrador desde este panel.')
    return
  }
  confirmMessage.value =
    '¿Estás seguro de que quieres eliminar a este usuario y todos sus datos asociados? Esta acción es irreversible.'
  confirmAction.value = async () => {
    try {
      await adminStore.deleteUser(userId)
      alert(adminStore.success)
      if (paginatedUsers.value.length === 0 && currentPage.value > 1) {
        currentPage.value--
      }
    } catch (error) {
      alert(adminStore.error)
    } finally {
      showConfirmModal.value = false
    }
  }
  showConfirmModal.value = true
}

const openUserDetailsModal = async (userId) => {
  if (userId === authStore.user?.id) {
    alert(
      'No puedes ver tu propio perfil de administrador desde este panel. Utiliza tu perfil de usuario si es necesario.',
    )
    return
  }
  await adminStore.fetchUserDetails(userId)
  showUserDetailsModal.value = true
}

const goBackToList = () => {
  showUserDetailsModal.value = false
  adminStore.selectedUser = null
}

const handleUpdateAd = async (adId, adData) => {
  try {
    await adminStore.updateAdAsAdmin(adId, adData)
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const handleDeleteAd = (adId) => {
  confirmMessage.value = '¿Estás seguro de que quieres eliminar este anuncio?'
  confirmAction.value = async () => {
    try {
      await adminStore.deleteAdAsAdmin(adId)
      alert(adminStore.success)
    } catch (error) {
      alert(adminStore.error)
    } finally {
      showConfirmModal.value = false
    }
  }
  showConfirmModal.value = true
}

const handleUpdateDog = async (dogId, dogData) => {
  try {
    await adminStore.updateDogAsAdmin(dogId, dogData)
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const handleDeleteDog = (dogId) => {
  confirmMessage.value = '¿Estás seguro de que quieres eliminar este perro?'
  confirmAction.value = async () => {
    try {
      await adminStore.deleteDogAsAdmin(dogId)
      alert(adminStore.success)
    } catch (error) {
      alert(adminStore.error)
    } finally {
      showConfirmModal.value = false
    }
  }
  showConfirmModal.value = true
}

const handleUpdateRequest = async (requestId, requestData) => {
  try {
    await adminStore.updateRequestAsAdmin(requestId, requestData)
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const handleDeleteRequest = (requestId) => {
  confirmMessage.value = '¿Estás seguro de que quieres eliminar esta solicitud?'
  confirmAction.value = async () => {
    try {
      await adminStore.deleteRequestAsAdmin(requestId)
      alert(adminStore.success)
    } catch (error) {
      alert(adminStore.error)
    } finally {
      showConfirmModal.value = false
    }
  }
  showConfirmModal.value = true
}

const confirmAndExecute = () => {
  if (confirmAction.value) {
    confirmAction.value()
  }
}

const statusText = (status) => {
  switch (status) {
    case 'pendiente':
      return 'Pendiente'
    case 'aceptada':
      return 'Aceptada'
    case 'rechazada':
      return 'Rechazada'
    case 'cancelada_por_owner':
      return 'Cancelada por el dueño'
    case 'cancelada_por_walker':
      return 'Cancelada por el paseador'
    default:
      return capitalize(status.replace(/_/g, ' '))
  }
}
</script>

<template>
  <div class="admin-panel-wrapper">
    <div class="admin-panel-container">
      <h1 class="panel-title">Panel de Administración</h1>

      <div class="panel-actions">
        <router-link to="/" class="back-link">Volver a Inicio</router-link>
        <BaseButton @click="openCreateUserModal" class="btn-primary">
          Crear Nuevo Usuario
        </BaseButton>
      </div>

      <Loader v-if="adminStore.loading && !showUserDetailsModal" />
      <div v-else-if="adminStore.error && !showUserDetailsModal" class="alert-error" role="alert">
        {{ adminStore.error }}
      </div>
      <div v-else class="table-container">
        <div class="table-wrapper">
          <table class="custom-table">
            <thead>
              <tr>
                <th class="table-header">ID</th>
                <th class="table-header">Nombre</th>
                <th class="table-header">Apellido</th>
                <th class="table-header">Email</th>
                <th class="table-header">Rol</th>
                <th class="table-header">Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginatedUsers" :key="user._id" class="table-row">
                <td class="table-data" data-label="ID">{{ user._id }}</td>
                <td class="table-data" data-label="Nombre">
                  {{ capitalizeFirstLetter(user.name) }}
                </td>
                <td class="table-data" data-label="Apellido">
                  {{ capitalizeFirstLetter(user.last_name) }}
                </td>
                <td class="table-data" data-label="Email">{{ user.email }}</td>
                <td class="table-data" data-label="Rol">
                  {{ capitalizeFirstLetter(user.role) }}
                </td>
                <td class="table-data" data-label="Acciones">
                  <div class="action-buttons">
                    <BaseButton
                      @click="openUserDetailsModal(user._id)"
                      class="btn-action view-btn"
                      :disabled="user._id === authStore.user?.id"
                      >Ver</BaseButton
                    >
                    <BaseButton
                      @click="openEditUserModal(user)"
                      class="btn-action edit-btn"
                      :disabled="user._id === authStore.user?.id"
                      >Editar</BaseButton
                    >
                    <BaseButton
                      @click="handleDeleteUser(user._id)"
                      class="btn-action delete-btn"
                      :disabled="user._id === authStore.user?.id"
                      >Eliminar</BaseButton
                    >
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="pagination">
          <BaseButton @click="goToPage(1)" :disabled="currentPage === 1" class="btn-pagination">
            Primera
          </BaseButton>
          <BaseButton
            @click="goToPage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="btn-pagination"
          >
            Anterior
          </BaseButton>
          <span class="page-info">Página {{ currentPage }} de {{ totalPages }}</span>
          <BaseButton
            @click="goToPage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="btn-pagination"
          >
            Siguiente
          </BaseButton>
          <BaseButton
            @click="goToPage(totalPages)"
            :disabled="currentPage === totalPages"
            class="btn-pagination"
          >
            Última
          </BaseButton>
        </div>
      </div>

      <Modal :show="showCreateUserModal" @close="showCreateUserModal = false">
        <template #title>Crear Nuevo Usuario</template>
        <template #body>
          <form @submit.prevent="handleCreateUser" class="modal-form">
            <div class="form-group">
              <BaseInput label="Nombre" v-model="newUserData.name" required />
            </div>
            <div class="form-group">
              <BaseInput label="Apellido" v-model="newUserData.last_name" required />
            </div>
            <div class="form-group">
              <BaseInput label="Email" type="email" v-model="newUserData.email" required />
            </div>
            <div class="form-group">
              <BaseInput
                pattern="^(?=.*[A-Z])(?=.*\d)\S{8,}$"
                label="Contraseña"
                type="password"
                v-model="newUserData.password"
                required
              />
            </div>
            <div class="form-group">
              <BaseSelect label="Rol" v-model="newUserData.role" :options="userRoles" required />
            </div>
            <div class="form-actions">
              <BaseButton type="button" @click="showCreateUserModal = false" class="btn-cancel">
                Cancelar
              </BaseButton>
              <BaseButton type="submit" class="btn-primary"> Crear Usuario </BaseButton>
            </div>
          </form>
        </template>
      </Modal>

      <Modal :show="showEditUserModal" @close="showEditUserModal = false">
        <template #title>Editar Usuario</template>
        <template #body>
          <form @submit.prevent="handleUpdateUser" class="modal-form">
            <div class="form-group">
              <BaseInput label="Nombre" v-model="editUserData.name" required />
            </div>
            <div class="form-group">
              <BaseInput label="Apellido" v-model="editUserData.last_name" required />
            </div>
            <div class="form-group">
              <BaseInput label="Email" type="email" v-model="editUserData.email" required />
            </div>
            <div class="form-group">
              <BaseInput
                pattern="^(?=.*[A-Z])(?=.*\d)\S{8,}$"
                label="Nueva Contraseña (dejar en blanco para no cambiar)"
                type="password"
                v-model="editUserData.password"
              />
            </div>
            <div class="form-group">
              <BaseSelect label="Rol" v-model="editUserData.role" :options="userRoles" required />
            </div>
            <div class="form-actions">
              <BaseButton type="button" @click="showEditUserModal = false" class="btn-cancel">
                Cancelar
              </BaseButton>
              <BaseButton type="submit" class="btn-edit"> Actualizar Usuario </BaseButton>
            </div>
          </form>
        </template>
      </Modal>

      <Modal :show="showUserDetailsModal" @close="goBackToList" :large="true">
        <template #title>Detalles del Usuario</template>
        <template #body>
          <Loader v-if="adminStore.loading && !selectedUser" />
          <div v-else-if="adminStore.error" class="alert-error" role="alert">
            {{ adminStore.error }}
          </div>
          <div v-else-if="selectedUser" class="user-details-content">
            <BaseButton @click="goBackToList" class="btn-back">
              Volver a la lista de usuarios
            </BaseButton>

            <h3 class="section-title">Información Personal</h3>
            <p><strong>ID:</strong> {{ selectedUser.user._id }}</p>
            <p>
              <strong>Nombre:</strong> {{ capitalizeFirstLetter(selectedUser.user.name) }}
              {{ capitalizeFirstLetter(selectedUser.user.last_name) }}
            </p>
            <p><strong>Email:</strong> {{ selectedUser.user.email }}</p>
            <p><strong>Rol:</strong> {{ capitalizeFirstLetter(selectedUser.user.role) }}</p>

            <h3 class="section-title">Anuncios (Paseador)</h3>
            <div v-if="selectedUser.advertisements && selectedUser.advertisements.length">
              <div v-for="ad in selectedUser.advertisements" :key="ad._id" class="detail-card">
                <p><strong>ID Anuncio:</strong> {{ ad._id }}</p>
                <p><strong>Biografía:</strong></p>
                <div class="bio-content">
                  {{ ad.biography }}
                </div>
                <p><strong>Perros Máx:</strong> {{ ad.maxDogs }}</p>
                <p><strong>Localidad:</strong> {{ ad.locality }}</p>
                <p><strong>Pausado:</strong> {{ ad.paused ? 'Sí' : 'No' }}</p>
                <div class="action-buttons mt-2">
                  <BaseButton
                    @click="handleUpdateAd(ad._id, { paused: !ad.paused })"
                    class="btn-action toggle-ad-btn"
                  >
                    {{ ad.paused ? 'Activar' : 'Pausar' }}
                  </BaseButton>
                  <BaseButton @click="handleDeleteAd(ad._id)" class="btn-action delete-btn">
                    Eliminar Anuncio
                  </BaseButton>
                </div>
              </div>
            </div>
            <p v-else class="info-message">No tiene anuncios.</p>

            <h3 class="section-title">Perros (Dueño)</h3>
            <div v-if="selectedUser.dogs && selectedUser.dogs.length">
              <div v-for="dog in selectedUser.dogs" :key="dog._id" class="detail-card">
                <p><strong>ID Perro:</strong> {{ dog._id }}</p>
                <p><strong>Nombre:</strong> {{ capitalizeFirstLetter(dog.name) }}</p>
                <p><strong>Raza:</strong> {{ capitalizeFirstLetter(dog.breed) }}</p>
                <p><strong>Edad:</strong> {{ dog.age }}</p>
                <div class="action-buttons mt-2">
                  <BaseButton @click="handleDeleteDog(dog._id)" class="btn-action delete-btn">
                    Eliminar Perro
                  </BaseButton>
                </div>
              </div>
            </div>
            <p v-else class="info-message">No tiene perros registrados.</p>

            <h3 class="section-title">Solicitudes</h3>
            <div v-if="selectedUser.requests && selectedUser.requests.length">
              <div v-for="req in selectedUser.requests" :key="req._id" class="detail-card">
                <p><strong>ID Solicitud:</strong> {{ req._id }}</p>
                <p><strong>Fecha:</strong> {{ req.date }}</p>
                <p><strong>Estado:</strong> {{ statusText(req.status) }}</p>
                <p>
                  <strong>Dueño:</strong>
                  {{ capitalizeFirstLetter(req.owner_info?.name || 'N/A') }}
                  {{ capitalizeFirstLetter(req.owner_info?.last_name || '') }} ({{
                    req.owner_info?.email || 'N/A'
                  }})
                </p>
                <p>
                  <strong>Paseador:</strong>
                  {{ capitalizeFirstLetter(req.walker_info?.name || 'N/A') }}
                  {{ capitalizeFirstLetter(req.walker_info?.last_name || '') }} ({{
                    req.walker_info?.email || 'N/A'
                  }})
                </p>
                <p>
                  <strong>Perros Solicitados:</strong>
                  <span v-if="req.dogs_info && req.dogs_info.length">
                    <span v-for="d_info in req.dogs_info" :key="d_info._id">
                      {{ capitalizeFirstLetter(d_info.name) }} ({{
                        capitalizeFirstLetter(d_info.breed)
                      }})<span v-if="selectedUser.dogs.indexOf(d_info) < req.dogs_info.length - 1"
                        >,
                      </span>
                    </span>
                  </span>
                  <span v-else>N/A</span>
                </p>
                <div class="action-buttons mt-2">
                  <BaseButton
                    @click="handleUpdateRequest(req._id, { status: 'aceptada' })"
                    class="btn-action accept-btn"
                    :disabled="req.status !== 'pendiente'"
                  >
                    Aceptar
                  </BaseButton>
                  <BaseButton
                    @click="handleUpdateRequest(req._id, { status: 'rechazada' })"
                    class="btn-action reject-btn"
                    :disabled="req.status !== 'pendiente'"
                  >
                    Rechazar
                  </BaseButton>
                  <BaseButton @click="handleDeleteRequest(req._id)" class="btn-action delete-btn">
                    Eliminar Solicitud
                  </BaseButton>
                </div>
              </div>
            </div>
            <p v-else class="info-message">No tiene solicitudes.</p>
          </div>
        </template>
      </Modal>

      <Modal :show="showConfirmModal" @close="showConfirmModal = false" :center="true">
        <template #title>Confirmar Eliminación</template>
        <template #body>
          <p class="confirm-message">{{ confirmMessage }}</p>
          <div class="confirm-actions">
            <BaseButton type="button" @click="showConfirmModal = false" class="btn-cancel">
              Cancelar
            </BaseButton>
            <BaseButton type="button" @click="confirmAndExecute" class="btn-delete-confirm">
              Eliminar
            </BaseButton>
          </div>
        </template>
      </Modal>
    </div>
  </div>
</template>

<style scoped>
.admin-panel-wrapper {
  background-color: #021a37;
  min-height: 100vh;
  padding: 2rem 0;
}

.admin-panel-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.panel-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 2rem;
  text-align: center;
  color: #003978;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.panel-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.back-link {
  color: #003978;
  font-weight: 600;
  text-decoration: none;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: #fecf35;
}

.btn-primary {
  background-color: #fecf35;
  color: #003978;
  border: none;
  border-radius: 10px;
  padding: 0.8rem 1.8rem;
  font-weight: bold;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.btn-primary:hover {
  background-color: #ffda6a;
  transform: translateY(-2px);
}

.loader-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.alert-error {
  background-color: #ffebeb;
  border: 1px solid #ff4d4f;
  color: #ff4d4f;
  padding: 1rem 1.5rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-weight: 500;
  text-align: center;
}

.table-container {
  background-color: #fff;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.table-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.custom-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  min-width: 700px;
}

.table-header {
  padding: 1.2rem 1.5rem;
  background-color: #003978;
  color: #fecf35;
  text-align: left;
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 2px solid #002a5c;
}

.table-row {
  transition: background-color 0.2s ease;
}

.table-row:nth-child(even) {
  background-color: #f8faff;
}

.table-row:hover {
  background-color: #e0f2f7;
}

.table-data {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e0e7ee;
  background-color: #fff;
  font-size: 0.9rem;
  color: #333;
}

.action-buttons {
  display: flex;
  gap: 0.7rem;
  flex-wrap: wrap;
}

.btn-action {
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.8rem;
  font-weight: 600;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border: none;
  color: white;
}

.view-btn {
  background-color: #003978;
}
.view-btn:hover {
  background-color: #002a5c;
  transform: translateY(-2px);
}

.edit-btn {
  background-color: #fecf35;
  color: #003978;
}
.edit-btn:hover {
  background-color: #ffda6a;
  transform: translateY(-2px);
}

.delete-btn {
  background-color: #ff4d4f;
}
.delete-btn:hover {
  background-color: #e60000;
  transform: translateY(-2px);
}

.toggle-ad-btn {
  background-color: #8a2be2;
}
.toggle-ad-btn:hover {
  background-color: #6a1ba3;
  transform: translateY(-2px);
}

.accept-btn {
  background-color: #28a745;
}
.accept-btn:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

.reject-btn {
  background-color: #fd7e14;
}
.reject-btn:hover {
  background-color: #e66a00;
  transform: translateY(-2px);
}

.btn-action:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  box-shadow: none;
  transform: none;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.8rem;
  padding: 1.5rem 0;
  border-top: 1px solid #e0e7ee;
  background-color: #f0f4f8;
  border-bottom-left-radius: 15px;
  border-bottom-right-radius: 15px;
}

.btn-pagination {
  background-color: #003978;
  color: #fefefe;
  border: none;
  border-radius: 8px;
  padding: 0.6rem 1.2rem;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

.btn-pagination:hover:not(:disabled) {
  background-color: #fecf35;
  color: #003978;
  transform: translateY(-2px);
}

.btn-pagination:disabled {
  background-color: #b0c4de;
  color: #e0e7ee;
  cursor: not-allowed;
  opacity: 0.7;
}

.page-info {
  color: #003978;
  font-weight: 600;
  font-size: 0.9rem;
}

.modal-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
}

.btn-cancel {
  background-color: #a0a0a0;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.8rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

.btn-cancel:hover {
  background-color: #8c8c8c;
  transform: translateY(-2px);
}

.btn-edit {
  background-color: #fecf35;
  color: #003978;
  border: none;
  border-radius: 10px;
  padding: 0.8rem 1.5rem;
  font-weight: bold;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
}

.btn-edit:hover {
  background-color: #ffda6a;
  transform: translateY(-2px);
}

.user-details-content {
  background-color: #fcfdff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: inset 0 1px 5px rgba(0, 0, 0, 0.05);
}

.btn-back {
  background-color: #003978;
  color: #fefefe;
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1.2rem;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
  margin-bottom: 1.5rem;
}

.btn-back:hover {
  background-color: #002a5c;
  transform: translateY(-2px);
}

.section-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: #003978;
  margin-top: 2rem;
  margin-bottom: 1rem;
  border-bottom: 2px solid #fecf35;
  padding-bottom: 0.5rem;
}

.user-details-content p {
  margin-bottom: 0.6rem;
  color: #333;
}

.detail-card {
  background-color: #f0f8ff;
  border: 1px solid #e0e7ee;
  border-radius: 10px;
  padding: 1rem;
  margin-bottom: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.detail-card strong {
  color: #003978;
}

.info-message {
  color: #6a6a6a;
  font-style: italic;
  padding: 1rem;
  background-color: #f7f7f7;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  background-color: #fff;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 90%;
  max-width: 500px;
  position: relative;
  animation: fadeInScale 0.3s ease-out;
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #fecf35;
  padding-bottom: 1rem;
}

.modal-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #003978;
}

.modal-close-button {
  background: none;
  border: none;
  font-size: 1.8rem;
  color: #a0a0a0;
  cursor: pointer;
  transition: color 0.3s ease;
}

.modal-close-button:hover {
  color: #666;
}

.confirm-message {
  text-align: center;
  color: #444;
  font-size: 1.1rem;
  margin-bottom: 2rem;
  line-height: 1.5;
}

.confirm-actions {
  display: flex;
  justify-content: center;
  gap: 1.5rem;
}

.btn-delete-confirm {
  background-color: #ff4d4f;
  color: #fff;
  border: none;
  border-radius: 10px;
  padding: 0.8rem 1.8rem;
  font-weight: bold;
  cursor: pointer;
  transition:
    background-color 0.3s ease,
    transform 0.2s ease;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.btn-delete-confirm:hover {
  background-color: #e60000;
  transform: translateY(-2px);
}

.bio-content {
  max-height: 120px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-wrap: break-word;
  line-height: 1.4;
  font-size: 0.95rem;
  color: #444;
  padding: 0.5rem;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f9f9f9;
  text-align: left;
  width: 100%;
}

@media (max-width: 768px) {
  .admin-panel-container {
    padding: 1rem;
    margin: 1rem;
  }

  .panel-title {
    font-size: 2rem;
    margin-bottom: 1.5rem;
  }

  .panel-actions {
    flex-direction: column;
    align-items: stretch;
  }

  .btn-primary,
  .back-link {
    width: 100%;
    text-align: center;
  }

  .table-container {
    padding: 0;
  }

  .table-wrapper {
    overflow-x: hidden;
  }

  .custom-table {
    min-width: unset;
  }

  .custom-table thead {
    display: none;
  }

  .custom-table,
  .custom-table tbody,
  .custom-table tr,
  .custom-table td {
    display: block;
    width: 100%;
  }

  .custom-table tr {
    margin-bottom: 1.5rem;
    border: 1px solid #e0e7ee;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  }

  .table-data {
    border-bottom: 1px solid #eee;
    text-align: right;
    position: relative;
    padding-left: 50%;
    white-space: normal;
    word-wrap: break-word;
  }

  .table-data::before {
    content: attr(data-label);
    position: absolute;
    left: 1rem;
    width: calc(50% - 1.5rem);
    text-align: left;
    font-weight: bold;
    color: #003978;
  }

  .table-data:last-child {
    border-bottom: 0;
  }

  .action-buttons {
    justify-content: center;
    margin-top: 1rem;
  }

  .btn-action {
    flex-grow: 1;
    text-align: center;
  }

  .pagination {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .btn-pagination {
    flex-grow: 1;
    text-align: center;
  }

  .modal-form {
    padding: 0.5rem;
  }

  .form-actions {
    flex-direction: column-reverse;
    gap: 0.8rem;
  }

  .form-actions .btn-primary,
  .form-actions .btn-cancel,
  .form-actions .btn-edit {
    width: 100%;
  }

  .user-details-content {
    padding: 1rem;
  }

  .btn-back {
    width: 100%;
    text-align: center;
  }

  .section-title {
    font-size: 1.2rem;
  }

  .detail-card {
    padding: 0.8rem;
  }

  .modal-container {
    padding: 1.5rem;
  }

  .modal-title {
    font-size: 1.5rem;
  }

  .confirm-message {
    font-size: 1rem;
  }

  .confirm-actions {
    flex-direction: column;
    gap: 1rem;
  }

  .btn-delete-confirm,
  .btn-cancel {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .panel-title {
    font-size: 1.8rem;
  }

  .btn-primary,
  .btn-action,
  .btn-pagination,
  .btn-back {
    padding: 0.6rem 1rem;
    font-size: 0.8rem;
  }

  .table-data {
    font-size: 0.85rem;
  }
}
</style>
