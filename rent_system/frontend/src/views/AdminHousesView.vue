<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { houseApi } from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(false)
const query = reactive({ page: 1, status: '', keyword: '' })

const statusMap = {
  pending: { text: '待审核', type: 'danger' },
  available: { text: '待租', type: 'success' },
  rented: { text: '已租', type: 'info' },
  offline: { text: '已下架', type: 'warning' },
}

async function load() {
  loading.value = true
  try {
    const data = await houseApi.adminList({ ...query })
    list.value = data.results
    total.value = data.count
  } finally {
    loading.value = false
  }
}

async function review(row, action) {
  if (action === 'reject') {
    await ElMessageBox.confirm(`驳回房源「${row.title}」后将从公开展示中下架，确定吗？`, '驳回房源', { type: 'warning' })
  }
  await houseApi.review(row.id, action)
  ElMessage.success(action === 'approve' ? '已通过审核并上架' : '已驳回下架')
  load()
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <div class="bar">
      <el-radio-group v-model="query.status" @change="() => { query.page = 1; load() }">
        <el-radio-button value="">全部</el-radio-button>
        <el-radio-button value="pending">待审核</el-radio-button>
        <el-radio-button value="available">待租</el-radio-button>
        <el-radio-button value="rented">已租</el-radio-button>
        <el-radio-button value="offline">已下架</el-radio-button>
      </el-radio-group>
      <el-input v-model="query.keyword" placeholder="按标题搜索" clearable style="width: 220px"
                @keyup.enter="() => { query.page = 1; load() }" />
    </div>

    <el-table :data="list" stripe>
      <el-table-column prop="title" label="标题" min-width="190" show-overflow-tooltip />
      <el-table-column prop="landlord_name" label="出租方" width="150" show-overflow-tooltip />
      <el-table-column prop="district" label="区域" width="90" />
      <el-table-column label="月租" width="90">
        <template #default="{ row }">¥{{ row.rent }}</template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="发布时间" width="110">
        <template #default="{ row }">{{ (row.created_at || '').slice(0, 10) }}</template>
      </el-table-column>
      <el-table-column label="操作" width="180" fixed="right">
        <template #default="{ row }">
          <template v-if="row.status === 'pending'">
            <el-button size="small" type="success" @click="review(row, 'approve')">通过</el-button>
            <el-button size="small" type="danger" plain @click="review(row, 'reject')">驳回</el-button>
          </template>
          <el-button v-else size="small" disabled>已处理</el-button>
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
  display: flex;
  gap: 14px;
  margin-bottom: 14px;
}
</style>
