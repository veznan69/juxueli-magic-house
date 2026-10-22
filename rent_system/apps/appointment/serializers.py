"""预约序列化器。"""
from rest_framework import serializers

from apps.house.models import House

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    house_title = serializers.CharField(source='house.title', read_only=True)
    house_district = serializers.CharField(source='house.district', read_only=True)
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'house', 'house_title', 'house_district', 'tenant',
                  'tenant_name', 'visit_time', 'phone', 'remark', 'status',
                  'created_at')
        read_only_fields = ('id', 'tenant', 'status', 'created_at')

    def validate_house(self, value):
        if value.status == House.Status.OFFLINE:
            raise serializers.ValidationError('该房源已下架，无法预约')
        return value
