"""Admin：预约看房。"""
from django.contrib import admin

from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'tenant', 'house', 'visit_time', 'phone', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('tenant__username', 'house__title', 'phone')
