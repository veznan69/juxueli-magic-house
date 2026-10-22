<script setup>
import { RouterView, RouterLink } from 'vue-router'
</script>

<template>
  <header class="nav">
    <div class="nav-inner">
      <RouterLink to="/" class="logo">房屋租赁管理系统</RouterLink>
      <nav class="links">
        <RouterLink to="/">首页</RouterLink>
        <a href="http://127.0.0.1:8000/admin/" target="_blank">管理后台</a>
      </nav>
    </div>
  </header>

  <main class="main">
    <RouterView />
  </main>

  <footer class="foot">基于 Python 的房屋租赁管理系统 · 本科毕业设计</footer>
</template>

<style scoped>
.nav {
  background: linear-gradient(135deg, #1e3a8a, #2563eb);
  color: #fff;
}
.nav-inner {
  max-width: 1080px;
  margin: 0 auto;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo {
  font-size: 18px;
  font-weight: 700;
  color: #fff;
  text-decoration: none;
}
.links a {
  color: rgba(255, 255, 255, 0.9);
  margin-left: 18px;
  text-decoration: none;
  font-size: 14px;
}
.links a:hover {
  color: #fff;
  text-decoration: underline;
}
.main {
  flex: 1;
  max-width: 1080px;
  width: 100%;
  margin: 0 auto;
  padding: 24px;
}
.foot {
  text-align: center;
  color: var(--muted);
  font-size: 13px;
  padding: 20px 0;
  border-top: 1px solid var(--border);
}
</style>
