"""项目级视图：健康检查与 API 根信息（骨架期）。"""
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET'])
def health_check(request):
    """健康检查接口：供前端探测后端连通性。"""
    return JsonResponse({
        'status': 'ok',
        'service': '房屋租赁管理系统后端',
        'version': 'v1.0-skeleton',
        'debug': settings.DEBUG,
    })


@api_view(['GET'])
def api_root(request):
    """API 根信息：列出当前可用端点。"""
    return JsonResponse({
        'name': '基于Python的房屋租赁管理系统 API',
        'version': 'v1',
        'endpoints': {
            'admin': '/admin/',
            'health': '/api/health/',
        },
    })
