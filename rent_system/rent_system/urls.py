"""项目级 URL 配置：Admin 后台 + API 路由。"""
from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    # Django Admin 后台（管理员模块的骨架，阶段②注册各业务模型）
    path('admin/', admin.site.urls),
    # API 根信息
    path('api/', views.api_root, name='api_root'),
    # 健康检查：前端 / 演示环境连通性探测
    path('api/health/', views.health_check, name='health_check'),
]
