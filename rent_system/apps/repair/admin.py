"""Admin：报修工单。"""
from django.contrib import admin

from .models import Repair


@admin.register(Repair)
class RepairAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'house', 'category', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('house__title', 'tenant__username', 'description')
