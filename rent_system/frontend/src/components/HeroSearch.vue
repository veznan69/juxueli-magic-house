<script setup>
/**
 * HeroSearch：首页主搜索框 + 热门搜索标签
 * 用法：<HeroSearch v-model="keyword" :hot-tags="['两居','整租']" @search="onSearch" @hot-tag="onHotTag" />
 */
defineProps({
  // 搜索关键字（支持 v-model）
  modelValue: { type: String, default: '' },
  // 热门标签列表
  hotTags: { type: Array, default: () => [] },
  // 占位提示
  placeholder: { type: String, default: '搜索小区 / 地址 / 标题，如：望京' },
})

const emit = defineEmits(['update:modelValue', 'search', 'hot-tag'])
</script>

<template>
  <div class="hero-search">
    <el-input
      :model-value="modelValue"
      :placeholder="placeholder"
      size="large"
      clearable
      @update:model-value="emit('update:modelValue', $event)"
      @keyup.enter="emit('search')"
    >
      <template #append>
        <el-button type="primary" @click="emit('search')">
          <el-icon><Search /></el-icon>搜索
        </el-button>
      </template>
    </el-input>
    <div v-if="hotTags.length" class="hot-tags">
      <span class="hot-label">热门搜索：</span>
      <span
        v-for="t in hotTags"
        :key="t"
        class="hot-tag"
        @click="emit('hot-tag', t)"
      >{{ t }}</span>
    </div>
  </div>
</template>

<style scoped>
.hero-search {
  max-width: 640px;
  margin: 0 auto;
}
.hot-tags {
  margin-top: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.hot-label {
  font-size: 13px;
  opacity: 0.75;
}
.hot-tag {
  font-size: 13px;
  padding: 3px 14px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.2s;
}
.hot-tag:hover {
  background: rgba(255, 255, 255, 0.28);
  transform: translateY(-1px);
}
</style>
