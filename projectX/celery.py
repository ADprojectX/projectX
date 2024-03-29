from celery import Celery
from django.conf import settings
import os
from kombu import Queue

# Create a Celery app object
app = Celery('projectX')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectX.settings")
# Load the Celery settings from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

task_queues = (
    Queue('audio_queue', priority=2,max_priority=2),
    Queue('mj_queue', priority=10,max_priority=10),
    Queue('video_generator_queue'),
    Queue('sdxl_queue', priority=10,max_priority=10)
    # Add other queues here if needed
)
# Set the custom queue for the task
app.conf.task_routes = {
    'projectX.utility.tasks.sent_mj_image_request': {'queue': 'mj_queue'},
    'projectX.utility.tasks.sent_audio_request': {'queue': 'audio_queue'},
    'projectX.utility.tasks.captionated_video': {'queue': 'video_generator_queue'},
    'projectX.utility.tasks.sent_sdxl_image_request': {'queue': 'sdxl_queue'},
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
# Limit the number of workers
# Limit the number of workers for the limited_queue only
# app.conf.worker_concurrency = {
#     'limited_queue': 2,
#     'default': 4,  # Set the desired concurrency for the default queue
# }
# Auto-discover tasks in all installed apps
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