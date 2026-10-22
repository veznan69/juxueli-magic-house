"""报修接口：租客提交/查看，房东处理。"""
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsLandlord

from .models import Repair
from .serializers import RepairSerializer


class TenantRepairViewSet(viewsets.ModelViewSet):
    """租客端：我的报修（提交 / 查看）。"""
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Repair.objects.filter(tenant=self.request.user)
                .select_related('house', 'tenant'))

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class LandlordRepairViewSet(viewsets.ReadOnlyModelViewSet):
    """房东端：名下房源的报修单，可标记处理中 / 完成并反馈。"""
    serializer_class = RepairSerializer
    permission_classes = [IsAuthenticated, IsLandlord]

    def get_queryset(self):
        return (Repair.objects
                .filter(house__landlord__in=self.request.user.lessors.all())
                .select_related('house', 'tenant'))

    @action(detail=True, methods=['post'], url_path='handle')
    def handle(self, request, pk=None):
        repair = self.get_object()
        target = request.data.get('status')
        if target not in (Repair.Status.PROCESSING, Repair.Status.DONE):
            return Response({'detail': '状态不合法（processing/done）'}, status=400)
        repair.status = target
        repair.reply = request.data.get('reply', repair.reply)
        if target == Repair.Status.DONE:
            repair.finished_at = timezone.now()
        repair.save()
        return Response(RepairSerializer(repair).data)
