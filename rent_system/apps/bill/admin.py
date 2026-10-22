"""Admin：租金账单。"""
from django.contrib import admin

from .models import Bill


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('id', 'contract', 'period', 'amount', 'due_date', 'status', 'paid_at')
    list_filter = ('status', 'period')
    search_fields = ('contract__house__title', 'contract__tenant__username')
