"""合同接口：租客看自己的，房东看名下房源的（只读，签约由后台/后续流程生成）。"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Contract
from .serializers import ContractSerializer


class ContractViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        base = Contract.objects.select_related('house', 'tenant')
        if user.is_landlord_role:
            return base.filter(house__landlord__in=user.lessors.all())
        return base.filter(tenant=user)
