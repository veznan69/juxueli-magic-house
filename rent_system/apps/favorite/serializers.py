"""收藏序列化器。"""
from rest_framework import serializers

from apps.house.models import House

from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    house_title = serializers.CharField(source='house.title', read_only=True)
    house_rent = serializers.DecimalField(source='house.rent', max_digits=10,
                                          decimal_places=2, read_only=True)
    house_rooms = serializers.CharField(source='house.rooms', read_only=True)
    house_district = serializers.CharField(source='house.district', read_only=True)
    house_status = serializers.CharField(source='house.status', read_only=True)

    class Meta:
        model = Favorite
        fields = ('id', 'house', 'house_title', 'house_rent', 'house_rooms',
                  'house_district', 'house_status', 'created_at')
        read_only_fields = fields


class ToggleSerializer(serializers.Serializer):
    house_id = serializers.IntegerField()
