"""房源接口：公开列表 / 详情、房东管理、管理员审核。"""
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsAdminRole, IsLandlord

from .models import House
from .serializers import (HouseDetailSerializer, HouseListSerializer,
                          HouseReviewSerializer, HouseWriteSerializer)


def _own_lessors(user):
    """当前房东账号可操作的出租主体集合。"""
    return user.lessors.all()


class HouseViewSet(viewsets.ModelViewSet):
    """房源：公开浏览 + 房东管理。"""

    def get_queryset(self):
        user = self.request.user
        # 详情/列表默认公开可见（待审核与已下架仅房东本人/管理员可见）
        if self.action in ('list', 'retrieve') and self.request.method == 'GET' \
                and not self.request.query_params.get('scope') == 'mine':
            base = House.objects.select_related('landlord')
            if user.is_authenticated and (user.is_landlord_role or user.is_admin_role):
                return base
            return base.exclude(status=House.Status.PENDING)
        if self.action == 'mine':
            return House.objects.filter(landlord__in=_own_lessors(user))
        return House.objects.select_related('landlord')

    def get_serializer_class(self):
        if self.action == 'list':
            return HouseListSerializer
        if self.action == 'retrieve':
            return HouseDetailSerializer
        return HouseWriteSerializer

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy',
                           'mine', 'set_status'):
            return [IsAuthenticated(), IsLandlord()]
        if self.action == 'review':
            return [IsAuthenticated(), IsAdminRole()]
        return [AllowAny()]

    def filter_queryset(self, queryset):
        """首页筛选：关键字 / 区域 / 价格区间 / 户型 / 状态 / 排序。"""
        q = self.request.query_params
        if keyword := q.get('keyword'):
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(address__icontains=keyword)
                | Q(district__icontains=keyword))
        if district := q.get('district'):
            queryset = queryset.filter(district__icontains=district)
        if rooms := q.get('rooms'):
            queryset = queryset.filter(rooms__icontains=rooms)
        if rent_min := q.get('rent_min'):
            queryset = queryset.filter(rent__gte=rent_min)
        if rent_max := q.get('rent_max'):
            queryset = queryset.filter(rent__lte=rent_max)
        if status := q.get('status'):
            queryset = queryset.filter(status=status)
        order = q.get('ordering')
        if order in ('rent', '-rent', '-view_count', '-created_at'):
            queryset = queryset.order_by(order)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """详情：浏览量 +1。"""
        instance = self.get_object()
        House.objects.filter(pk=instance.pk).update(view_count=instance.view_count + 1)
        instance.view_count += 1
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='mine')
    def mine(self, request, *args, **kwargs):
        """房东：我的房源（含待审核/已下架）。"""
        page = self.paginate_queryset(self.get_queryset())
        serializer = HouseListSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'], url_path='set-status')
    def set_status(self, request, pk=None):
        """房东：上架 / 下架自己的房源。"""
        house = self.get_object()
        if house.landlord not in _own_lessors(request.user):
            return Response({'detail': '无权操作他人房源'}, status=403)
        target = request.data.get('status')
        if target not in (House.Status.AVAILABLE, House.Status.OFFLINE):
            return Response({'detail': '仅支持上架（available）/下架（offline）'}, status=400)
        house.status = target
        house.save(update_fields=['status'])
        return Response(HouseDetailSerializer(house).data)

    @action(detail=True, methods=['post'], url_path='review')
    def review(self, request, pk=None):
        """管理员：审核待上架房源。"""
        house = self.get_object()
        serializer = HouseReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        house.status = (House.Status.AVAILABLE if serializer.validated_data['action'] == 'approve'
                        else House.Status.OFFLINE)
        house.save(update_fields=['status'])
        return Response(HouseDetailSerializer(house).data)

    def destroy(self, request, *args, **kwargs):
        house = self.get_object()
        if house.landlord not in _own_lessors(request.user) \
                and not request.user.is_admin_role:
            return Response({'detail': '无权删除他人房源'}, status=403)
        return super().destroy(request, *args, **kwargs)


class AdminHouseViewSet(viewsets.ReadOnlyModelViewSet):
    """管理后台：全部房源（含待审核），支持状态筛选。"""
    queryset = House.objects.select_related('landlord').order_by('-created_at')
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get_serializer_class(self):
        return HouseDetailSerializer if self.action == 'retrieve' else HouseListSerializer

    def filter_queryset(self, queryset):
        if status := self.request.query_params.get('status'):
            queryset = queryset.filter(status=status)
        if keyword := self.request.query_params.get('keyword'):
            queryset = queryset.filter(title__icontains=keyword)
        return queryset
