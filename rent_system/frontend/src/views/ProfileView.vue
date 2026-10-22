<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { authApi } from '../api'
import { useAuth } from '../store/auth'

const { setUser, displayName, role } = useAuth()
const loading = ref(false)
const form = reactive({ username: '', phone: '', email: '' })

onMounted(async () => {
  loading.value = true
  try {
    const me = await authApi.me()
    Object.assign(form, { username: me.username, phone: me.phone, email: me.email })
    setUser(me)
  } finally {
    loading.value = false
  }
})

async function save() {
  const data = await authApi.updateMe({ phone: form.phone, email: form.email })
  setUser(data)
  ElMessage.success('个人信息已更新')
}
</script>

<template>
  <div class="card-plain" v-loading="loading" style="max-width: 560px">
    <div class="head">
      <el-avatar :size="56" style="background: #2563eb; font-size: 24px">
        {{ displayName.slice(0, 1).toUpperCase() }}
      </el-avatar>
      <div>
        <div class="uname">{{ displayName }}</div>
        <el-tag size="small">{{ { tenant: '租客', landlord: '房东', admin: '管理员' }[role] }}</el-tag>
      </div>
    </div>

    <el-form label-width="80px" style="margin-top: 20px">
      <el-form-item label="用户名">
        <el-input :model-value="form.username" disabled />
      </el-form-item>
      <el-form-item label="手机号">
        <el-input v-model="form.phone" placeholder="填写手机号方便联系" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" placeholder="选填" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="save">保存修改</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.head {
  display: flex;
  align-items: center;
  gap: 14px;
}
.uname {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}
</style>
