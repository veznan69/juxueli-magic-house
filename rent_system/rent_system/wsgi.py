"""WSGI 配置：生产部署入口（Nginx + uWSGI 场景使用）。"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rent_system.settings')

application = get_wsgi_application()
