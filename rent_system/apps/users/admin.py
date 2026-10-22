"""Admin：用户管理。"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserModelAdmin(UserAdmin):
    list_display = ('id', 'username', 'role', 'phone', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'phone')
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {'fields': ('role', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('扩展信息', {'fields': ('role', 'phone')}),
    )
