<script setup>
import * as echarts from 'echarts'
import { onMounted, onUnmounted, ref } from 'vue'
import { adminApi } from '../api'

const stats = ref(null)
const loading = ref(false)
const pieRef = ref(null)
const barRef = ref(null)
let charts = []

const statusNames = { pending: '待审核', available: '待租', rented: '已租', offline: '已下架' }

function renderCharts() {
  if (!stats.value) return
  const pie = echarts.init(pieRef.value)
  pie.setOption({
    title: { text: '房源状态分布', left: 'center', textStyle: { fontSize: 14, color: '#1e293b' } },
    tooltip: { trigger: 'item', formatter: '{b}: {c} 套（{d}%）' },
    color: ['#ef4444', '#10b981', '#3b82f6', '#f59e0b'],
    series: [{
      type: 'pie',
      radius: ['38%', '66%'],
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { formatter: '{b}\n{c} 套' },
      data: Object.entries(stats.value.house_status)
        .filter(([, v]) => v > 0)
        .map(([k, v]) => ({ name: statusNames[k] || k, value: v })),
    }],
  })
  charts.push(pie)

  const income = stats.value.income || []
  const bar = echarts.init(barRef.value)
  bar.setOption({
    title: { text: '租金收入趋势（已缴账单）', left: 'center', textStyle: { fontSize: 14, color: '#1e293b' } },
    tooltip: { trigger: 'axis', formatter: '{b}<br/>收入：¥{c}' },
    grid: { left: 60, right: 24, top: 48, bottom: 32 },
    xAxis: { type: 'category', data: income.map((i) => i.period) },
    yAxis: { type: 'value', name: '元' },
    series: [{
      type: 'bar',
      data: income.map((i) => i.total),
      barWidth: 34,
      itemStyle: {
        borderRadius: [6, 6, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#3b82f6' },
          { offset: 1, color: '#1e40af' },
        ]),
      },
    }],
  })
  charts.push(bar)
}

function onResize() {
  charts.forEach((c) => c.resize())
}

onMounted(async () => {
  loading.value = true
  try {
    stats.value = await adminApi.stats()
  } finally {
    loading.value = false
  }
  renderCharts()
  window.addEventListener('resize', onResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', onResize)
  charts.forEach((c) => c.dispose())
  charts = []
})

const cards = [
  { key: 'house_total', label: '房源总数', icon: 'House', color: '#2563eb', suffix: '套' },
  { key: 'user_total', label: '注册用户', icon: 'UserFilled', color: '#7c3aed', suffix: '人' },
  { key: 'contract_active', label: '履行中合同', icon: 'Tickets', color: '#059669', suffix: '份' },
  { key: 'repair_pending', label: '待处理报修', icon: 'Tools', color: '#ea580c', suffix: '单' },
]
</script>

<template>
  <div v-loading="loading">
    <div class="cards">
      <div v-for="c in cards" :key="c.key" class="stat-card hover-lift">
        <el-icon :size="30" :style="{ color: c.color }"><component :is="c.icon" /></el-icon>
        <div>
          <div class="num">{{ stats?.[c.key] ?? '-' }}<small> {{ c.suffix }}</small></div>
          <div class="label">{{ c.label }}</div>
        </div>
      </div>
    </div>

    <div class="charts">
      <div class="chart-box card-plain"><div ref="pieRef" class="chart"></div></div>
      <div class="chart-box card-plain"><div ref="barRef" class="chart"></div></div>
    </div>

    <div class="card-plain">
      <div class="card-title">运营概况</div>
      <el-descriptions :column="4" border>
        <el-descriptions-item label="待审核房源">{{ stats?.house_status?.pending ?? 0 }} 套</el-descriptions-item>
        <el-descriptions-item label="待租房源">{{ stats?.house_status?.available ?? 0 }} 套</el-descriptions-item>
        <el-descriptions-item label="租客数">{{ stats?.tenant_count ?? 0 }} 人</el-descriptions-item>
        <el-descriptions-item label="房东数">{{ stats?.landlord_count ?? 0 }} 人</el-descriptions-item>
        <el-descriptions-item label="公告数">{{ stats?.notice_count ?? 0 }} 条</el-descriptions-item>
        <el-descriptions-item label="收藏总数">{{ stats?.favorite_count ?? 0 }} 次</el-descriptions-item>
        <el-descriptions-item label="出租率">
          {{ stats?.house_total ? Math.round((stats.house_status.rented / stats.house_total) * 100) : 0 }}%
        </el-descriptions-item>
        <el-descriptions-item label="累计租金收入">
          ¥{{ (stats?.income || []).reduce((s, i) => s + i.total, 0).toFixed(2) }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </div>
</template>

<style scoped>
.cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 18px;
}
.stat-card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 20px 22px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.num {
  font-size: 26px;
  font-weight: 700;
  color: var(--text);
}
.num small {
  font-size: 13px;
  color: var(--muted);
  font-weight: 400;
}
.label {
  color: var(--muted);
  font-size: 13px;
}
.charts {
  display: grid;
  grid-template-columns: 1fr 1.4fr;
  gap: 16px;
  margin-bottom: 18px;
}
.chart {
  height: 300px;
}
@media (max-width: 900px) {
  .cards, .charts {
    grid-template-columns: 1fr;
  }
}
</style>
