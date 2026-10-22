<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { appointmentApi } from '../api'

const list = ref([])
const loading = ref(false)

const statusMap = {
  pending: { text: '待确认', type: 'warning' },
  confirmed: { text: '已确认', type: 'success' },
  rejected: { text: '已拒绝', type: 'danger' },
  done: { text: '已完成', type: 'info' },
}

async function load() {
  loading.value = true
  try {
    const data = await appointmentApi.landlordList()
    list.value = data.results
  } finally {
    loading.value = false
  }
}

async function handle(row, status, tip) {
  await appointmentApi.handle(row.id, status)
  ElMessage.success(tip)
  load()
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <el-table :data="list" stripe>
      <el-table-column label="房源" min-width="180">
        <template #default="{ row }">{{ row.house_title }}</template>
      </el-table-column>
      <el-table-column prop="tenant_name" label="租客" width="100" />
      <el-table-column label="看房时间" width="160">
        <template #default="{ row }">{{ (row.visit_time || '').slice(0, 16).replace('T', ' ') }}</template>
      </el-table-column>
      <el-table-column prop="phone" label="联系电话" width="130" />
      <el-table-column prop="remark" label="备注" min-width="130" show-overflow-tooltip />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <template v-if="row.status === 'pending'">
            <el-button size="small" type="success" @click="handle(row, 'confirmed', '已确认预约')">确认</el-button>
            <el-button size="small" type="danger" plain @click="handle(row, 'rejected', '已拒绝预约')">拒绝</el-button>
          </template>
          <el-button v-if="row.status === 'confirmed'" size="small" type="primary" plain
                     @click="handle(row, 'done', '已完成看房')">完成看房</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && list.length === 0" description="暂无预约" />
  </div>
</template>
