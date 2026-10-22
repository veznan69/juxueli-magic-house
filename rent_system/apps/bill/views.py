"""账单接口：租客查看 / 缴费，房东查看名下房源账单。"""
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Bill
from .serializers import BillSerializer


class BillViewSet(viewsets.ReadOnlyModelViewSet):
    """账单：按角色自动过滤（租客=自己合同，房东=名下房源），支持状态筛选。"""
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        base = Bill.objects.select_related('contract__house', 'contract__tenant')
        if user.is_landlord_role:
            base = base.filter(contract__house__landlord__in=user.lessors.all())
        else:
            base = base.filter(contract__tenant=user)
        if status := self.request.query_params.get('status'):
            base = base.filter(status=status)
        return base

    @action(detail=True, methods=['post'], url_path='pay')
    def pay(self, request, pk=None):
        """租客缴费（模拟支付）：待缴/逾期 → 已缴。"""
        bill = self.get_object()
        if bill.contract.tenant != request.user:
            return Response({'detail': '只能缴纳自己的账单'}, status=status.HTTP_403_FORBIDDEN)
        if bill.status == Bill.Status.PAID:
            return Response({'detail': '该账单已缴纳'}, status=status.HTTP_400_BAD_REQUEST)
        bill.status = Bill.Status.PAID
        bill.paid_at = timezone.now()
        bill.save(update_fields=['status', 'paid_at'])
        return Response(BillSerializer(bill).data)
