# 基于 Python 的房屋租赁管理系统

本科毕业设计项目 · B/S 架构 · **Django + DRF + Vue 3 前后端分离**

> 本文档对应《毕设系统规划.html》定稿方案，当前为**阶段①：项目骨架**。

---

## 一、环境准备（一次性）

| 依赖 | 状态 | 说明 |
|------|------|------|
| Python 3.11 | ✅ 已就绪 | 本机预装，脚本会自动创建 venv 虚拟环境 |
| Redis 8.10.2 | ✅ 已安装 | 便携版位于 `../redis/`，端口 6379（可选，不启动系统也能跑） |
| Node.js v24.22.0 | ⏳ **待安装** | 双击上级目录的 `node-v24.22.0-x64-installer.msi`，一路下一步 |

安装 Node.js 后，首次运行前端前执行一次：

```bash
cd frontend
npm install
```

---

## 二、一键启动（日常使用）

双击项目根目录的 **`start.bat`**，自动完成：

1. **后台分离启动 Redis**（端口 6379，不会阻塞窗口）
2. 创建 / 检查 venv 并安装依赖
3. 数据库迁移（SQLite，零配置）
4. 启动 Django（8000）与 Vue 开发服务器（5173）并自动打开浏览器

| 地址 | 用途 |
|------|------|
| http://127.0.0.1:5173/ | 前端首页（Vue 开发服务器） |
| http://127.0.0.1:8000/admin/ | Django Admin 管理后台（账号 `admin` / 密码 `admin123456`） |

**演示账号**（`python manage.py seed_demo` 一键灌入）：

| 角色 | 账号 | 密码 |
|------|------|------|
| 管理员 | admin | admin123456 |
| 房东 | landlord | landlord123 |
| 租客 | tenant1 / tenant2 | tenant123 |
| http://127.0.0.1:8000/api/health/ | 后端健康检查接口 |

---

## 三、目录结构

```
rent_system/
├── manage.py               # Django 入口
├── requirements.txt        # 后端依赖
├── start.bat               # 一键启动脚本
├── db.sqlite3              # SQLite 开发库（自动生成）
├── rent_system/            # 项目配置包
│   ├── settings.py         #   SQLite/MySQL 切换、CORS、DRF、中文化、Redis 预留
│   ├── urls.py             #   /admin/ + /api/health/
│   ├── views.py            #   健康检查与 API 根视图
│   └── wsgi.py / asgi.py   #   部署入口
├── apps/                   # 业务应用（阶段②填充模型，按 11 张核心表规划）
│   ├── users/              #   用户账号（登录主体）
│   ├── lessor/             #   出租方（房东主体，与 user 解耦）
│   ├── house/              #   房源
│   ├── appointment/        #   预约看房
│   ├── contract/           #   租赁合同
│   ├── bill/               #   租金账单
│   ├── repair/             #   报修工单
│   ├── favorite/           #   收藏
│   └── notice/             #   公告
└── frontend/               # Vue 3 前端
    ├── package.json        #   依赖清单（vue3 / router / axios / echarts）
    ├── vite.config.js      #   5173 端口 + /api 代理到 8000
    └── src/
        ├── main.js / App.vue / style.css
        ├── router/index.js     # 路由表
        ├── api/request.js      # axios 封装（baseURL=/api，统一错误处理）
        └── views/HomeView.vue  # 首页（调用健康接口展示连通状态）
```

---

## 四、关键设计（论文可直接引用）

1. **架构**：前后端分离。Vue 3 负责视图层，Django + DRF 提供 RESTful API，JSON 交互。
2. **数据库切换**：开发期 SQLite 零配置；部署期取消 `settings.py` 中 `DATABASES` 注释块即可切换 MySQL 8（论文表述：开发期 SQLite、部署期 MySQL）。
3. **出租方建模**：`user`（登录账号）与 `lessor`（出租主体）解耦——个人房东 1 对 1，公司房东多账号共用 1 个 lessor。
4. **Redis 预留**：缓存 / 登录态接入点已在 `settings.py` 预留注释（`CACHES` + `SESSION_ENGINE`），高并发场景可无缝启用。
5. **部署**：演示期 `npm run build` 产出 `frontend/dist`，交由 Django 托管，花生壳映射 8000 端口即可外网访问。

---

## 五、常用命令备忘

```bash
# 后端（在项目根目录）
venv\Scripts\activate                 # 激活虚拟环境
python manage.py runserver 8000       # 启动后端
python manage.py makemigrations       # 生成迁移（阶段②建模型后用）
python manage.py migrate              # 应用迁移
python manage.py createsuperuser      # 新建管理员

# 前端（在 frontend 目录）
npm install        # 首次安装依赖
npm run dev        # 开发服务器 5173
npm run build      # 产出 dist（演示部署用）
```

---

## 六、同步到 GitHub（本机专用备忘）

- 仓库：https://github.com/veznan69/juxueli-magic-house （公开，描述：橘雪梨的神秘妙妙屋）
- git 使用绿色版：`../portable-git/cmd/git.exe`（未安装全局 git）
- 学校网络会拦截 schannel 证书吊销检查，推送需临时关闭 SSL 校验：

```bash
# 1. 每次推送前，把远程地址临时带上 PAT（PAT 在 github.com/settings/tokens 生成，勾选 repo）
git remote set-url origin https://<你的PAT>@github.com/veznan69/juxueli-magic-house.git
# 2. 推送
git -c http.sslVerify=false push -u origin main
# 3. 推完立刻清掉 token
git remote set-url origin https://github.com/veznan69/juxueli-magic-house.git
```

- `.gitignore` 已排除：venv、node_modules、db.sqlite3、redis/ 二进制、*.msi/*.zip/*.exe 安装包、IDE 数据文件

---

## 六、开发路线图

- [x] **① 项目骨架**：Django + DRF + Vue 3 一键启动
- [x] **② 数据库模型与 Admin**：9 张业务表 + 自定义 User（role 字段），house 外键关联 lessor（出租方与登录账号解耦）
- [x] **③ 全角色 API 与页面**：18 个页面（租客端/房东端/管理后台）+ `/api/v1/` 全套接口 + seed_demo 演示数据
- [x] 管理后台 ECharts 统计看板（房源状态饼图、租金收入柱状图）
- [ ] ④ 加分项：Redis 缓存接入、合同 PDF、花生壳外网演示

## 七、API 一览（/api/v1/）

| 模块 | 端点 |
|------|------|
| 认证 | `POST auth/register/` `POST auth/login/` `GET/PATCH auth/me/`（Token 认证） |
| 房源 | `GET/POST houses/` `GET houses/{id}/` `GET houses/mine/` `POST houses/{id}/set-status/` `POST houses/{id}/review/`（管理员）；筛选参数：keyword/district/rooms/rent_min/rent_max/ordering |
| 预约 | `GET/POST appointments/`（租客）`GET landlord/appointments/` + `POST {id}/handle/`（房东） |
| 合同 | `GET contracts/`（按角色自动过滤） |
| 账单 | `GET bills/?status=` `POST bills/{id}/pay/` |
| 报修 | `GET/POST repairs/`（租客）`GET landlord/repairs/` + `POST {id}/handle/`（房东） |
| 收藏 | `GET favorites/` `POST favorites/toggle/` |
| 公告 | `GET notices/`（公开）`POST/DELETE`（管理员） |
| 管理 | `GET admin-users/` + `POST {id}/set-active/ set-role/`；`GET admin-houses/`；`GET stats/` |

## 八、页面清单（frontend/src/views/）

- **公共**：首页房源列表（搜索/筛选/排序/收藏）、房源详情（预约看房）、登录、注册、公告列表
- **租客端**：个人中心、我的收藏、我的预约、我的合同、我的账单（在线缴费）、我的报修
- **房东端**：房源管理（发布/编辑/上下架）、预约处理、报修处理
- **管理后台**：数据看板（ECharts）、房源审核、用户管理、公告管理
