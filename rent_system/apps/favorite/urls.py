"""收藏路由。"""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('favorites', views.FavoriteViewSet, basename='favorites')

urlpatterns = [path('', include(router.urls))]
