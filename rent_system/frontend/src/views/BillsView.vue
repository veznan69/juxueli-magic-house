<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { billApi } from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(false)
const paying = ref(0)
const query = reactive({ page: 1, status: '' })

const statusMap = {
  unpaid: { text: '待缴', type: 'warning' },
  paid: { text: '已缴', type: 'success' },
  overdue: { text: '逾期', type: 'danger' },
}

async function load() {
  loading.value = true
  try {
    const data = await billApi.list({ ...query })
    list.value = data.results
    total.value = data.count
  } finally {
    loading.value = false
  }
}

async function pay(row) {
  paying.value = row.id
  try {
    await billApi.pay(row.id)
    ElMessage.success(`账单 ${row.period} 缴费成功`)
    load()
  } finally {
    paying.value = 0
  }
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <div class="bar">
      <el-radio-group v-model="query.status" @change="() => { query.page = 1; load() }">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button value="unpaid">待缴</el-radio-button>
        <el-radio-button value="overdue">逾期</el-radio-button>
        <el-radio-button value="paid">已缴</el-radio-button>
      </el-radio-group>
    </div>

    <el-table :data="list" stripe>
      <el-table-column label="账期" width="100">
        <template #default="{ row }">{{ row.period }}</template>
      </el-table-column>
      <el-table-column label="房源" min-width="200">
        <template #default="{ row }">{{ row.house_title }}</template>
      </el-table-column>
      <el-table-column label="金额" width="110">
        <template #default="{ row }">¥{{ row.amount }}</template>
      </el-table-column>
      <el-table-column prop="due_date" label="应缴日" width="110" />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="缴费时间" width="160">
        <template #default="{ row }">
          {{ row.paid_at ? row.paid_at.slice(0, 16).replace('T', ' ') : '-' }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="110" fixed="right">
        <template #default="{ row }">
          <el-button
            v-if="row.status !== 'paid'"
            type="primary"
            size="small"
            :loading="paying === row.id"
            @click="pay(row)"
          >缴费</el-button>
        </template>
      </el-table-column>
    </el-table>

    <div style="display: flex; justify-content: center; margin-top: 16px" v-if="total > 10">
      <el-pagination v-model:current-page="query.page" :page-size="10" :total="total"
                     layout="prev, pager, next" background @current-change="load" />
    </div>
  </div>
</template>

<style scoped>
.bar {
  margin-bottom: 14px;
}
</style>
