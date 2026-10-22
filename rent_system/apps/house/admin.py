"""Admin：房源与房源图片。"""
from django.contrib import admin

from .models import House, HouseImage


class HouseImageInline(admin.TabularInline):
    model = HouseImage
    extra = 0


@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'district', 'rooms', 'area', 'rent',
                    'status', 'landlord', 'view_count', 'created_at')
    list_filter = ('status', 'district', 'rooms')
    search_fields = ('title', 'address', 'district')
    list_editable = ('status',)
    inlines = [HouseImageInline]
    date_hierarchy = 'created_at'


@admin.register(HouseImage)
class HouseImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'house', 'is_cover', 'uploaded_at')
