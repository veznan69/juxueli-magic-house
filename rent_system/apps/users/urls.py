"""认证与用户管理路由：auth 子路由 + 管理端用户路由。"""
from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

# 认证接口（由主路由挂到 /api/v1/auth/ 下）
auth_urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('me/', views.MeView.as_view(), name='me'),
]

# 管理端用户管理（挂到 /api/v1/ 下）
router = DefaultRouter()
router.register('admin-users', views.AdminUserViewSet, basename='admin-users')

urlpatterns = auth_urlpatterns + router.urls
