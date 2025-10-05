import { computed, ref } from 'vue'

export type AuthMode = 'login' | 'register'
export type UserRole = 'user' | 'doctor'

export type StoredUser = {
  username: string
  password: string
  role: UserRole
}

const USERS_KEY = 'astro_auth_users'
const SESSION_KEY = 'astro_auth_session'

const storedUsers = ref<StoredUser[]>([])
const currentUser = ref<StoredUser | null>(null)
const authDialogOpen = ref(false)
const authMode = ref<AuthMode>('login')

function normalizeUser(rawUser: any): StoredUser | null {
  if (!rawUser || typeof rawUser.username !== 'string' || typeof rawUser.password !== 'string') {
    return null
  }

  const role: UserRole = rawUser.role === 'doctor' ? 'doctor' : 'user'
  return { username: rawUser.username, password: rawUser.password, role }
}

function loadUsers() {
  const raw = typeof window !== 'undefined' ? localStorage.getItem(USERS_KEY) : null
  if (raw) {
    try {
      const parsed = JSON.parse(raw)
      const users: StoredUser[] = Array.isArray(parsed)
        ? parsed
            .map(normalizeUser)
            .filter((user): user is StoredUser => user !== null)
        : []
      storedUsers.value = users
    } catch (err) {
      console.error('Unable to parse stored users', err)
      storedUsers.value = []
    }
  }
}

function loadSession() {
  const raw = typeof window !== 'undefined' ? localStorage.getItem(SESSION_KEY) : null
  if (raw) {
    try {
      currentUser.value = normalizeUser(JSON.parse(raw))
    } catch (err) {
      console.error('Unable to parse stored session', err)
      currentUser.value = null
    }
  }
}

if (typeof window !== 'undefined') {
  loadUsers()
  loadSession()
}

function persistUsers() {
  localStorage.setItem(USERS_KEY, JSON.stringify(storedUsers.value))
}

function persistSession() {
  if (currentUser.value) {
    localStorage.setItem(SESSION_KEY, JSON.stringify(currentUser.value))
  } else {
    localStorage.removeItem(SESSION_KEY)
  }
}

function register(username: string, password: string, role: UserRole) {
  const trimmed = username.trim()
  if (!trimmed || !password) {
    throw new Error('Identifiants requis.')
  }
  const exists = storedUsers.value.some((user) => user.username.toLowerCase() === trimmed.toLowerCase())
  if (exists) {
    throw new Error('Ce compte existe déjà.')
  }

  const normalizedRole: UserRole = role === 'doctor' ? 'doctor' : 'user'
  const newUser: StoredUser = { username: trimmed, password, role: normalizedRole }
  storedUsers.value.push(newUser)
  currentUser.value = newUser
  persistUsers()
  persistSession()
}

function login(username: string, password: string) {
  const trimmed = username.trim()
  if (!trimmed || !password) {
    throw new Error('Identifiants requis.')
  }

  const match = storedUsers.value.find(
    (user) => user.username.toLowerCase() === trimmed.toLowerCase() && user.password === password,
  )
  if (!match) {
    throw new Error('Identifiants incorrects.')
  }

  currentUser.value = match
  persistSession()
}

function logout() {
  currentUser.value = null
  persistSession()
}

function openAuthDialog(mode: AuthMode = 'login') {
  authMode.value = mode
  authDialogOpen.value = true
}

function closeAuthDialog() {
  authDialogOpen.value = false
}

export function useAuth() {
  const isAuthenticated = computed(() => currentUser.value !== null)
  const isDoctor = computed(() => currentUser.value?.role === 'doctor')

  return {
    authDialogOpen,
    authMode,
    currentUser,
    isAuthenticated,
    isDoctor,
    login,
    register,
    logout,
    openAuthDialog,
    closeAuthDialog,
  }
}
