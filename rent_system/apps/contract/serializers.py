"""合同序列化器。"""
from rest_framework import serializers

from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    house_title = serializers.CharField(source='house.title', read_only=True)
    house_district = serializers.CharField(source='house.district', read_only=True)
    house_rooms = serializers.CharField(source='house.rooms', read_only=True)
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)

    class Meta:
        model = Contract
        fields = ('id', 'house', 'house_title', 'house_district', 'house_rooms',
                  'tenant', 'tenant_name', 'start_date', 'end_date',
                  'monthly_rent', 'deposit', 'status', 'created_at')
        read_only_fields = fields
