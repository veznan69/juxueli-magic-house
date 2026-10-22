"""预约路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('appointments', views.TenantAppointmentViewSet, basename='appointments')
router.register('landlord/appointments', views.LandlordAppointmentViewSet,
                basename='landlord-appointments')

urlpatterns = [path('', include(router.urls))]
