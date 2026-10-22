"""自定义权限：按角色控制接口访问。"""
from rest_framework.permissions import BasePermission


class IsLandlord(BasePermission):
    """仅房东（操作员）可访问。"""
    message = '仅房东账号可执行此操作'

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and getattr(request.user, 'is_landlord_role', False))


class IsAdminRole(BasePermission):
    """仅管理员（或超管）可访问。"""
    message = '仅管理员账号可执行此操作'

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and getattr(request.user, 'is_admin_role', False))


class IsTenant(BasePermission):
    """仅租客可访问。"""
    message = '仅租客账号可执行此操作'

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated
                    and request.user.role == 'tenant')
