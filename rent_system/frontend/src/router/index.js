import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: '首页' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 路由标题同步
router.afterEach((to) => {
  document.title = to.meta.title
    ? `${to.meta.title} - 房屋租赁管理系统`
    : '房屋租赁管理系统'
})

export default router
