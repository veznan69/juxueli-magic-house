"""报修路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('repairs', views.TenantRepairViewSet, basename='repairs')
router.register('landlord/repairs', views.LandlordRepairViewSet, basename='landlord-repairs')

urlpatterns = [path('', include(router.urls))]
