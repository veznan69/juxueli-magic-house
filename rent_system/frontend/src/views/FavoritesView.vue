<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { coverStyle, favoriteApi } from '../api'

const router = useRouter()
const favorites = ref([])
const loading = ref(false)

const statusMap = {
  available: { text: '待租', type: 'success' },
  rented: { text: '已租', type: 'info' },
  offline: { text: '已下架', type: 'warning' },
  pending: { text: '待审核', type: 'danger' },
}

async function load() {
  loading.value = true
  try {
    const data = await favoriteApi.list()
    favorites.value = data.results
  } finally {
    loading.value = false
  }
}

async function unfav(f) {
  await favoriteApi.toggle(f.house)
  ElMessage.success('已取消收藏')
  load()
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <el-empty v-if="!loading && favorites.length === 0" description="还没有收藏房源，去首页逛逛吧">
      <el-button type="primary" @click="router.push('/')">去找房</el-button>
    </el-empty>

    <div class="card-plain hover-lift" v-for="f in favorites" :key="f.id">
      <div class="row">
        <div class="mini-cover cover-fallback" :style="coverStyle({ id: f.house, cover: '' })">
          {{ f.house_rooms }}
        </div>
        <div class="info">
          <div class="t">{{ f.house_title }}</div>
          <div class="m">
            <el-tag :type="statusMap[f.house_status]?.type || 'info'" size="small">
              {{ statusMap[f.house_status]?.text || f.house_status }}
            </el-tag>
            <span>{{ f.house_rooms }}</span>
            <span>{{ f.house_district }}</span>
            <span class="time">收藏于 {{ (f.created_at || '').slice(0, 10) }}</span>
          </div>
        </div>
        <div class="ops">
          <span class="price">¥{{ f.house_rent }}<small>/月</small></span>
          <el-button size="small" type="primary" plain @click="router.push(`/houses/${f.house}`)">
            查看详情
          </el-button>
          <el-button size="small" @click="unfav(f)">取消收藏</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  align-items: center;
  gap: 16px;
}
.mini-cover {
  width: 96px;
  height: 68px;
  border-radius: 8px;
  font-size: 12px;
  flex-shrink: 0;
}
.info {
  flex: 1;
  min-width: 0;
}
.t {
  font-weight: 600;
  margin-bottom: 6px;
}
.m {
  display: flex;
  gap: 12px;
  align-items: center;
  color: var(--muted);
  font-size: 13px;
}
.time {
  margin-left: auto;
}
.ops {
  display: flex;
  align-items: center;
  gap: 10px;
}
.price {
  color: #dc2626;
  font-weight: 700;
  font-size: 18px;
  margin-right: 6px;
}
.price small {
  font-size: 12px;
  color: var(--muted);
  font-weight: 400;
}
</style>
