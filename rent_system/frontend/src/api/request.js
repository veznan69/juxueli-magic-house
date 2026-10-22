import axios from 'axios'

const service = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

service.interceptors.request.use(
  (config) => config,
  (error) => Promise.reject(error),
)

service.interceptors.response.use(
  (response) => response.data,
  (error) => {
    // 统一错误处理：打印并向上抛出，由页面自行展示提示
    const msg = error.response?.data?.detail || error.message || '网络请求失败'
    console.error('[API Error]', msg)
    return Promise.reject(error)
  },
)

export default service
