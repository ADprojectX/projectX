from celery import Celery
from django.conf import settings
import os
# Create a Celery app object
app = Celery('projectX')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectX.settings")
# Load the Celery settings from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# import os
# from celery import Celery
  
# # set the default Django settings module for the 'celery' program.
# 

# app = Celery('projectX')
  
# # Using a string here means the worker doesn't 
# # have to serialize the configuration object to 
# # child processes. - namespace='CELERY' means all 
# # celery-related configuration keys should 
# # have a `CELERY_` prefix.
# app.config_from_object('django.conf:settings',
#                        namespace='CELERY')
  
# # Load task modules from all registered Django app configs.
# app.autodiscover_tasks()