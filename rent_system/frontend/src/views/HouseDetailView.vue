<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { appointmentApi, coverStyle, favoriteApi, houseApi } from '../api'
import { useAuth } from '../store/auth'

const route = useRoute()
const router = useRouter()
const { isLoggedIn, role } = useAuth()

const house = ref(null)
const loading = ref(true)
const favLoading = ref(false)
const favorited = ref(false)
const submitting = ref(false)

const form = reactive({ visit_time: '', phone: '', remark: '' })

const statusMap = {
  available: { text: '待租', type: 'success' },
  rented: { text: '已租', type: 'info' },
  offline: { text: '已下架', type: 'warning' },
  pending: { text: '待审核', type: 'danger' },
}
const statusInfo = computed(() => statusMap[house.value?.status] || { text: house.value?.status, type: 'info' })

function vrDemo() {
  ElMessage.info('VR 看房功能即将上线，敬请期待')
}

async function load() {
  try {
    house.value = await houseApi.detail(route.params.id)
  } finally {
    loading.value = false
  }
}

async function checkFav() {
  if (!isLoggedIn.value || role.value !== 'tenant') return
  const data = await favoriteApi.list()
  favorited.value = data.results.some((f) => f.house === house.value?.id)
}

async function toggleFav() {
  if (!isLoggedIn.value) return router.push('/login')
  favLoading.value = true
  try {
    const data = await favoriteApi.toggle(house.value.id)
    favorited.value = data.favorited
    ElMessage.success(data.favorited ? '已加入收藏' : '已取消收藏')
  } finally {
    favLoading.value = false
  }
}

async function submitAppointment() {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { next: route.fullPath } })
    return
  }
  if (!form.visit_time || !form.phone) {
    ElMessage.warning('请填写看房时间和联系电话')
    return
  }
  submitting.value = true
  try {
    await appointmentApi.create({
      house: house.value.id,
      visit_time: form.visit_time,
      phone: form.phone,
      remark: form.remark,
    })
    ElMessage.success('预约已提交，等待房东确认')
    form.visit_time = ''
    form.remark = ''
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  load()
  checkFav()
})
</script>

<template>
  <div class="page-wrap" v-loading="loading">
    <template v-if="house">
      <el-breadcrumb style="margin-bottom: 16px">
        <el-breadcrumb-item to="/">首页</el-breadcrumb-item>
        <el-breadcrumb-item>{{ house.district }}</el-breadcrumb-item>
        <el-breadcrumb-item>房源详情</el-breadcrumb-item>
      </el-breadcrumb>

      <div class="detail-card">
        <div class="cover-big cover-fallback" :style="coverStyle(house)">
          <span style="font-size: 22px">{{ house.rooms }} · {{ house.area }}㎡</span>
          <el-button class="vr-btn" round size="small" @click="vrDemo">
            <el-icon><VideoCameraFilled /></el-icon>&nbsp;VR 看房
          </el-button>
        </div>

        <div class="info">
          <div class="head">
            <h2>{{ house.title }}</h2>
            <el-button
              :loading="favLoading"
              :type="favorited ? 'warning' : 'default'"
              circle
              @click="toggleFav"
            >
              <el-icon><StarFilled v-if="favorited" /><Star v-else /></el-icon>
            </el-button>
          </div>

          <div class="tags">
            <el-tag :type="statusInfo.type">{{ statusInfo.text }}</el-tag>
            <el-tag type="info" effect="plain">{{ house.rooms }}</el-tag>
            <el-tag type="info" effect="plain">{{ house.area }}㎡</el-tag>
            <el-tag type="info" effect="plain">{{ house.payment }}</el-tag>
            <el-tag type="info" effect="plain">{{ house.view_count }} 次浏览</el-tag>
          </div>

          <div class="price-line">
            <span class="price">¥{{ house.rent }}</span>
            <span class="per">/月</span>
            <span class="deposit">押金 ¥{{ house.deposit }}</span>
          </div>

          <el-descriptions :column="2" border style="margin-top: 14px">
            <el-descriptions-item label="所在区域">{{ house.district }}</el-descriptions-item>
            <el-descriptions-item label="详细地址">{{ house.address }}</el-descriptions-item>
            <el-descriptions-item label="出租方">{{ house.landlord_name }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ house.landlord_phone || '-' }}</el-descriptions-item>
          </el-descriptions>

          <div v-if="house.facilities?.length" class="facilities">
            <span class="sec">配套设施：</span>
            <el-tag v-for="f in house.facilities" :key="f" size="small" class="fac-tag">{{ f }}</el-tag>
          </div>

          <p v-if="house.description" class="desc">{{ house.description }}</p>
        </div>
      </div>

      <!-- 预约看房 -->
      <div class="card-plain" style="margin-top: 18px">
        <div class="card-title">预约看房</div>
        <el-form label-width="90px" style="max-width: 560px">
          <el-form-item label="看房时间" required>
            <el-date-picker
              v-model="form.visit_time"
              type="datetime"
              placeholder="选择看房日期时间"
              format="YYYY-MM-DD HH:mm"
              value-format="YYYY-MM-DDTHH:mm:ss"
              style="width: 100%"
            />
          </el-form-item>
          <el-form-item label="联系电话" required>
            <el-input v-model="form.phone" placeholder="方便房东联系你" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="form.remark" type="textarea" :rows="2" placeholder="如：想周末下午看房" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="submitting" @click="submitAppointment">
              提交预约
            </el-button>
            <span class="tip">提交后可在「我的预约」中查看房东确认结果</span>
          </el-form-item>
        </el-form>
      </div>
    </template>
  </div>
</template>

<style scoped>
.detail-card {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 14px;
  padding: 24px;
}
.cover-big {
  height: 300px;
  border-radius: 10px;
  position: relative;
}
.vr-btn {
  position: absolute;
  left: 14px;
  bottom: 14px;
  background: rgba(255, 255, 255, 0.85);
  border: none;
  color: #1e40af;
  backdrop-filter: blur(4px);
}
.vr-btn:hover {
  background: #fff;
  color: #2563eb;
}
.head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
.head h2 {
  font-size: 22px;
  color: var(--text);
}
.tags {
  display: flex;
  gap: 8px;
  margin: 10px 0;
  flex-wrap: wrap;
}
.price-line {
  display: flex;
  align-items: baseline;
  gap: 6px;
  background: #fef2f2;
  border-radius: 8px;
  padding: 10px 16px;
  width: fit-content;
}
.price {
  color: #dc2626;
  font-size: 30px;
  font-weight: 700;
}
.per {
  color: var(--muted);
}
.deposit {
  color: var(--muted);
  font-size: 13px;
  margin-left: 10px;
}
.facilities {
  margin-top: 14px;
}
.sec {
  color: var(--muted);
  font-size: 13px;
}
.fac-tag {
  margin-right: 6px;
}
.desc {
  margin-top: 14px;
  color: #475569;
  font-size: 14px;
  white-space: pre-wrap;
}
.tip {
  color: var(--muted);
  font-size: 12px;
  margin-left: 12px;
}
@media (max-width: 760px) {
  .detail-card {
    grid-template-columns: 1fr;
  }
}
</style>
