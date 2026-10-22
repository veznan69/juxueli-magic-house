import { computed, reactive } from 'vue'

// 轻量全局状态：token + 当前用户（localStorage 持久化）
const state = reactive({
  token: localStorage.getItem('token') || '',
  user: JSON.parse(localStorage.getItem('user') || 'null'),
})

export function useAuth() {
  const isLoggedIn = computed(() => !!state.token)
  const role = computed(() => state.user?.role || '')
  const displayName = computed(() => state.user?.username || '未登录')

  function setAuth(token, user) {
    state.token = token
    state.user = user
    localStorage.setItem('token', token)
    localStorage.setItem('user', JSON.stringify(user))
  }

  function setUser(user) {
    state.user = user
    localStorage.setItem('user', JSON.stringify(user))
  }

  function logout() {
    state.token = ''
    state.user = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  return { state, isLoggedIn, role, displayName, setAuth, setUser, logout }
}
