import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hr_solution_back.settings')

app = Celery('hr_solution_back')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
