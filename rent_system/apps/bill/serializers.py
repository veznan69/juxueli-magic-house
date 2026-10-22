"""账单序列化器。"""
from rest_framework import serializers

from .models import Bill


class BillSerializer(serializers.ModelSerializer):
    house_title = serializers.CharField(source='contract.house.title', read_only=True)
    tenant_name = serializers.CharField(source='contract.tenant.username', read_only=True)

    class Meta:
        model = Bill
        fields = ('id', 'contract', 'house_title', 'tenant_name', 'period',
                  'amount', 'due_date', 'status', 'paid_at')
        read_only_fields = fields
