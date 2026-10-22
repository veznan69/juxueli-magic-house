import axios from 'axios'
import request from './request'

// 健康检查在 /api/health/（不在 v1 命名空间内），单独走一次 axios
export const healthApi = {
  ping: () => axios.get('/api/health/', { timeout: 5000 }).then((r) => r.data),
}

export const authApi = {
  register: (data) => request.post('/auth/register/', data),
  login: (data) => request.post('/auth/login/', data),
  me: () => request.get('/auth/me/'),
  updateMe: (data) => request.patch('/auth/me/', data),
}

export const houseApi = {
  list: (params) => request.get('/houses/', { params }),
  detail: (id) => request.get(`/houses/${id}/`),
  mine: () => request.get('/houses/mine/'),
  create: (data) => request.post('/houses/', data),
  update: (id, data) => request.patch(`/houses/${id}/`, data),
  remove: (id) => request.delete(`/houses/${id}/`),
  setStatus: (id, status) =>
    request.post(`/houses/${id}/set-status/`, { status }),
  adminList: (params) => request.get('/admin-houses/', { params }),
  review: (id, action, reason = '') =>
    request.post(`/houses/${id}/review/`, { action, reason }),
}

export const appointmentApi = {
  mine: () => request.get('/appointments/'),
  create: (data) => request.post('/appointments/', data),
  cancel: (id) => request.delete(`/appointments/${id}/`),
  landlordList: () => request.get('/landlord/appointments/'),
  handle: (id, status) => request.post(`/landlord/appointments/${id}/handle/`, { status }),
}

export const contractApi = {
  list: () => request.get('/contracts/'),
}

export const billApi = {
  list: (params) => request.get('/bills/', { params }),
  pay: (id) => request.post(`/bills/${id}/pay/`),
}

export const repairApi = {
  mine: () => request.get('/repairs/'),
  create: (data) => request.post('/repairs/', data),
  landlordList: () => request.get('/landlord/repairs/'),
  handle: (id, data) => request.post(`/landlord/repairs/${id}/handle/`, data),
}

export const favoriteApi = {
  list: () => request.get('/favorites/'),
  toggle: (houseId) => request.post('/favorites/toggle/', { house_id: houseId }),
}

export const noticeApi = {
  list: (params) => request.get('/notices/', { params }),
  create: (data) => request.post('/notices/', data),
  remove: (id) => request.delete(`/notices/${id}/`),
}

export const adminApi = {
  users: (params) => request.get('/admin-users/', { params }),
  setActive: (id, active) => request.post(`/admin-users/${id}/set-active/`, { active }),
  setRole: (id, role) => request.post(`/admin-users/${id}/set-role/`, { role }),
  stats: () => request.get('/stats/'),
}

// 房源封面渐变色占位：按 id 稳定取色
const GRADIENTS = [
  'linear-gradient(135deg,#2563eb,#60a5fa)',
  'linear-gradient(135deg,#059669,#34d399)',
  'linear-gradient(135deg,#7c3aed,#a78bfa)',
  'linear-gradient(135deg,#ea580c,#fb923c)',
  'linear-gradient(135deg,#0891b2,#22d3ee)',
  'linear-gradient(135deg,#db2777,#f472b6)',
]

export function coverStyle(house) {
  if (house.cover) {
    return { backgroundImage: `url(${house.cover})`, backgroundSize: 'cover' }
  }
  const idx = (house.id || 0) % GRADIENTS.length
  return { background: GRADIENTS[idx] }
}
