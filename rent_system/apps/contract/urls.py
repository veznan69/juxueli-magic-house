"""合同路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('contracts', views.ContractViewSet, basename='contracts')

urlpatterns = [path('', include(router.urls))]
