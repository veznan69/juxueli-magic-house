"""认证与用户管理接口。"""
from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.permissions import IsAdminRole
from apps.users.serializers import RegisterSerializer, UserSerializer

from .models import User


class RegisterView(APIView):
    """注册：创建账号并返回 Token。"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data},
                        status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """登录：校验账号密码，签发 / 复用 Token。"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username', '')
        password = request.data.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response({'detail': '用户名或密码错误'},
                            status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': UserSerializer(user).data})


class MeView(APIView):
    """当前登录用户信息。"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class AdminUserViewSet(viewsets.ReadOnlyModelViewSet):
    """管理后台：用户列表 / 启停 / 改角色（仅管理员）。"""
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]
    search_fields = ('username', 'phone')

    @action(detail=True, methods=['post'], url_path='set-active')
    def set_active(self, request, pk=None):
        """启用 / 停用账号。"""
        user = self.get_object()
        if user.is_superuser:
            return Response({'detail': '不能操作超级管理员'}, status=400)
        user.is_active = bool(request.data.get('active', not user.is_active))
        user.save(update_fields=['is_active'])
        return Response(UserSerializer(user).data)

    @action(detail=True, methods=['post'], url_path='set-role')
    def set_role(self, request, pk=None):
        """调整角色。"""
        role = request.data.get('role', '')
        if role not in ('tenant', 'landlord', 'admin'):
            return Response({'detail': '角色不合法'}, status=400)
        user = self.get_object()
        user.role = role
        user.save(update_fields=['role'])
        return Response(UserSerializer(user).data)
