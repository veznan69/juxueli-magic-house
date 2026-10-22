"""认证序列化器：注册 / 用户信息。"""
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """用户信息（登录态返回）。"""

    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'phone', 'email', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(label='密码', write_only=True, min_length=6,
                                     style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'phone', 'role')

    def validate_role(self, value):
        # 注册只允许创建租客/房东，管理员由后台分配
        if value not in ('tenant', 'landlord'):
            raise serializers.ValidationError('注册角色仅支持租客或房东')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
