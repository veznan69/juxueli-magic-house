<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { repairApi } from '../api'

const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const current = ref(null)
const form = reactive({ status: 'processing', reply: '' })

const statusMap = {
  pending: { text: '待处理', type: 'warning' },
  processing: { text: '处理中', type: 'primary' },
  done: { text: '已完成', type: 'success' },
}

async function load() {
  loading.value = true
  try {
    const data = await repairApi.landlordList()
    list.value = data.results
  } finally {
    loading.value = false
  }
}

function openHandle(row, status) {
  current.value = row
  form.status = status
  form.reply = row.reply || ''
  dialogVisible.value = true
}

async function submit() {
  submitting.value = true
  try {
    await repairApi.handle(current.value.id, { status: form.status, reply: form.reply })
    ElMessage.success('处理结果已保存')
    dialogVisible.value = false
    load()
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <el-table :data="list" stripe>
      <el-table-column label="房源" min-width="170">
        <template #default="{ row }">{{ row.house_title }}</template>
      </el-table-column>
      <el-table-column prop="tenant_name" label="报修人" width="90" />
      <el-table-column prop="category" label="类型" width="80" />
      <el-table-column prop="description" label="问题描述" min-width="170" show-overflow-tooltip />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="reply" label="处理反馈" min-width="150" show-overflow-tooltip>
        <template #default="{ row }">{{ row.reply || '-' }}</template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button v-if="row.status === 'pending'" size="small" type="primary"
                     @click="openHandle(row, 'processing')">开始处理</el-button>
          <el-button v-if="row.status !== 'done'" size="small" type="success" plain
                     @click="openHandle(row, 'done')">完成</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && list.length === 0" description="暂无报修工单" />

    <el-dialog v-model="dialogVisible" title="处理报修" width="460px">
      <el-form label-width="80px">
        <el-form-item label="处理状态">
          <el-radio-group v-model="form.status">
            <el-radio-button value="processing">处理中</el-radio-button>
            <el-radio-button value="done">已完成</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="处理反馈">
          <el-input v-model="form.reply" type="textarea" :rows="3"
                    placeholder="如：已联系师傅，周四上午上门维修" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
