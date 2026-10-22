<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { repairApi } from '../api'

const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)

const form = reactive({ house_id: null, category: '水电', description: '' })
const myHouses = ref([])

const statusMap = {
  pending: { text: '待处理', type: 'warning' },
  processing: { text: '处理中', type: 'primary' },
  done: { text: '已完成', type: 'success' },
}

async function load() {
  loading.value = true
  try {
    const data = await repairApi.mine()
    list.value = data.results
    // 报修只能针对自己承租的房源（合同履行中的房子）
    const contracts = await import('../api').then((m) => m.contractApi.list())
    myHouses.value = contracts.results
      .filter((c) => c.status === 'active')
      .map((c) => ({ value: c.house, label: `${c.house_title}（${c.house_rooms}）` }))
  } finally {
    loading.value = false
  }
}

async function submit() {
  if (!form.house_id || !form.description) {
    ElMessage.warning('请选择房源并描述问题')
    return
  }
  submitting.value = true
  try {
    await repairApi.create({ house: form.house_id, category: form.category, description: form.description })
    ElMessage.success('报修已提交，等待房东处理')
    dialogVisible.value = false
    form.description = ''
    load()
  } finally {
    submitting.value = false
  }
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <div style="margin-bottom: 14px">
      <el-button type="primary" @click="dialogVisible = true">
        <el-icon><Plus /></el-icon>提交报修
      </el-button>
    </div>

    <el-table :data="list" stripe>
      <el-table-column label="房源" min-width="180">
        <template #default="{ row }">{{ row.house_title }}</template>
      </el-table-column>
      <el-table-column prop="category" label="类型" width="80" />
      <el-table-column prop="description" label="问题描述" min-width="180" show-overflow-tooltip />
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="reply" label="房东反馈" min-width="160" show-overflow-tooltip>
        <template #default="{ row }">{{ row.reply || '-' }}</template>
      </el-table-column>
      <el-table-column label="提交时间" width="110">
        <template #default="{ row }">{{ (row.created_at || '').slice(0, 10) }}</template>
      </el-table-column>
    </el-table>
    <el-empty v-if="!loading && list.length === 0" description="暂无报修记录" />

    <el-dialog v-model="dialogVisible" title="提交报修" width="480px">
      <el-form label-width="80px">
        <el-form-item label="房源" required>
          <el-select v-model="form.house_id" placeholder="选择承租中的房源" style="width: 100%">
            <el-option v-for="h in myHouses" :key="h.value" :value="h.value" :label="h.label" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-radio-group v-model="form.category">
            <el-radio-button v-for="c in ['水电', '门窗', '家电', '家具', '其他']"
                             :key="c" :value="c">{{ c }}</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="问题描述" required>
          <el-input v-model="form.description" type="textarea" :rows="3"
                    placeholder="请描述故障情况，如：厨房水龙头漏水" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>
