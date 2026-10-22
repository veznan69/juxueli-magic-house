<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuth } from '../store/auth'

const router = useRouter()
const { isLoggedIn, role, displayName, logout } = useAuth()

function onUserCommand(command) {
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
  <header class="nav">
    <div class="nav-inner">
      <router-link to="/" class="logo">
        <el-icon :size="22"><OfficeBuilding /></el-icon>
        <span>房屋租赁管理系统</span>
      </router-link>

      <nav class="links">
        <router-link to="/">首页找房</router-link>
        <router-link v-if="isLoggedIn" to="/profile">个人中心</router-link>
        <router-link v-if="role === 'landlord'" to="/landlord/houses">房东工作台</router-link>
        <router-link v-if="role === 'admin'" to="/admin">管理后台</router-link>
      </nav>

      <div class="right">
        <template v-if="!isLoggedIn">
          <el-button text class="ghost-btn" @click="router.push('/login')">登录</el-button>
          <el-button type="primary" round @click="router.push('/register')">注册</el-button>
        </template>
        <el-dropdown v-else @command="onUserCommand">
          <span class="user-chip">
            <el-avatar :size="30" class="avatar">{{ displayName.slice(0, 1).toUpperCase() }}</el-avatar>
            {{ displayName }}
            <el-icon><ArrowDown /></el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="/profile">个人中心</el-dropdown-item>
              <el-dropdown-item v-if="role === 'landlord'" command="/landlord/houses">
                房东工作台
              </el-dropdown-item>
              <el-dropdown-item v-if="role === 'admin'" command="/admin">管理后台</el-dropdown-item>
              <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<style scoped>
.nav {
  background: linear-gradient(135deg, #1e3a8a, #2563eb);
  color: #fff;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 12px rgba(30, 58, 138, 0.35);
}
.nav-inner {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  gap: 28px;
}
.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  font-size: 18px;
  font-weight: 700;
  text-decoration: none;
}
.links {
  display: flex;
  gap: 20px;
  flex: 1;
}
.links a {
  color: rgba(255, 255, 255, 0.85);
  text-decoration: none;
  font-size: 14px;
  padding: 4px 2px;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}
.links a:hover,
.links a.router-link-active {
  color: #fff;
  border-bottom-color: #93c5fd;
}
.right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.ghost-btn {
  color: rgba(255, 255, 255, 0.9);
}
.ghost-btn:hover {
  color: #fff;
}
.user-chip {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #fff;
  cursor: pointer;
  font-size: 14px;
  outline: none;
}
.avatar {
  background: #93c5fd;
  color: #1e3a8a;
  font-weight: 700;
}
</style>
