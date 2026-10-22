"""项目级 URL 配置：Admin 后台 + API 路由（/api/v1/）+ 媒体文件。"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.users.urls import auth_urlpatterns, router as users_router
from . import views

api_v1 = [
    path('auth/', include(auth_urlpatterns)),    # 注册/登录/me
    path('', include(users_router.urls)),        # 管理端用户管理
    path('', include('apps.house.urls')),        # 房源 + 管理端房源
    path('', include('apps.appointment.urls')),  # 预约（租客/房东）
    path('', include('apps.contract.urls')),     # 合同
    path('', include('apps.bill.urls')),         # 账单
    path('', include('apps.repair.urls')),       # 报修
    path('', include('apps.favorite.urls')),     # 收藏
    path('', include('apps.notice.urls')),       # 公告
    path('stats/', views.StatsView.as_view(), name='stats'),
]

urlpatterns = [
    # Django Admin 后台
    path('admin/', admin.site.urls),
    # API v1（版本化前缀）
    path('api/v1/', include(api_v1)),
    # 健康检查与 API 根信息
    path('api/health/', views.health_check, name='health_check'),
    path('api/', views.api_root, name='api_root'),
]

# 开发期：托管上传的媒体文件（房源图片）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
