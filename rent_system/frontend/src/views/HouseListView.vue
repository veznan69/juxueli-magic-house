<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { coverStyle, favoriteApi, houseApi } from '../api'
import { useAuth } from '../store/auth'
import BannerCarousel from '../components/BannerCarousel.vue'
import HeroSearch from '../components/HeroSearch.vue'

const router = useRouter()
const { isLoggedIn } = useAuth()

const loading = ref(false)
const houses = ref([])
const total = ref(0)
const heroTotal = ref(0)          // 全站在租统计（不带筛选）
const recommended = ref([])       // 猜你喜欢（按浏览量）
const customRent = ref(false)     // 自定义租金区间展开
const customMin = ref('')
const customMax = ref('')

const query = reactive({
  page: 1,
  keyword: '',
  district: '',
  rooms: '',
  rent_min: '',
  rent_max: '',
  ordering: '-created_at',
})

// 筛选选项（与演示数据区域匹配；租金区间为安居客式快捷档位）
const DISTRICTS = ['朝阳区', '海淀区', '丰台区', '西城区']
const HOT_TAGS = ['两居', '一居室', '整租', '独立卫浴', '望京']
const RENT_PRESETS = [
  { label: '1000以下', min: '', max: '999' },
  { label: '1000-2000', min: '1000', max: '2000' },
  { label: '2000-3000', min: '2000', max: '3000' },
  { label: '3000-5000', min: '3000', max: '5000' },
  { label: '5000以上', min: '5000', max: '' },
]
const ROOMS = [
  { label: '一居', value: '1室' },
  { label: '两居', value: '2室' },
  { label: '三居及以上', value: '3室' },
]
const ORDERINGS = [
  { label: '最新发布', value: '-created_at' },
  { label: '租金低到高', value: 'rent' },
  { label: '租金高到低', value: '-rent' },
  { label: '最多浏览', value: '-view_count' },
]

// 首页运营轮播图（点击联动筛选或跳转公告页）
const banners = [
  { id: 1, tag: '平台精选', title: '好房上新 · 实拍审核', sub: '管理员逐套审核，拒绝虚假房源', btn: '浏览全部房源',
    bg: 'linear-gradient(120deg, #1e3a8a, #2563eb 55%, #38bdf8)',
    action: () => { reset(); scrollToList() } },
  { id: 2, tag: '品质两居', title: '精装两居 · 拎包入住', sub: '家电齐全 · 押一付三 · 随时看房', btn: '查看两居',
    bg: 'linear-gradient(120deg, #1e40af, #7c3aed)',
    action: () => { hotTag('两居'); scrollToList() } },
  { id: 3, tag: '毕业季', title: '毕业生租房一站式指南', sub: '低预算一居室 · 押一付一 · 交通便利', btn: '逛逛一居室',
    bg: 'linear-gradient(120deg, #0f766e, #059669 60%, #34d399)',
    action: () => { hotTag('一居室'); scrollToList() } },
  { id: 4, tag: '租得安心', title: '在线预约 · 电子合同 · 透明账单', sub: '看房、签约、缴费、报修全流程线上办理', btn: '了解平台',
    bg: 'linear-gradient(120deg, #9d174d, #db2777 60%, #f472b6)',
    action: () => router.push('/notices') },
]

const activeRentIdx = computed(() =>
  RENT_PRESETS.findIndex((p) => p.min === query.rent_min && p.max === query.rent_max))
const noRentFilter = computed(() => query.rent_min === '' && query.rent_max === '')

function buildParams() {
  const p = { page: query.page, ordering: query.ordering }
  if (query.keyword) p.keyword = query.keyword
  if (query.district) p.district = query.district
  if (query.rooms) p.rooms = query.rooms
  if (query.rent_min) p.rent_min = query.rent_min
  if (query.rent_max) p.rent_max = query.rent_max
  return p
}

async function load() {
  loading.value = true
  try {
    const data = await houseApi.list(buildParams())
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

function setDistrict(d) { query.district = d; search() }
function setRooms(v) { query.rooms = v; search() }
function setOrdering(v) { query.ordering = v; search() }
function setRent(p) {
  query.rent_min = p.min
  query.rent_max = p.max
  customRent.value = false
  search()
}
function applyCustom() {
  query.rent_min = customMin.value
  query.rent_max = customMax.value
  customRent.value = false
  search()
}
function hotTag(t) { query.keyword = t; search() }
function mapSearch() { ElMessage.info('地图找房功能即将上线，敬请期待') }

function scrollToList() {
  document.querySelector('.filter-card')?.scrollIntoView({ behavior: 'smooth' })
}
function onBanner(b) { b.action() }

function reset() {
  Object.assign(query, { page: 1, keyword: '', district: '', rooms: '', rent_min: '', rent_max: '', ordering: '-created_at' })
  customRent.value = false
  customMin.value = ''
  customMax.value = ''
  load()
}

// 猜你喜欢 + 全站统计：各发一次列表请求（现有接口，零后端改动）
async function loadExtras() {
  try {
    const [all, hot] = await Promise.all([
      houseApi.list({ page: 1 }),
      houseApi.list({ ordering: '-view_count', page: 1 }),
    ])
    heroTotal.value = all.count
    recommended.value = hot.results.slice(0, 4)
  } catch { /* 统计与推荐加载失败不影响主列表 */ }
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
    available: { text: '待租' },
    rented: { text: '已租' },
    offline: { text: '已下架' },
    pending: { text: '待审核' },
  }[status] || { text: status }
}

onMounted(() => {
  load()
  loadExtras()
  loadFavorites()
})
</script>

<template>
  <div>
    <!-- Hero 区：标题 + 统计 + 搜索 + 热门标签 -->
    <section class="hero">
      <h1>找到心仪的家，从这里开始</h1>
      <p>当前在租房源 <b>{{ heroTotal }}</b> 套 · 在线预约看房 · 电子合同 · 透明账单</p>
      <HeroSearch
        v-model="query.keyword"
        :hot-tags="HOT_TAGS"
        @search="search"
        @hot-tag="hotTag"
      />
    </section>

    <div class="page-wrap">
      <!-- 运营轮播图 -->
      <BannerCarousel :banners="banners" @select="onBanner" />

      <!-- 安居客式分行筛选条 -->
      <div class="card-plain filter-card">
        <div class="f-row">
          <span class="f-label">位置</span>
          <div class="f-chips">
            <span class="f-chip" :class="{ active: query.district === '' }" @click="setDistrict('')">不限</span>
            <span v-for="d in DISTRICTS" :key="d" class="f-chip"
                  :class="{ active: query.district === d }" @click="setDistrict(d)">{{ d }}</span>
          </div>
        </div>
        <div class="f-row">
          <span class="f-label">租金</span>
          <div class="f-chips">
            <span class="f-chip" :class="{ active: noRentFilter && !customRent }" @click="setRent({ min: '', max: '' })">不限</span>
            <span v-for="(p, i) in RENT_PRESETS" :key="p.label" class="f-chip"
                  :class="{ active: activeRentIdx === i }" @click="setRent(p)">{{ p.label }}</span>
            <span class="f-chip" :class="{ active: customRent }" @click="customRent = !customRent">自定义</span>
            <template v-if="customRent">
              <el-input v-model="customMin" placeholder="最低" size="small" style="width: 86px" />
              <span class="f-sep">—</span>
              <el-input v-model="customMax" placeholder="最高" size="small" style="width: 86px" />
              <el-button type="primary" size="small" @click="applyCustom">确定</el-button>
            </template>
          </div>
        </div>
        <div class="f-row">
          <span class="f-label">户型</span>
          <div class="f-chips">
            <span class="f-chip" :class="{ active: query.rooms === '' }" @click="setRooms('')">不限</span>
            <span v-for="r in ROOMS" :key="r.value" class="f-chip"
                  :class="{ active: query.rooms === r.value }" @click="setRooms(r.value)">{{ r.label }}</span>
          </div>
        </div>
        <div class="f-row">
          <span class="f-label">排序</span>
          <div class="f-chips">
            <span v-for="o in ORDERINGS" :key="o.value" class="f-chip"
                  :class="{ active: query.ordering === o.value }" @click="setOrdering(o.value)">{{ o.label }}</span>
            <span class="f-right">
              <el-button size="small" plain @click="mapSearch">
                <el-icon><Location /></el-icon>&nbsp;地图找房
              </el-button>
              <el-button text size="small" @click="reset">重置</el-button>
              <span class="result-count">共 {{ total }} 套房源</span>
            </span>
          </div>
        </div>
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
            <span class="cover-text">{{ h.district }} · {{ h.rooms }}</span>
            <span class="status-badge" :class="`st-${h.status}`">{{ statusTag(h.status).text }}</span>
          </div>
          <div class="body">
            <div class="title-row">
              <span class="title">{{ h.title }}</span>
              <el-icon class="fav" :class="{ active: favSet.has(h.id) }" @click.stop="toggleFav(h)">
                <StarFilled v-if="favSet.has(h.id)" />
                <Star v-else />
              </el-icon>
            </div>
            <div class="fac-row">
              <span v-for="f in (h.facilities || []).slice(0, 3)" :key="f" class="fac-tag">{{ f }}</span>
              <span v-if="!(h.facilities || []).length" class="fac-empty">{{ h.address }}</span>
            </div>
            <div class="meta">
              <span>{{ h.rooms }}</span><span class="dot">|</span>
              <span>{{ h.area }}㎡</span><span class="dot">|</span>
              <span>{{ h.district }}</span><span class="dot">|</span>
              <span>{{ h.payment }}</span>
            </div>
            <div class="bottom">
              <span class="price">¥{{ h.rent }}<small>/月</small></span>
              <span class="views">{{ h.view_count }} 人浏览</span>
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

      <!-- 猜你喜欢：热门推荐位 -->
      <div class="rec-section" v-if="recommended.length">
        <div class="rec-head">
          <span class="rec-title">猜你喜欢 · 热门房源</span>
          <span class="rec-sub">按浏览量为你推荐</span>
        </div>
        <div class="rec-grid">
          <div v-for="h in recommended" :key="h.id" class="rec-card hover-lift"
               @click="router.push(`/houses/${h.id}`)">
            <div class="rec-cover cover-fallback" :style="coverStyle(h)">
              <span>{{ h.rooms }}</span>
            </div>
            <div class="rec-body">
              <div class="rec-title">{{ h.title }}</div>
              <div class="rec-meta">{{ h.rooms }} · {{ h.area }}㎡ · {{ h.district }}</div>
              <div class="rec-bottom">
                <span class="price">¥{{ h.rent }}<small>/月</small></span>
                <span class="views">{{ h.view_count }} 浏览</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.hero {
  background: linear-gradient(135deg, #1e3a8a, #2563eb 55%, #3b82f6);
  color: #fff;
  text-align: center;
  padding: 48px 24px 54px;
}
.hero h1 {
  font-size: 30px;
  font-weight: 700;
  margin-bottom: 8px;
}
.hero p {
  opacity: 0.85;
  margin-bottom: 24px;
}
.hero p b {
  color: #fbbf24;
  font-size: 18px;
  padding: 0 2px;
}
/* 分行筛选条 */
.filter-card {
  padding: 10px 22px 4px;
}
.f-row {
  display: flex;
  align-items: flex-start;
  min-height: 44px;
  padding: 6px 0;
  border-bottom: 1px dashed var(--border);
}
.f-row:last-child {
  border-bottom: none;
}
.f-label {
  width: 52px;
  flex-shrink: 0;
  color: var(--muted);
  font-size: 13px;
  line-height: 28px;
}
.f-chips {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
  flex: 1;
}
.f-chip {
  font-size: 13px;
  color: var(--text);
  padding: 3px 14px;
  border-radius: 999px;
  cursor: pointer;
  transition: all 0.15s;
  line-height: 22px;
}
.f-chip:hover {
  color: var(--el-color-primary);
  background: var(--el-color-primary-light-9);
}
.f-chip.active {
  background: var(--el-color-primary);
  color: #fff;
  font-weight: 500;
}
.f-sep {
  color: var(--muted);
  margin: 0 2px;
}
.f-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
}
.result-count {
  color: var(--muted);
  font-size: 13px;
  margin-left: 6px;
}

/* 房源卡片 */
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
  position: relative;
}
.cover-text {
  font-size: 15px;
  letter-spacing: 2px;
}
.status-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 999px;
  color: #fff;
}
.st-available { background: rgba(16, 185, 129, 0.92); }
.st-rented { background: rgba(100, 116, 139, 0.9); }
.st-offline { background: rgba(245, 158, 11, 0.92); }
.st-pending { background: rgba(239, 68, 68, 0.92); }
.body {
  padding: 13px 15px 15px;
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
.fac-row {
  display: flex;
  gap: 6px;
  margin: 8px 0 9px;
  min-height: 22px;
  overflow: hidden;
}
.fac-tag {
  font-size: 12px;
  color: var(--el-color-primary-dark);
  background: var(--el-color-primary-light-9);
  border: 1px solid var(--el-color-primary-light-8);
  padding: 1px 8px;
  border-radius: 4px;
  white-space: nowrap;
}
.fac-empty {
  font-size: 12px;
  color: var(--muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.meta {
  display: flex;
  gap: 8px;
  align-items: center;
  color: var(--muted);
  font-size: 13px;
  margin-bottom: 10px;
}
.dot {
  color: var(--border);
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
.views {
  color: var(--muted);
  font-size: 12px;
}
.pager {
  display: flex;
  justify-content: center;
  margin: 24px 0;
}

/* 猜你喜欢 */
.rec-section {
  margin-top: 30px;
}
.rec-head {
  display: flex;
  align-items: baseline;
  gap: 12px;
  margin-bottom: 14px;
}
.rec-title {
  font-size: 18px;
  font-weight: 700;
  color: #1e40af;
}
.rec-sub {
  color: var(--muted);
  font-size: 13px;
}
.rec-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}
.rec-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  overflow: hidden;
  cursor: pointer;
}
.rec-cover {
  height: 110px;
}
.rec-cover span {
  font-size: 13px;
  letter-spacing: 2px;
}
.rec-body {
  padding: 11px 13px 13px;
}
.rec-title {
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.rec-meta {
  color: var(--muted);
  font-size: 12px;
  margin: 5px 0 8px;
}
.rec-bottom {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.rec-bottom .price {
  font-size: 17px;
}
@media (max-width: 860px) {
  .rec-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .f-label {
    width: 100%;
  }
  .f-row {
    flex-direction: column;
    gap: 6px;
  }
  .f-right {
    margin-left: 0;
  }
}
</style>
