<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { coverStyle, favoriteApi, houseApi } from '../api'
import { useAuth } from '../store/auth'

const router = useRouter()
const { isLoggedIn } = useAuth()

const loading = ref(false)
const houses = ref([])
const total = ref(0)
const query = reactive({
  page: 1,
  keyword: '',
  rooms: '',
  rent_min: '',
  rent_max: '',
  ordering: '-created_at',
})

async function load() {
  loading.value = true
  try {
    const data = await houseApi.list({ ...query })
    houses.value = data.results
    total.value = data.count
  } finally {
    loading.value = false
  }
}

function search() {
  query.page = 1
  load()
}

function reset() {
  Object.assign(query, { page: 1, keyword: '', rooms: '', rent_min: '', rent_max: '', ordering: '-created_at' })
  load()
}

const favSet = ref(new Set())

async function loadFavorites() {
  if (!isLoggedIn.value) return
  try {
    const data = await favoriteApi.list()
    favSet.value = new Set(data.results.map((f) => f.house))
  } catch { /* 未登录或接口异常时忽略 */ }
}

async function toggleFav(house) {
  if (!isLoggedIn.value) {
    ElMessage.warning('登录后即可收藏房源')
    router.push('/login')
    return
  }
  const data = await favoriteApi.toggle(house.id)
  if (data.favorited) favSet.value.add(house.id)
  else favSet.value.delete(house.id)
  ElMessage.success(data.favorited ? '已加入收藏' : '已取消收藏')
}

function statusTag(status) {
  return {
    available: { text: '待租', type: 'success' },
    rented: { text: '已租', type: 'info' },
    offline: { text: '已下架', type: 'warning' },
    pending: { text: '待审核', type: 'danger' },
  }[status] || { text: status, type: 'info' }
}

onMounted(() => {
  load()
  loadFavorites()
})
</script>

<template>
  <div>
    <!-- Hero 区 -->
    <section class="hero">
      <h1>找到心仪的家，从这里开始</h1>
      <p>真实房源 · 在线预约 · 电子合同 · 透明账单</p>
      <div class="hero-search">
        <el-input
          v-model="query.keyword"
          size="large"
          placeholder="搜索小区 / 地址 / 标题，如：望京"
          clearable
          @keyup.enter="search"
        >
          <template #append>
            <el-button type="primary" @click="search">
              <el-icon><Search /></el-icon>搜索
            </el-button>
          </template>
        </el-input>
      </div>
    </section>

    <div class="page-wrap">
      <!-- 筛选栏 -->
      <div class="card-plain filter-bar">
        <el-select v-model="query.rooms" placeholder="户型" clearable style="width: 130px" @change="search">
          <el-option label="一居" value="1室" />
          <el-option label="两居" value="2室" />
          <el-option label="三居及以上" value="3室" />
        </el-select>
        <el-input v-model="query.rent_min" placeholder="最低租金" style="width: 120px" @keyup.enter="search" />
        <el-input v-model="query.rent_max" placeholder="最高租金" style="width: 120px" @keyup.enter="search" />
        <el-select v-model="query.ordering" style="width: 150px" @change="search">
          <el-option label="最新发布" value="-created_at" />
          <el-option label="租金从低到高" value="rent" />
          <el-option label="租金从高到低" value="-rent" />
          <el-option label="最多浏览" value="-view_count" />
        </el-select>
        <el-button @click="reset">重置</el-button>
        <span class="result-count">共 {{ total }} 套房源</span>
      </div>

      <!-- 房源卡片 -->
      <div v-loading="loading" class="grid">
        <el-empty v-if="!loading && houses.length === 0" description="没有符合条件的房源，换个条件试试" style="grid-column: 1/-1" />
        <div
          v-for="h in houses"
          :key="h.id"
          class="house-card hover-lift"
          @click="router.push(`/houses/${h.id}`)"
        >
          <div class="cover cover-fallback" :style="coverStyle(h)">
            <span>{{ h.district }} · {{ h.rooms }}</span>
          </div>
          <div class="body">
            <div class="title-row">
              <span class="title">{{ h.title }}</span>
              <el-icon
                class="fav"
                :class="{ active: favSet.has(h.id) }"
                @click.stop="toggleFav(h)"
              >
                <StarFilled v-if="favSet.has(h.id)" />
                <Star v-else />
              </el-icon>
            </div>
            <div class="meta">
              <el-tag :type="statusTag(h.status).type" size="small">{{ statusTag(h.status).text }}</el-tag>
              <span>{{ h.rooms }}</span>
              <span>{{ h.area }}㎡</span>
              <span>{{ h.district }}</span>
            </div>
            <div class="bottom">
              <span class="price">¥{{ h.rent }}<small>/月</small></span>
              <span class="payment">{{ h.payment }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="pager" v-if="total > 0">
        <el-pagination
          v-model:current-page="query.page"
          :page-size="10"
          :total="total"
          layout="prev, pager, next"
          background
          @current-change="load"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero {
  background: linear-gradient(135deg, #1e3a8a, #2563eb 55%, #3b82f6);
  color: #fff;
  text-align: center;
  padding: 52px 24px 60px;
}
.hero h1 {
  font-size: 30px;
  font-weight: 700;
  margin-bottom: 8px;
}
.hero p {
  opacity: 0.85;
  margin-bottom: 26px;
}
.hero-search {
  max-width: 640px;
  margin: 0 auto;
}
.filter-bar {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}
.result-count {
  color: var(--muted);
  font-size: 13px;
  margin-left: auto;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 18px;
  min-height: 200px;
}
.house-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
}
.cover {
  height: 150px;
}
.body {
  padding: 14px 16px 16px;
}
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
}
.title {
  font-weight: 600;
  font-size: 15px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.fav {
  color: #cbd5e1;
  font-size: 18px;
  flex-shrink: 0;
}
.fav.active {
  color: #f59e0b;
}
.meta {
  display: flex;
  gap: 10px;
  align-items: center;
  color: var(--muted);
  font-size: 13px;
  margin: 8px 0 10px;
}
.bottom {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.price {
  color: #dc2626;
  font-size: 20px;
  font-weight: 700;
}
.price small {
  font-size: 12px;
  color: var(--muted);
  font-weight: 400;
}
.payment {
  color: var(--muted);
  font-size: 12px;
}
.pager {
  display: flex;
  justify-content: center;
  margin: 24px 0;
}
</style>
