import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('vk_custom')

app.config_from_object('django.conf:settings', namespace='CELERY')  # CELERY_BROKER_URL

app.autodiscover_tasks()  # сам находит задачи из приложений

# celery redis
