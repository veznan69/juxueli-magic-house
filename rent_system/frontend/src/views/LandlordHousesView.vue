<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { houseApi } from '../api'

const list = ref([])
const total = ref(0)
const loading = ref(false)
const dialogVisible = ref(false)
const editingId = ref(null)
const submitting = ref(false)

const emptyForm = {
  title: '', district: '', address: '', rooms: '1室1厅', area: 50,
  rent: 3000, deposit: 3000, payment: '押一付三',
  facilities: 'WiFi,空调,洗衣机,冰箱', description: '',
}
const form = reactive({ ...emptyForm })

const statusMap = {
  pending: { text: '待审核', type: 'danger' },
  available: { text: '待租', type: 'success' },
  rented: { text: '已租', type: 'info' },
  offline: { text: '已下架', type: 'warning' },
}

async function load() {
  loading.value = true
  try {
    const data = await houseApi.mine()
    list.value = data.results
    total.value = data.count
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  Object.assign(form, emptyForm)
  dialogVisible.value = true
}

function openEdit(row) {
  editingId.value = row.id
  Object.assign(form, {
    title: row.title, district: row.district, address: row.address,
    rooms: row.rooms, area: row.area, rent: row.rent, deposit: row.deposit,
    payment: row.payment, facilities: row.facilities || '', description: row.description || '',
  })
  dialogVisible.value = true
}

async function submit() {
  if (!form.title || !form.district || !form.address) {
    ElMessage.warning('请填写标题、区域与地址')
    return
  }
  submitting.value = true
  try {
    if (editingId.value) {
      await houseApi.update(editingId.value, { ...form })
      ElMessage.success('房源已更新')
    } else {
      await houseApi.create({ ...form })
      ElMessage.success('房源已提交，等待管理员审核')
    }
    dialogVisible.value = false
    load()
  } finally {
    submitting.value = false
  }
}

async function toggleStatus(row) {
  const target = row.status === 'available' ? 'offline' : 'available'
  await houseApi.setStatus(row.id, target)
  ElMessage.success(target === 'offline' ? '已下架' : '已上架')
  load()
}

async function remove(row) {
  await ElMessageBox.confirm(`确定删除房源「${row.title}」吗？删除后不可恢复`, '删除房源', { type: 'warning' })
  await houseApi.remove(row.id)
  ElMessage.success('已删除')
  load()
}

onMounted(load)
</script>

<template>
  <div v-loading="loading">
    <div style="margin-bottom: 14px; display: flex; justify-content: space-between">
      <el-alert type="info" :closable="false" style="flex: 1; margin-right: 16px"
                title="新发布房源需管理员审核通过后才会公开展示" />
      <el-button type="primary" @click="openCreate">
        <el-icon><Plus /></el-icon>发布房源
      </el-button>
    </div>

    <el-table :data="list" stripe>
      <el-table-column prop="title" label="标题" min-width="180" show-overflow-tooltip />
      <el-table-column prop="district" label="区域" width="90" />
      <el-table-column prop="rooms" label="户型" width="90" />
      <el-table-column prop="area" label="面积㎡" width="80" />
      <el-table-column label="月租" width="90">
        <template #default="{ row }">¥{{ row.rent }}</template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="statusMap[row.status]?.type" size="small">
            {{ statusMap[row.status]?.text || row.status }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="浏览" width="70" />
      <el-table-column label="操作" width="220" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="openEdit(row)">编辑</el-button>
          <el-button v-if="['available', 'offline'].includes(row.status)" size="small"
                     :type="row.status === 'available' ? 'warning' : 'success'" plain
                     @click="toggleStatus(row)">
            {{ row.status === 'available' ? '下架' : '上架' }}
          </el-button>
          <el-button size="small" type="danger" plain @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑房源' : '发布房源'" width="560px">
      <el-form label-width="90px">
        <el-form-item label="标题" required>
          <el-input v-model="form.title" placeholder="如：精装两居 拎包入住" />
        </el-form-item>
        <el-form-item label="区域" required>
          <el-input v-model="form.district" placeholder="如：朝阳区" style="width: 200px" />
        </el-form-item>
        <el-form-item label="详细地址" required>
          <el-input v-model="form.address" placeholder="小区 / 楼栋 / 门牌号" />
        </el-form-item>
        <el-form-item label="户型">
          <el-select v-model="form.rooms" style="width: 140px">
            <el-option v-for="r in ['1室0厅', '1室1厅', '2室1厅', '2室2厅', '3室2厅', '4室2厅']"
                       :key="r" :value="r" :label="r" />
          </el-select>
        </el-form-item>
        <el-form-item label="面积 / 租金">
          <el-input-number v-model="form.area" :min="10" :max="500" /> ㎡
          <el-input-number v-model="form.rent" :min="100" :max="50000" :step="100" style="margin-left: 12px" /> 元/月
        </el-form-item>
        <el-form-item label="押金 / 押付">
          <el-input-number v-model="form.deposit" :min="0" :max="50000" :step="100" /> 元
          <el-select v-model="form.payment" style="width: 130px; margin-left: 12px">
            <el-option v-for="p in ['押一付一', '押一付三', '押二付一', '半年付']" :key="p" :value="p" :label="p" />
          </el-select>
        </el-form-item>
        <el-form-item label="配套设施">
          <el-input v-model="form.facilities" placeholder="逗号分隔：WiFi,空调,洗衣机" />
        </el-form-item>
        <el-form-item label="房源描述">
          <el-input v-model="form.description" type="textarea" :rows="3"
                    placeholder="介绍房屋亮点、周边配套、交通情况等" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="submitting" @click="submit">
          {{ editingId ? '保存修改' : '提交发布' }}
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>
