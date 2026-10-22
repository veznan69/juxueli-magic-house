"""用户模型：基于 AbstractUser 扩展，增加角色与手机号。"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """登录账号表：只存"能登录的人"，三角色统一管理。"""

    class Roles(models.TextChoices):
        TENANT = 'tenant', '租客'
        LANDLORD = 'landlord', '房东'
        ADMIN = 'admin', '管理员'

    role = models.CharField('角色', max_length=10, choices=Roles.choices,
                            default=Roles.TENANT)
    phone = models.CharField('手机号', max_length=20, blank=True, default='')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'

    @property
    def is_admin_role(self):
        """是否管理员（含超管）。"""
        return self.role == self.Roles.ADMIN or self.is_superuser

    @property
    def is_landlord_role(self):
        """是否房东。"""
        return self.role == self.Roles.LANDLORD
