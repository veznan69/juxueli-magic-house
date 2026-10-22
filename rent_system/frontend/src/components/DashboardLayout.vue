<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuth } from '../store/auth'

const props = defineProps({
  layout: { type: String, required: true }, // user | landlord | admin
})

const route = useRoute()
const router = useRouter()
const { displayName, role, logout } = useAuth()

const titles = {
  user: '用户中心',
  landlord: '房东工作台',
  admin: '管理后台',
}
const title = computed(() => titles[props.layout])

const menus = {
  user: [
    { path: '/profile', icon: 'User', label: '个人中心' },
    { path: '/favorites', icon: 'Star', label: '我的收藏' },
    { path: '/appointments', icon: 'Calendar', label: '我的预约' },
    { path: '/contracts', icon: 'Tickets', label: '我的合同' },
    { path: '/bills', icon: 'Wallet', label: '我的账单' },
    { path: '/repairs', icon: 'Tools', label: '我的报修' },
  ],
  landlord: [
    { path: '/landlord/houses', icon: 'House', label: '房源管理' },
    { path: '/landlord/appointments', icon: 'Calendar', label: '预约处理' },
    { path: '/landlord/repairs', icon: 'Tools', label: '报修处理' },
  ],
  admin: [
    { path: '/admin', icon: 'DataAnalysis', label: '数据看板' },
    { path: '/admin/houses', icon: 'House', label: '房源审核' },
    { path: '/admin/users', icon: 'UserFilled', label: '用户管理' },
    { path: '/admin/notices', icon: 'Bell', label: '公告管理' },
  ],
}
const menuItems = computed(() => menus[props.layout])

function onCommand(command) {
  if (command === 'logout') {
    logout()
    ElMessage.success('已退出登录')
    router.push('/')
  } else {
    router.push(command)
  }
}
</script>

<template>
  <el-container class="dash">
    <el-aside width="220px" class="aside">
      <div class="aside-brand" @click="router.push('/')">
        <el-icon :size="20"><OfficeBuilding /></el-icon>
        <span>{{ title }}</span>
      </div>
      <el-menu :default-active="route.path" router class="aside-menu">
        <el-menu-item v-for="m in menuItems" :key="m.path" :index="m.path">
          <el-icon><component :is="m.icon" /></el-icon>
          <span>{{ m.label }}</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="topbar">
        <span class="topbar-title">{{ title }}</span>
        <el-dropdown @command="onCommand">
          <span class="topbar-user">
            <el-avatar :size="28">{{ displayName.slice(0, 1).toUpperCase() }}</el-avatar>
            {{ displayName }}
            <el-tag v-if="role" size="small" effect="plain">
              {{ { tenant: '租客', landlord: '房东', admin: '管理员' }[role] }}
            </el-tag>
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="/">回到首页</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main class="main-area">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.dash {
  min-height: 100vh;
}
.aside {
  background: #fff;
  border-right: 1px solid var(--border);
}
.aside-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  height: 60px;
  padding: 0 20px;
  font-weight: 700;
  color: #1e40af;
  cursor: pointer;
  border-bottom: 1px solid var(--border);
}
.aside-menu {
  border-right: none;
}
.topbar {
  background: #fff;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.topbar-title {
  font-weight: 600;
  color: #1e293b;
}
.topbar-user {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  outline: none;
  color: var(--text);
}
.main-area {
  background: var(--bg);
  padding: 20px;
}
</style>
