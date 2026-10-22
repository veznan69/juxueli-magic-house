"""公告接口：全员可读，管理员发布 / 删除。"""
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.users.permissions import IsAdminRole

from .models import Notice
from .serializers import NoticeSerializer


class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminRole()]

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)
