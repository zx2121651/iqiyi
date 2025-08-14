import os
from celery import Celery

# 设置 Django 的 settings 模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'xiaohongshu_backend.settings')

app = Celery('xiaohongshu_backend')

# 使用 Django settings.py 中定义的 CELERY 配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从所有已注册的 Django app 中加载 tasks.py
app.autodiscover_tasks()
