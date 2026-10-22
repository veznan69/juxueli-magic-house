<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { adminApi } from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(false)
const page = ref(1)

const roleMap = { tenant: '租客', landlord: '房东', admin: '管理员' }

async function load() {
  loading.value = true
  try {
    const data = await adminApi.users({ page: page.value })
    list.value = data.results
    total.value = data.count
  } finally {
    loading.value = false
  }
}

async function setActive(row) {
  const action = row.is_active ? '停用' : '启用'
  await ElMessageBox.confirm(`确定${action}账号「${row.username}」吗？`, `${action}账号`)
  const data = await adminApi.setActive(row.id, !row.is_active)
  Object.assign(row, data)
  ElMessage.success(`已${action}`)
}

async function setRole(row) {
  const { value } = await ElMessageBox.prompt(
    `调整「${row.username}」的角色（tenant=租客 / landlord=房东 / admin=管理员）`,
    '调整角色', { inputValue: row.role, inputPattern: /^(tenant|landlord|admin)$/ , inputErrorMessage: '请输入 tenant / landlord / admin' })
  const data = await adminApi.setRole(row.id, value.trim())
  Object.assign(row, data)
  ElMessage.success('角色已调整')
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <el-table :data="list" stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" width="130" />
      <el-table-column label="角色" width="110">
        <template #default="{ row }">
          <el-tag :type="{ tenant: 'info', landlord: 'success', admin: 'danger' }[row.role]" size="small">
            {{ roleMap[row.role] || row.role }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="phone" label="手机号" width="130">
        <template #default="{ row }">{{ row.phone || '-' }}</template>
      </el-table-column>
      <el-table-column prop="email" label="邮箱" min-width="160">
        <template #default="{ row }">{{ row.email || '-' }}</template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'warning'" size="small">
            {{ row.is_active ? '正常' : '停用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="注册时间" width="110">
        <template #default="{ row }">{{ (row.date_joined || '').slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="170" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="setRole(row)" :disabled="row.is_superuser">调角色</el-button>
          <el-button size="small" :type="row.is_active ? 'danger' : 'success'" plain
                     :disabled="row.is_superuser" @click="setActive(row)">
            {{ row.is_active ? '停用' : '启用' }}
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="display: flex; justify-content: center; margin-top: 16px" v-if="total > 10">
      <el-pagination v-model:current-page="page" :page-size="10" :total="total"
                     layout="prev, pager, next" background @current-change="load" />
    </div>
  </div>
</template>
