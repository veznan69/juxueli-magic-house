"""ASGI 配置：异步部署入口（当前毕设未使用，预留）。"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rent_system.settings')

application = get_asgi_application()
