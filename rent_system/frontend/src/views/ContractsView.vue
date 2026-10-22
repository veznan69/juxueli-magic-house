<script setup>
import { onMounted, ref } from 'vue'
import { contractApi } from '../api'

const list = ref([])
const loading = ref(false)

const statusMap = {
  active: { text: '履行中', type: 'success' },
  expired: { text: '已到期', type: 'info' },
  terminated: { text: '已解约', type: 'danger' },
}

onMounted(async () => {
  loading.value = true
  try {
    const data = await contractApi.list()
    list.value = data.results
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div v-loading="loading">
    <el-table :data="list" stripe>
      <el-table-column label="房源" min-width="200">
        <template #default="{ row }">{{ row.house_title }}（{{ row.house_rooms }}）</template>
      </el-table-column>
      <el-table-column prop="start_date" label="起租日" width="110" />
      <el-table-column prop="end_date" label="到期日" width="110" />
      <el-table-column label="月租金" width="110">
        <template #default="{ row }">¥{{ row.monthly_rent }}</template>
      </el-table-column>
      <el-table-column label="押金" width="100">
        <template #default="{ row }">¥{{ row.deposit }}</template>
      </el-table-column>
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="签订时间" width="110">
        <template #default="{ row }">{{ (row.created_at || '').slice(0, 10) }}</template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && list.length === 0" description="暂无合同，预约看房满意后即可签约" />
  </div>
</template>
