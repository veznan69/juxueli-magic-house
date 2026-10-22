"""预约接口：租客发起/查看，房东处理。"""
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.users.permissions import IsLandlord

from .models import Appointment
from .serializers import AppointmentSerializer


class TenantAppointmentViewSet(viewsets.ModelViewSet):
    """租客端：我的预约（列表 / 创建 / 取消=删除）。"""
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (Appointment.objects.filter(tenant=self.request.user)
                .select_related('house', 'tenant'))

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)


class LandlordAppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    """房东端：查看名下房源的预约，并可确认 / 拒绝 / 完成。"""
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated, IsLandlord]

    def get_queryset(self):
        return (Appointment.objects
                .filter(house__landlord__in=self.request.user.lessors.all())
                .select_related('house', 'tenant'))

    @action(detail=True, methods=['post'], url_path='handle')
    def handle(self, request, pk=None):
        """处理预约：confirmed / rejected / done。"""
        appointment = self.get_object()
        target = request.data.get('status')
        if target not in (Appointment.Status.CONFIRMED, Appointment.Status.REJECTED,
                          Appointment.Status.DONE):
            return Response({'detail': '状态不合法（confirmed/rejected/done）'}, status=400)
        appointment.status = target
        appointment.save(update_fields=['status'])
        return Response(AppointmentSerializer(appointment).data)
