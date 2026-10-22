"""收藏接口：列表 + 收藏/取消收藏开关。"""
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.house.models import House

from .models import Favorite
from .serializers import FavoriteSerializer, ToggleSerializer


class FavoriteViewSet(viewsets.ReadOnlyModelViewSet):
    """我的收藏：列表与取消由 toggle 完成。"""
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Favorite.objects.filter(user=self.request.user)
                .select_related('house'))

    @action(detail=False, methods=['post'], url_path='toggle')
    def toggle(self, request):
        """收藏 / 取消收藏（幂等开关），返回最新状态。"""
        serializer = ToggleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        house = get_object_or_404(House, pk=serializer.validated_data['house_id'])
        favorite, created = Favorite.objects.get_or_create(user=request.user, house=house)
        if not created:
            favorite.delete()
            return Response({'favorited': False, 'house_id': house.pk})
        return Response({'favorited': True, 'house_id': house.pk})
