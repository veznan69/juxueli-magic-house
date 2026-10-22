<script setup>
import { ref, onMounted } from 'vue'
import request from '../api/request'

const health = ref(null)
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    health.value = await request.get('/health/')
  } catch (e) {
    error.value = '无法连接后端服务，请确认 Django 已启动（8000 端口）'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="home">
    <section class="hero">
      <h1>基于 Python 的房屋租赁管理系统</h1>
      <p>B/S 架构 · Django + DRF + Vue 3 前后端分离 · 本科毕业设计</p>
    </section>

    <section class="card">
      <h2>系统状态</h2>
      <p v-if="loading">正在连接后端…</p>
      <p v-else-if="error" class="err">{{ error }}</p>
      <div v-else class="ok">
        <span class="dot"></span>
        后端连接正常 · {{ health?.service }} · 版本 {{ health?.version }}
      </div>
    </section>

    <section class="card">
      <h2>项目进度（骨架期）</h2>
      <ol class="steps">
        <li class="done">① 项目骨架：Django + DRF + Vue 3 一键启动</li>
        <li>② 数据库模型与 Admin 后台（user / lessor / house 等 11 张表）</li>
        <li>③ 核心业务：房源、预约、合同、账单、报修</li>
        <li>④ 加分项：Redis 缓存、ECharts 统计、合同 PDF</li>
      </ol>
    </section>
  </div>
</template>

<style scoped>
.hero {
  background: linear-gradient(135deg, #1e3a8a, #2563eb);
  color: #fff;
  border-radius: 14px;
  padding: 40px 32px;
  margin-bottom: 20px;
}
.hero h1 {
  font-size: 26px;
  margin-bottom: 8px;
}
.hero p {
  font-size: 14px;
  opacity: 0.9;
}
.card {
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 22px 26px;
  margin-bottom: 16px;
}
.card h2 {
  font-size: 17px;
  margin-bottom: 12px;
  color: var(--primary-dark);
}
.ok {
  color: #065f46;
  display: flex;
  align-items: center;
  gap: 8px;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #10b981;
  display: inline-block;
}
.err {
  color: #b91c1c;
}
.steps {
  padding-left: 20px;
  font-size: 14px;
}
.steps li {
  margin-bottom: 6px;
  color: var(--muted);
}
.steps li.done {
  color: #065f46;
  font-weight: 600;
}
</style>
