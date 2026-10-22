"""Admin：公告。"""
from django.contrib import admin

from .models import Notice


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'publisher', 'created_at')
    search_fields = ('title', 'content')
