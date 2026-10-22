"""Admin：租赁合同。"""
from django.contrib import admin

from .models import Contract


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'house', 'tenant', 'start_date', 'end_date',
                    'monthly_rent', 'deposit', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('house__title', 'tenant__username')
