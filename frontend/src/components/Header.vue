<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useAuth } from '@/composables/useAuth'
import type { UserRole } from '@/composables/useAuth'

const {
  authDialogOpen,
  authMode,
  isAuthenticated,
  isDoctor,
  currentUser,
  openAuthDialog,
  closeAuthDialog,
  login,
  register,
  logout,
} = useAuth()

const isRegisterMode = computed(() => authMode.value === 'register')
const loading = ref(false)
const errorMessage = ref('')
const form = reactive<{ username: string; password: string; confirmPassword: string; role: UserRole }>(
  {
    username: '',
    password: '',
    confirmPassword: '',
    role: 'user',
  },
)

const roleOptions: Array<{ label: string; value: UserRole }> = [
  { label: 'Utilisateur', value: 'user' },
  { label: 'Docteur', value: 'doctor' },
]

function resetForm() {
  form.username = ''
  form.password = ''
  form.confirmPassword = ''
  form.role = 'user'
  errorMessage.value = ''
  loading.value = false
}

watch(authDialogOpen, (open) => {
  if (open) {
    resetForm()
  }
})

watch(authMode, () => {
  resetForm()
})

function toggleMode() {
  authMode.value = isRegisterMode.value ? 'login' : 'register'
}

function handleClose() {
  closeAuthDialog()
}

function validatePasswords() {
  if (isRegisterMode.value && form.password !== form.confirmPassword) {
    throw new Error('Les mots de passe ne correspondent pas.')
  }
}

async function submitAuth() {
  if (loading.value) return
  try {
    loading.value = true
    validatePasswords()
    if (isRegisterMode.value) {
      register(form.username, form.password, form.role)
    } else {
      login(form.username, form.password)
    }
    handleClose()
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : 'Erreur inconnue.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-app-bar
    app
    elevation="2"
    class="header-bar"
  >
    <v-container fluid class="container-header">
      <div class="d-flex align-center">
        <v-img
          src="@/assets/logo_app_head.png"
          class="logo"
          contain
        />
        <v-app-bar-title class="title">AstroMetric</v-app-bar-title>
      </div>

      <div class="btn-container">
        <v-btn class="btn-menu" to="/">
          <v-icon class="icon-btn">mdi-home</v-icon>
          Home
        </v-btn>

        <template v-if="isAuthenticated">
          <v-menu>
            <template #activator="{ props }">
              <v-btn class="btn-menu" v-bind="props">
                <v-icon class="icon-btn">{{ isDoctor ? 'mdi-school' : 'mdi-account' }}</v-icon>
                {{ currentUser?.username }}
              </v-btn>
            </template>
            <v-list>
              <v-list-subheader>Profil</v-list-subheader>
              <v-list-item>
                <v-list-item-title>Rôle : {{ isDoctor ? 'Docteur' : 'Utilisateur' }}</v-list-item-title>
              </v-list-item>
              <v-divider class="my-2" />
              <v-list-item @click="logout">
                <v-list-item-title>Se déconnecter</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
        <template v-else>
          <v-btn class="btn-menu" @click="openAuthDialog('login')">
            <v-icon class="icon-btn">mdi-account</v-icon>
            Login
          </v-btn>
        </template>

        <v-btn class="btn-menu" to="/FAQ/page_faq">
          <v-icon class="icon-btn">mdi-magnify</v-icon>
          FAQ
        </v-btn>
      </div>
    </v-container>

    <v-dialog v-model="authDialogOpen" max-width="420">
      <v-card>
        <v-card-title class="text-center">
          {{ isRegisterMode ? 'Créer un compte' : 'Se connecter' }}
        </v-card-title>
        <v-card-text>
          <v-form @submit.prevent="submitAuth">
            <v-text-field
              v-model="form.username"
              label="Nom d'utilisateur"
              prepend-inner-icon="mdi-account"
              autocomplete="username"
              density="comfortable"
              required
            />
            <v-text-field
              v-model="form.password"
              label="Mot de passe"
              type="password"
              prepend-inner-icon="mdi-lock"
              autocomplete="current-password"
              density="comfortable"
              required
            />
            <v-text-field
              v-if="isRegisterMode"
              v-model="form.confirmPassword"
              label="Confirmer le mot de passe"
              type="password"
              prepend-inner-icon="mdi-lock-check"
              autocomplete="new-password"
              density="comfortable"
              required
            />
            <v-select
              v-if="isRegisterMode"
              v-model="form.role"
              :items="roleOptions"
              item-title="label"
              item-value="value"
              label="Votre rôle"
              prepend-inner-icon="mdi-account-tie"
              density="comfortable"
              required
            />

            <v-alert
              v-if="errorMessage"
              type="error"
              class="mt-2"
              density="comfortable"
            >
              {{ errorMessage }}
            </v-alert>

            <v-btn
              class="mt-4"
              color="primary"
              block
              :loading="loading"
              :disabled="loading"
              type="submit"
            >
              {{ isRegisterMode ? "S'inscrire" : 'Connexion' }}
            </v-btn>
          </v-form>
        </v-card-text>
        <v-card-actions class="justify-center">
          <v-btn variant="text" @click="toggleMode">
            {{ isRegisterMode ? 'Déjà un compte ? Se connecter' : "Pas de compte ? S'inscrire" }}
          </v-btn>
          <v-btn variant="text" @click="handleClose">Fermer</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app-bar>
</template>

<style scoped>
.container-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #222222;
}

.header-bar {
  color: #fff;
  padding: 0;
  margin: 0;
}

.logo {
  width: 48px;
  height: 48px;
}

.title {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
  font-size: 1.4rem;
  color: #cbffed;
}

.title :deep(.v-toolbar-title__placeholder) {
  overflow: visible;
}

.btn-container {
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 25%;
}

.btn-menu {
  background: transparent;
  color: #cbffed;
  transition: all 0.3s ease;
}

.icon-btn {
  margin-right: 7px;
}
</style>
