"""公告路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('notices', views.NoticeViewSet, basename='notices')

urlpatterns = [path('', include(router.urls))]
