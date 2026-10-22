"""报修序列化器。"""
from rest_framework import serializers

from .models import Repair


class RepairSerializer(serializers.ModelSerializer):
    house_title = serializers.CharField(source='house.title', read_only=True)
    tenant_name = serializers.CharField(source='tenant.username', read_only=True)

    class Meta:
        model = Repair
        fields = ('id', 'house', 'house_title', 'tenant', 'tenant_name',
                  'category', 'description', 'status', 'reply',
                  'created_at', 'finished_at')
        read_only_fields = ('id', 'tenant', 'status', 'reply',
                            'created_at', 'finished_at')

    def validate_category(self, value):
        if value not in ('水电', '门窗', '家电', '家具', '其他'):
            raise serializers.ValidationError('报修类型不合法')
        return value
