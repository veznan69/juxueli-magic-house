<script setup>
import { onMounted, ref } from 'vue'
import { noticeApi } from '../api'

const notices = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const data = await noticeApi.list()
    notices.value = data.results
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page-wrap" v-loading="loading">
    <h2 class="page-title">平台公告</h2>
    <el-empty v-if="!loading && notices.length === 0" description="暂无公告" />
    <div v-for="n in notices" :key="n.id" class="card-plain hover-lift">
      <div class="n-head">
        <el-icon class="bell"><BellFilled /></el-icon>
        <span class="n-title">{{ n.title }}</span>
        <span class="n-time">{{ (n.created_at || '').slice(0, 16).replace('T', ' ') }}</span>
      </div>
      <p class="n-content">{{ n.content }}</p>
      <p class="n-publisher" v-if="n.publisher_name">发布人：{{ n.publisher_name }}</p>
    </div>
  </div>
</template>

<style scoped>
.page-title {
  color: #1e40af;
  margin-bottom: 16px;
}
.n-head {
  display: flex;
  align-items: center;
  gap: 10px;
}
.bell {
  color: #f59e0b;
  font-size: 18px;
}
.n-title {
  font-weight: 600;
  font-size: 15px;
  flex: 1;
}
.n-time {
  color: var(--muted);
  font-size: 12px;
}
.n-content {
  color: #475569;
  font-size: 14px;
  margin-top: 8px;
  white-space: pre-wrap;
}
.n-publisher {
  color: var(--muted);
  font-size: 12px;
  margin-top: 6px;
  text-align: right;
}
</style>
