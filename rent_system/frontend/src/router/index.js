import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuth } from '../store/auth'

import PublicLayout from '../components/PublicLayout.vue'
import DashboardLayout from '../components/DashboardLayout.vue'

const routes = [
  // ===== 公共区 =====
  {
    path: '/',
    component: PublicLayout,
    children: [
      {
        path: '',
        name: 'home',
        component: () => import('../views/HouseListView.vue'),
        meta: { title: '首页找房' },
      },
      {
        path: 'houses/:id',
        name: 'house-detail',
        component: () => import('../views/HouseDetailView.vue'),
        meta: { title: '房源详情' },
      },
      {
        path: 'login',
        name: 'login',
        component: () => import('../views/LoginView.vue'),
        meta: { title: '登录', guestOnly: true },
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('../views/RegisterView.vue'),
        meta: { title: '注册', guestOnly: true },
      },
      {
        path: 'notices',
        name: 'notices',
        component: () => import('../views/NoticeListView.vue'),
        meta: { title: '平台公告' },
      },
    ],
  },

  // ===== 租客端 =====
  {
    path: '/',
    component: DashboardLayout,
    props: { layout: 'user' },
    meta: { requiresAuth: true, roles: ['tenant'] },
    children: [
      { path: 'profile', component: () => import('../views/ProfileView.vue'), meta: { title: '个人中心' } },
      { path: 'favorites', component: () => import('../views/FavoritesView.vue'), meta: { title: '我的收藏' } },
      { path: 'appointments', component: () => import('../views/MyAppointmentsView.vue'), meta: { title: '我的预约' } },
      { path: 'contracts', component: () => import('../views/ContractsView.vue'), meta: { title: '我的合同' } },
      { path: 'bills', component: () => import('../views/BillsView.vue'), meta: { title: '我的账单' } },
      { path: 'repairs', component: () => import('../views/RepairsView.vue'), meta: { title: '我的报修' } },
    ],
  },

  // ===== 房东端 =====
  {
    path: '/landlord',
    component: DashboardLayout,
    props: { layout: 'landlord' },
    meta: { requiresAuth: true, roles: ['landlord'] },
    children: [
      { path: 'houses', component: () => import('../views/LandlordHousesView.vue'), meta: { title: '房源管理' } },
      { path: 'appointments', component: () => import('../views/LandlordAppointmentsView.vue'), meta: { title: '预约处理' } },
      { path: 'repairs', component: () => import('../views/LandlordRepairsView.vue'), meta: { title: '报修处理' } },
    ],
  },

  // ===== 管理后台 =====
  {
    path: '/admin',
    component: DashboardLayout,
    props: { layout: 'admin' },
    meta: { requiresAuth: true, roles: ['admin'] },
    children: [
      { path: '', component: () => import('../views/AdminDashboardView.vue'), meta: { title: '数据看板' } },
      { path: 'houses', component: () => import('../views/AdminHousesView.vue'), meta: { title: '房源审核' } },
      { path: 'users', component: () => import('../views/AdminUsersView.vue'), meta: { title: '用户管理' } },
      { path: 'notices', component: () => import('../views/AdminNoticesView.vue'), meta: { title: '公告管理' } },
    ],
  },

  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由守卫：登录态 + 角色校验
router.beforeEach((to) => {
  const { isLoggedIn, role } = useAuth()

  document.title = to.meta.title
    ? `${to.meta.title} - 房屋租赁管理系统`
    : '房屋租赁管理系统'

  // 已登录访问登录/注册页 → 回首页
  if (to.meta.guestOnly && isLoggedIn.value) {
    return { path: '/' }
  }
  if (to.meta.requiresAuth && !isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return { path: '/login', query: { next: to.fullPath } }
  }
  if (to.meta.roles && !to.meta.roles.includes(role.value)
      && !(role.value === 'admin' && to.meta.roles.includes('tenant'))) {
    ElMessage.error('无权访问该页面')
    return { path: '/' }
  }
  return true
})

export default router
