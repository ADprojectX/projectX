from celery import Celery
from django.conf import settings

# Create a Celery app object
app = Celery('projectX')

# Load the Celery settings from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
