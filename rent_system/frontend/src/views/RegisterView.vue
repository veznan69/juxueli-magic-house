<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { authApi } from '../api'
import { useAuth } from '../store/auth'

const router = useRouter()
const { setAuth } = useAuth()

const form = reactive({
  username: '',
  password: '',
  password2: '',
  phone: '',
  role: 'tenant',
})
const loading = ref(false)

async function submit() {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  if (form.password.length < 6) {
    ElMessage.warning('密码至少 6 位')
    return
  }
  if (form.password !== form.password2) {
    ElMessage.warning('两次输入的密码不一致')
    return
  }
  loading.value = true
  try {
    const data = await authApi.register({
      username: form.username,
      password: form.password,
      phone: form.phone,
      role: form.role,
    })
    setAuth(data.token, data.user)
    ElMessage.success('注册成功，欢迎加入！')
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-wrap">
    <div class="auth-card">
      <h2>注册账号</h2>
      <p class="sub">选择你的角色，一分钟后开始找房 / 发布房源</p>
      <el-form label-position="top" @keyup.enter="submit">
        <el-form-item label="注册身份">
          <el-radio-group v-model="form.role" size="large">
            <el-radio-button value="tenant">我要租房（租客）</el-radio-button>
            <el-radio-button value="landlord">我要出租（房东）</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="3 位以上字母或数字" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="方便房东 / 平台联系你" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="至少 6 位" />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input v-model="form.password2" type="password" show-password placeholder="再输入一次" />
        </el-form-item>
        <el-button type="primary" size="large" style="width: 100%" :loading="loading" @click="submit">
          注 册
        </el-button>
      </el-form>
      <p class="swap">
        已有账号？<router-link to="/login">去登录</router-link>
      </p>
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
  width: 440px;
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
</style>
