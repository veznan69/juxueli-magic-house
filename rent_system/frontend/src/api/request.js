import axios from 'axios'
import { ElMessage } from 'element-plus'

const service = axios.create({
  baseURL: '/api/v1',
  timeout: 10000,
})

// 请求拦截：自动携带 Token
service.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Token ${token}`
  return config
})

// 响应拦截：直接返回 data；401 清登录态跳登录页
service.interceptors.response.use(
  (response) => response.data,
  (error) => {
    const status = error.response?.status
    const data = error.response?.data
    let msg = data?.detail || data?.message
    if (!msg && data && typeof data === 'object') {
      msg = Object.values(data).flat().join('；')
    }
    msg = msg || error.message || '网络请求失败'
    if (status === 401 && !location.pathname.startsWith('/login')) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      ElMessage.warning('登录已失效，请重新登录')
      location.href = '/login'
    } else {
      ElMessage.error(String(msg).slice(0, 120))
    }
    return Promise.reject(error)
  },
)

export default service
