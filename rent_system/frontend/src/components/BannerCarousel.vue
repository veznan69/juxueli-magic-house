<script setup>
/**
 * BannerCarousel：运营位轮播图
 * 用法：<BannerCarousel :banners="banners" @select="onBanner" />
 * banners 项字段：{ id, tag, title, sub, btn, bg, ...自定义字段 }，点击时整对象通过 select 事件抛出
 */
defineProps({
  banners: { type: Array, default: () => [] },
  // 轮播高度
  height: { type: String, default: '230px' },
  // 自动切换间隔（毫秒）
  interval: { type: Number, default: 4000 },
})

const emit = defineEmits(['select'])
</script>

<template>
  <div v-if="banners.length" class="banner">
    <el-carousel :height="height" :interval="interval" arrow="hover">
      <el-carousel-item v-for="b in banners" :key="b.id">
        <div class="banner-slide" :style="{ background: b.bg }" @click="emit('select', b)">
          <span class="b-tag">{{ b.tag }}</span>
          <h3 class="b-title">{{ b.title }}</h3>
          <p class="b-sub">{{ b.sub }}</p>
          <el-button round class="b-btn">{{ b.btn }}</el-button>
        </div>
      </el-carousel-item>
    </el-carousel>
  </div>
</template>

<style scoped>
.banner {
  margin-bottom: 18px;
  border-radius: 14px;
  overflow: hidden;
}
.banner-slide {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 0 64px;
  color: #fff;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.banner-slide::before {
  content: '';
  position: absolute;
  right: -60px;
  top: -70px;
  width: 240px;
  height: 240px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.12);
}
.banner-slide::after {
  content: '';
  position: absolute;
  right: 90px;
  bottom: -90px;
  width: 180px;
  height: 180px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.09);
}
.b-tag {
  font-size: 12px;
  letter-spacing: 2px;
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.4);
  padding: 2px 12px;
  border-radius: 999px;
  margin-bottom: 12px;
}
.b-title {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 6px;
}
.b-sub {
  font-size: 14px;
  opacity: 0.88;
  margin-bottom: 16px;
}
.b-btn {
  background: #fff;
  color: #1e40af;
  border: none;
  font-weight: 600;
}
.b-btn:hover {
  background: #f1f5f9;
  color: #2563eb;
}
</style>
