<script setup>
import { onMounted, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
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
    const data = await appointmentApi.mine()
    list.value = data.results
  } finally {
    loading.value = false
  }
}

async function cancel(row) {
  await ElMessageBox.confirm(`确定取消对「${row.house_title}」的预约吗？`, '取消预约')
  await appointmentApi.cancel(row.id)
  ElMessage.success('已取消预约')
  load()
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <el-alert type="info" :closable="false" style="margin-bottom: 14px"
              title="预约提交后由房东确认；确认后请按约定时间看房" />
    <el-table :data="list" stripe>
      <el-table-column label="房源" min-width="200">
        <template #default="{ row }">{{ row.house_title }}（{{ row.house_district }}）</template>
      </el-table-column>
      <el-table-column label="看房时间" width="170">
        <template #default="{ row }">{{ (row.visit_time || '').slice(0, 16).replace('T', ' ') }}</template>
      </el-table-column>
      <el-table-column prop="phone" label="联系电话" width="130" />
      <el-table-column prop="remark" label="备注" min-width="140" show-overflow-tooltip />
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="danger" plain
                     @click="cancel(row)">取消</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
