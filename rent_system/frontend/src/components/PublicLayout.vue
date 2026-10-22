<script setup>
import AppHeader from './AppHeader.vue'
</script>

<template>
  <div class="public-layout">
    <AppHeader />
    <main class="public-main">
      <router-view />
    </main>
    <footer class="public-foot">
      基于 Python 的房屋租赁管理系统 · 本科毕业设计 · Django + DRF + Vue 3
    </footer>
  </div>
</template>

<style scoped>
.public-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.public-main {
  flex: 1;
}
.public-foot {
  text-align: center;
  color: var(--muted);
  font-size: 13px;
  padding: 20px 0;
  border-top: 1px solid var(--border);
  background: #fff;
}
</style>
