<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authApi } from '../api'
import { useAuth } from '../store/auth'

const route = useRoute()
const router = useRouter()
const { setAuth } = useAuth()

const form = reactive({ username: '', password: '' })
const loading = ref(false)

async function submit() {
  if (!form.username || !form.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    const data = await authApi.login(form)
    setAuth(data.token, data.user)
    ElMessage.success(`欢迎回来，${data.user.username}`)
    router.push(route.query.next || '/')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-wrap">
    <div class="auth-card">
      <h2>登录</h2>
      <p class="sub">登录后可收藏房源、预约看房、管理合同账单</p>
      <el-form label-position="top" @keyup.enter="submit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" size="large">
            <template #prefix><el-icon><User /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="请输入密码" size="large">
            <template #prefix><el-icon><Lock /></el-icon></template>
          </el-input>
        </el-form-item>
        <el-button type="primary" size="large" style="width: 100%" :loading="loading" @click="submit">
          登 录
        </el-button>
      </el-form>
      <p class="swap">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
      <el-divider>演示账号</el-divider>
      <div class="demo-accounts">
        <el-tag @click="form.username = 'admin'; form.password = 'admin123456'">管理员 admin / admin123456</el-tag>
        <el-tag type="success" @click="form.username = 'landlord'; form.password = 'landlord123'">房东 landlord / landlord123</el-tag>
        <el-tag type="warning" @click="form.username = 'tenant1'; form.password = 'tenant123'">租客 tenant1 / tenant123</el-tag>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-wrap {
  min-height: calc(100vh - 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1e3a8a, #2563eb);
  padding: 24px;
}
.auth-card {
  width: 420px;
  background: #fff;
  border-radius: 16px;
  padding: 36px 40px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.25);
}
h2 {
  color: #1e40af;
  margin-bottom: 4px;
}
.sub {
  color: var(--muted);
  font-size: 13px;
  margin-bottom: 18px;
}
.swap {
  text-align: center;
  color: var(--muted);
  font-size: 13px;
  margin-top: 14px;
}
.swap a {
  color: #2563eb;
}
.demo-accounts {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: center;
}
.demo-accounts .el-tag {
  cursor: pointer;
}
</style>
