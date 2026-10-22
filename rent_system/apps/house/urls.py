"""房源路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('houses', views.HouseViewSet, basename='houses')
router.register('admin-houses', views.AdminHouseViewSet, basename='admin-houses')

urlpatterns = [path('', include(router.urls))]
