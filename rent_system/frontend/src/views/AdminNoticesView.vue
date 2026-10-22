<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { noticeApi } from '../api'

const list = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const form = reactive({ title: '', content: '' })

async function load() {
  loading.value = true
  try {
    const data = await noticeApi.list()
    list.value = data.results
  } finally {
    loading.value = false
  }
}

async function create() {
  if (!form.title || !form.content) {
    ElMessage.warning('请填写标题与内容')
    return
  }
  submitting.value = true
  try {
    await noticeApi.create({ ...form })
    ElMessage.success('公告已发布')
    dialogVisible.value = false
    form.title = ''
    form.content = ''
    load()
  } finally {
    submitting.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(`确定删除公告「${row.title}」吗？`, '删除公告', { type: 'warning' })
  await noticeApi.remove(row.id)
  ElMessage.success('已删除')
  load()
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <div style="margin-bottom: 14px">
      <el-button type="primary" @click="dialogVisible = true">
        <el-icon><Plus /></el-icon>发布公告
      </el-button>
    </div>

    <el-table :data="list" stripe>
      <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
      <el-table-column prop="content" label="内容" min-width="300" show-overflow-tooltip />
      <el-table-column prop="publisher_name" label="发布人" width="110">
        <template #default="{ row }">{{ row.publisher_name || '-' }}</template>
      </el-table-column>
      <el-table-column label="发布时间" width="160">
        <template #default="{ row }">{{ (row.created_at || '').slice(0, 16).replace('T', ' ') }}</template>
      </el-table-column>
      <el-table-column label="操作" width="90" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="danger" plain @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="发布公告" width="520px">
      <el-form label-width="60px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" placeholder="公告标题" />
        </el-form-item>
        <el-form-item label="内容" required>
          <el-input v-model="form.content" type="textarea" :rows="5" placeholder="公告正文" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="create">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>
