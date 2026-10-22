"""公告序列化器。"""
from rest_framework import serializers

from .models import Notice


class NoticeSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source='publisher.username',
                                           read_only=True, default='')

    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'publisher', 'publisher_name',
                  'created_at')
        read_only_fields = ('id', 'publisher', 'publisher_name', 'created_at')
