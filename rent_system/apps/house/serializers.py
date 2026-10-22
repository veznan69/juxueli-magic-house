"""房源序列化器：列表 / 详情 / 写操作。"""
from rest_framework import serializers

from apps.lessor.models import Lessor

from .models import House, HouseImage


class HouseListSerializer(serializers.ModelSerializer):
    """列表卡片：含出租方名称与封面图。"""
    landlord_name = serializers.CharField(source='landlord.name', read_only=True)
    cover = serializers.SerializerMethodField()

    class Meta:
        model = House
        fields = ('id', 'title', 'district', 'address', 'rooms', 'area', 'rent',
                  'deposit', 'payment', 'status', 'view_count', 'landlord_name',
                  'cover', 'created_at')

    def get_cover(self, obj):
        return obj.cover_image


class HouseDetailSerializer(HouseListSerializer):
    """详情：附出租方联系信息与描述。"""
    landlord_contact = serializers.CharField(source='landlord.contact_person',
                                             read_only=True)
    landlord_phone = serializers.CharField(source='landlord.phone', read_only=True)
    facilities = serializers.SerializerMethodField()

    class Meta(HouseListSerializer.Meta):
        fields = HouseListSerializer.Meta.fields + (
            'landlord_contact', 'landlord_phone', 'description', 'facilities')

    def get_facilities(self, obj):
        return [f.strip() for f in obj.facilities.split(',') if f.strip()]


class HouseWriteSerializer(serializers.ModelSerializer):
    """房东发布 / 编辑房源。"""
    facilities = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = House
        fields = ('title', 'district', 'address', 'rooms', 'area', 'rent',
                  'deposit', 'payment', 'facilities', 'description')

    def create(self, validated_data):
        user = self.context['request'].user
        # 房东账号首次发布时自动创建个人出租主体
        lessor, _ = Lessor.objects.get_or_create(
            name=user.username,
            defaults={'contact_person': user.username, 'phone': user.phone or ''},
        )
        user.lessors.add(lessor)
        validated_data['landlord'] = lessor
        validated_data['status'] = House.Status.PENDING  # 新房源待审核
        return House.objects.create(**validated_data)


class HouseReviewSerializer(serializers.Serializer):
    """管理员审核：approve=通过上架，reject=驳回下架。"""
    action = serializers.ChoiceField(choices=['approve', 'reject'])
    reason = serializers.CharField(required=False, allow_blank=True, default='')
