<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAdminStore } from '@/stores/admin'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import BaseSelect from '@/components/BaseSelect.vue'
import Loader from '@/components/Loader.vue'
import Modal from '@/components/Modal.vue'

const adminStore = useAdminStore()

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

const userRoles = [
  { value: 'owner', label: 'Propietario' },
  { value: 'walker', label: 'Paseador' },
  { value: 'admin', label: 'Administrador' },
]

onMounted(() => {
  adminStore.fetchAllUsers()
})

const openCreateUserModal = () => {
  newUserData.value = { name: '', last_name: '', email: '', password: '', role: 'owner' }
  showCreateUserModal.value = true
}

const handleCreateUser = async () => {
  try {
    await adminStore.createUser(newUserData.value)
    showCreateUserModal.value = false
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const openEditUserModal = (user) => {
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

const handleDeleteUser = async (userId) => {
  if (
    confirm(
      '¿Estás seguro de que quieres eliminar a este usuario y todos sus datos asociados? Esta acción es irreversible.',
    )
  ) {
    try {
      await adminStore.deleteUser(userId)
      alert(adminStore.success)
    } catch (error) {
      alert(adminStore.error)
    }
  }
}

const openUserDetailsModal = async (userId) => {
  await adminStore.fetchUserDetails(userId)
  showUserDetailsModal.value = true
}

const handleUpdateAd = async (adId, adData) => {
  try {
    await adminStore.updateAdAsAdmin(adId, adData)
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const handleDeleteAd = async (adId) => {
  if (confirm('¿Estás seguro de que quieres eliminar este anuncio?')) {
    try {
      await adminStore.deleteAdAsAdmin(adId)
      alert(adminStore.success)
    } catch (error) {
      alert(adminStore.error)
    }
  }
}

const handleUpdateDog = async (dogId, dogData) => {
  try {
    await adminStore.updateDogAsAdmin(dogId, dogData)
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const handleDeleteDog = async (dogId) => {
  if (confirm('¿Estás seguro de que quieres eliminar este perro?')) {
    try {
      await adminStore.deleteDogAsAdmin(dogId)
      alert(adminStore.success)
    } catch (error) {
      alert(adminStore.error)
    }
  }
}

const handleUpdateRequest = async (requestId, requestData) => {
  try {
    await adminStore.updateRequestAsAdmin(requestId, requestData)
    alert(adminStore.success)
  } catch (error) {
    alert(adminStore.error)
  }
}

const handleDeleteRequest = async (requestId) => {
  if (confirm('¿Estás seguro de que quieres eliminar esta solicitud?')) {
    try {
      await adminStore.deleteRequestAsAdmin(requestId)
      alert(adminStore.success)
    } catch (error) {
      alert(adminStore.error)
    }
  }
}
</script>

<template>
  <div class="container mx-auto p-4">
    <h1 class="text-3xl font-bold mb-6 text-center text-indigo-700">Panel de Administración</h1>

    <div class="flex justify-end mb-4">
      <BaseButton @click="openCreateUserModal" class="bg-green-500 hover:bg-green-600 text-white">
        Crear Nuevo Usuario
      </BaseButton>
    </div>

    <Loader v-if="adminStore.loading" class="text-indigo-600" />
    <div
      v-else-if="adminStore.error"
      class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
      role="alert"
    >
      {{ adminStore.error }}
    </div>
    <div v-else class="bg-white shadow-md rounded-lg overflow-hidden">
      <table class="min-w-full leading-normal">
        <thead>
          <tr>
            <th
              class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              ID
            </th>
            <th
              class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Nombre
            </th>
            <th
              class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Apellido
            </th>
            <th
              class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Email
            </th>
            <th
              class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Rol
            </th>
            <th
              class="px-5 py-3 border-b-2 border-gray-200 bg-gray-100 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider"
            >
              Acciones
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in adminStore.users" :key="user._id" class="hover:bg-gray-50">
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              {{ user._id }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              {{ user.name }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              {{ user.last_name }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              {{ user.email }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              {{ user.role }}
            </td>
            <td class="px-5 py-5 border-b border-gray-200 bg-white text-sm">
              <div class="flex space-x-2">
                <BaseButton
                  @click="openUserDetailsModal(user._id)"
                  class="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1"
                  >Ver</BaseButton
                >
                <BaseButton
                  @click="openEditUserModal(user)"
                  class="bg-yellow-500 hover:bg-yellow-600 text-white text-xs px-3 py-1"
                  >Editar</BaseButton
                >
                <BaseButton
                  @click="handleDeleteUser(user._id)"
                  class="bg-red-500 hover:bg-red-600 text-white text-xs px-3 py-1"
                  >Eliminar</BaseButton
                >
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <Modal :show="showCreateUserModal" @close="showCreateUserModal = false">
      <template #title>Crear Nuevo Usuario</template>
      <template #body>
        <form @submit.prevent="handleCreateUser">
          <div class="mb-4">
            <BaseInput label="Nombre" v-model="newUserData.name" required />
          </div>
          <div class="mb-4">
            <BaseInput label="Apellido" v-model="newUserData.last_name" required />
          </div>
          <div class="mb-4">
            <BaseInput label="Email" type="email" v-model="newUserData.email" required />
          </div>
          <div class="mb-4">
            <BaseInput label="Contraseña" type="password" v-model="newUserData.password" required />
          </div>
          <div class="mb-4">
            <BaseSelect label="Rol" v-model="newUserData.role" :options="userRoles" required />
          </div>
          <div class="flex justify-end space-x-2 mt-6">
            <BaseButton
              type="button"
              @click="showCreateUserModal = false"
              class="bg-gray-300 hover:bg-gray-400 text-gray-800"
            >
              Cancelar
            </BaseButton>
            <BaseButton type="submit" class="bg-green-500 hover:bg-green-600 text-white">
              Crear Usuario
            </BaseButton>
          </div>
        </form>
      </template>
    </Modal>

    <Modal :show="showEditUserModal" @close="showEditUserModal = false">
      <template #title>Editar Usuario</template>
      <template #body>
        <form @submit.prevent="handleUpdateUser">
          <div class="mb-4">
            <BaseInput label="Nombre" v-model="editUserData.name" required />
          </div>
          <div class="mb-4">
            <BaseInput label="Apellido" v-model="editUserData.last_name" required />
          </div>
          <div class="mb-4">
            <BaseInput label="Email" type="email" v-model="editUserData.email" required />
          </div>
          <div class="mb-4">
            <BaseInput
              label="Nueva Contraseña (dejar en blanco para no cambiar)"
              type="password"
              v-model="editUserData.password"
            />
          </div>
          <div class="mb-4">
            <BaseSelect label="Rol" v-model="editUserData.role" :options="userRoles" required />
          </div>
          <div class="flex justify-end space-x-2 mt-6">
            <BaseButton
              type="button"
              @click="showEditUserModal = false"
              class="bg-gray-300 hover:bg-gray-400 text-gray-800"
            >
              Cancelar
            </BaseButton>
            <BaseButton type="submit" class="bg-yellow-500 hover:bg-yellow-600 text-white">
              Actualizar Usuario
            </BaseButton>
          </div>
        </form>
      </template>
    </Modal>

    <Modal :show="showUserDetailsModal" @close="showUserDetailsModal = false" :large="true">
      <template #title>Detalles del Usuario</template>
      <template #body>
        <Loader v-if="adminStore.loading && !selectedUser" class="text-indigo-600" />
        <div
          v-else-if="adminStore.error"
          class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
          role="alert"
        >
          {{ adminStore.error }}
        </div>
        <div v-else-if="selectedUser">
          <h3 class="text-lg font-semibold mb-2 text-indigo-600">Información Personal</h3>
          <p><strong>ID:</strong> {{ selectedUser.user._id }}</p>
          <p>
            <strong>Nombre:</strong> {{ selectedUser.user.name }} {{ selectedUser.user.last_name }}
          </p>
          <p><strong>Email:</strong> {{ selectedUser.user.email }}</p>
          <p><strong>Rol:</strong> {{ selectedUser.user.role }}</p>

          <h3 class="text-lg font-semibold mt-6 mb-2 text-indigo-600">Anuncios (Paseador)</h3>
          <div v-if="selectedUser.advertisements && selectedUser.advertisements.length">
            <div
              v-for="ad in selectedUser.advertisements"
              :key="ad._id"
              class="border p-4 mb-3 rounded-lg shadow-sm bg-gray-50"
            >
              <p><strong>ID Anuncio:</strong> {{ ad._id }}</p>
              <p><strong>Biografía:</strong> {{ ad.biography }}</p>
              <p><strong>Perros Máx:</strong> {{ ad.maxDogs }}</p>
              <p><strong>Localidad:</strong> {{ ad.locality }}</p>
              <p><strong>Pausado:</strong> {{ ad.paused ? 'Sí' : 'No' }}</p>
              <div class="flex space-x-2 mt-2">
                <BaseButton
                  @click="handleUpdateAd(ad._id, { paused: !ad.paused })"
                  class="bg-purple-500 hover:bg-purple-600 text-white text-xs px-3 py-1"
                >
                  {{ ad.paused ? 'Activar' : 'Pausar' }}
                </BaseButton>
                <BaseButton
                  @click="handleDeleteAd(ad._id)"
                  class="bg-red-500 hover:bg-red-600 text-white text-xs px-3 py-1"
                  >Eliminar Anuncio</BaseButton
                >
              </div>
            </div>
          </div>
          <p v-else class="text-gray-600">No tiene anuncios.</p>

          <h3 class="text-lg font-semibold mt-6 mb-2 text-indigo-600">Perros (Propietario)</h3>
          <div v-if="selectedUser.dogs && selectedUser.dogs.length">
            <div
              v-for="dog in selectedUser.dogs"
              :key="dog._id"
              class="border p-4 mb-3 rounded-lg shadow-sm bg-gray-50"
            >
              <p><strong>ID Perro:</strong> {{ dog._id }}</p>
              <p><strong>Nombre:</strong> {{ dog.name }}</p>
              <p><strong>Raza:</strong> {{ dog.breed }}</p>
              <p><strong>Edad:</strong> {{ dog.age }}</p>
              <div class="flex space-x-2 mt-2">
                <BaseButton
                  @click="handleDeleteDog(dog._id)"
                  class="bg-red-500 hover:bg-red-600 text-white text-xs px-3 py-1"
                  >Eliminar Perro</BaseButton
                >
              </div>
            </div>
          </div>
          <p v-else class="text-gray-600">No tiene perros registrados.</p>

          <h3 class="text-lg font-semibold mt-6 mb-2 text-indigo-600">Solicitudes</h3>
          <div v-if="selectedUser.requests && selectedUser.requests.length">
            <div
              v-for="req in selectedUser.requests"
              :key="req._id"
              class="border p-4 mb-3 rounded-lg shadow-sm bg-gray-50"
            >
              <p><strong>ID Solicitud:</strong> {{ req._id }}</p>
              <p><strong>Fecha:</strong> {{ req.date }}</p>
              <p><strong>Estado:</strong> {{ req.status }}</p>
              <p>
                <strong>Dueño:</strong> {{ req.owner_info.name }} {{ req.owner_info.last_name }} ({{
                  req.owner_info.email
                }})
              </p>
              <p>
                <strong>Paseador:</strong> {{ req.walker_info.name }}
                {{ req.walker_info.last_name }} ({{ req.walker_info.email }})
              </p>
              <p>
                <strong>Perros Solicitados:</strong>
                <span v-if="req.dogs_info && req.dogs_info.length">
                  <span v-for="d_info in req.dogs_info" :key="d_info._id">
                    {{ d_info.name }} ({{ d_info.breed }})
                  </span>
                </span>
                <span v-else>N/A</span>
              </p>
              <div class="flex space-x-2 mt-2">
                <BaseButton
                  @click="handleUpdateRequest(req._id, { status: 'aceptada' })"
                  class="bg-green-500 hover:bg-green-600 text-white text-xs px-3 py-1"
                  :disabled="req.status !== 'pendiente'"
                  >Aceptar</BaseButton
                >
                <BaseButton
                  @click="handleUpdateRequest(req._id, { status: 'rechazada' })"
                  class="bg-yellow-500 hover:bg-yellow-600 text-white text-xs px-3 py-1"
                  :disabled="req.status !== 'pendiente'"
                  >Rechazar</BaseButton
                >
                <BaseButton
                  @click="handleDeleteRequest(req._id)"
                  class="bg-red-500 hover:bg-red-600 text-white text-xs px-3 py-1"
                  >Eliminar Solicitud</BaseButton
                >
              </div>
            </div>
          </div>
          <p v-else class="text-gray-600">No tiene solicitudes.</p>
        </div>
      </template>
    </Modal>
  </div>
</template>
