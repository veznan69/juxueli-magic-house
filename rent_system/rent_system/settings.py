"""
Django settings for rent_system project.

基于 Python 的房屋租赁管理系统 —— 后端配置
- 开发期使用 SQLite（零配置启动）
- 部署期可切换 MySQL 8（见 DATABASES 下方注释）
- 预留 Redis 缓存 / 登录态接入（见 CACHES 注释）
"""

from pathlib import Path

# 项目根目录：bishe/rent_system/
BASE_DIR = Path(__file__).resolve().parent.parent

# 安全警告：仅开发期使用。生产环境请改用环境变量注入并妥善保管。
SECRET_KEY = 'django-insecure-rent-system-bishe-dev-2026-9f3a1c7d2e8b'

DEBUG = True

# 花生壳映射演示需要接受任意 Host；生产环境请收敛为具体域名
ALLOWED_HOSTS = ['*']

# ============================================
# 应用定义
# ============================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 第三方
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    # 本项目应用（按定稿 11 张核心表规划，骨架期仅占位，阶段②填充模型）
    'apps.users.apps.UsersConfig',
    'apps.lessor.apps.LessorConfig',
    'apps.house.apps.HouseConfig',
    'apps.appointment.apps.AppointmentConfig',
    'apps.contract.apps.ContractConfig',
    'apps.bill.apps.BillConfig',
    'apps.repair.apps.RepairConfig',
    'apps.favorite.apps.FavoriteConfig',
    'apps.notice.apps.NoticeConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CORS 需位于 CommonMiddleware 之前
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'rent_system.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'rent_system.wsgi.application'
ASGI_APPLICATION = 'rent_system.asgi.application'

# 自定义用户模型：AbstractUser + role 字段（tenant/landlord/admin）
AUTH_USER_MODEL = 'users.User'

# ============================================
# 数据库：开发期 SQLite（零配置，文件位于项目根目录）
# ============================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# —— 部署期切换 MySQL 8：安装 mysqlclient 后取消下方注释 ——
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'rent_system',
#         'USER': 'root',
#         'PASSWORD': 'your_password',
#         'HOST': '127.0.0.1',
#         'PORT': '3306',
#         'OPTIONS': {'charset': 'utf8mb4'},
#     }
# }

# —— 可选：接入 Redis 做缓存 / 登录态（便携版已装，端口 6379）——
# 需先 pip install django-redis，再取消注释：
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',
#         'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
#     }
# }
# SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 登录态存 Redis

# 密码校验规则
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ============================================
# 国际化：中文界面 + 东八区时间
# ============================================
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = False

# 静态文件与媒体文件（房源图片等上传至 media/）
STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================
# DRF 配置：骨架期放开权限便于联调，业务开发后逐步收紧
# ============================================
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# ============================================
# 跨域配置：允许 Vue 开发服务器（5173）访问 8000 端口
# 生产部署（dist 由 Django 托管）时同源，无需跨域
# ============================================
CORS_ALLOW_ALL_ORIGINS = True
# 若启用 Cookie 登录态，改为白名单并开启 credentials：
# CORS_ALLOWED_ORIGINS = ['http://localhost:5173', 'http://127.0.0.1:5173']
# CORS_ALLOW_CREDENTIALS = True
