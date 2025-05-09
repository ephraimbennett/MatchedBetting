import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "house_hedge.settings")
app = Celery("house_hedge")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
