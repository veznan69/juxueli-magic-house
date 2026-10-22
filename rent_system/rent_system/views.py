"""项目级视图：健康检查、API 根信息、管理端统计聚合。"""
from django.conf import settings
from django.db.models import Count, Sum
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.bill.models import Bill
from apps.contract.models import Contract
from apps.favorite.models import Favorite
from apps.house.models import House
from apps.notice.models import Notice
from apps.repair.models import Repair
from apps.users.models import User
from apps.users.permissions import IsAdminRole


@api_view(['GET'])
def health_check(request):
    """健康检查接口：供前端探测后端连通性。"""
    return JsonResponse({
        'status': 'ok',
        'service': '房屋租赁管理系统后端',
        'version': 'v1.1',
        'debug': settings.DEBUG,
    })


@api_view(['GET'])
def api_root(request):
    """API 根信息：列出当前可用端点。"""
    return JsonResponse({
        'name': '基于Python的房屋租赁管理系统 API',
        'version': 'v1',
        'prefix': '/api/v1/',
        'endpoints': {
            'admin': '/admin/',
            'health': '/api/health/',
            'auth': '/api/v1/auth/register/ | login/ | me/',
            'houses': '/api/v1/houses/',
            'stats': '/api/v1/stats/（管理员）',
        },
    })


class StatsView(APIView):
    """管理后台统计：单次聚合返回全部指标，供 ECharts 使用。"""
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request):
        # 房源状态分布
        status_rows = House.objects.values('status').annotate(c=Count('id'))
        house_status = {row['status']: row['c'] for row in status_rows}
        # 用户角色分布
        role_rows = User.objects.values('role').annotate(c=Count('id'))
        role_counts = {row['role']: row['c'] for row in role_rows}
        # 已缴账单按账期汇总（租金收入趋势）
        income_rows = (Bill.objects.filter(status=Bill.Status.PAID)
                       .values('period').annotate(total=Sum('amount'))
                       .order_by('period'))

        return Response({
            'house_total': House.objects.count(),
            'house_status': {
                'pending': house_status.get('pending', 0),
                'available': house_status.get('available', 0),
                'rented': house_status.get('rented', 0),
                'offline': house_status.get('offline', 0),
            },
            'user_total': User.objects.count(),
            'tenant_count': role_counts.get('tenant', 0),
            'landlord_count': role_counts.get('landlord', 0),
            'contract_active': Contract.objects.filter(
                status=Contract.Status.ACTIVE).count(),
            'repair_pending': Repair.objects.exclude(
                status=Repair.Status.DONE).count(),
            'notice_count': Notice.objects.count(),
            'favorite_count': Favorite.objects.count(),
            'income': [{'period': r['period'], 'total': float(r['total'])}
                       for r in income_rows],
        })
