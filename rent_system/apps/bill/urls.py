"""账单路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('bills', views.BillViewSet, basename='bills')

urlpatterns = [path('', include(router.urls))]
