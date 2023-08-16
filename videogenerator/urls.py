from django.urls import path, include
from . import views

urlpatterns = [
    path("project/", views.create_request, name='createprojectrequest'),
    path("fetch-script/", views.get_script, name='fetch-script'),
    path("save-script/", views.save_script, name='save-script'),
    path('video-files/', views.get_video_files, name='get_video_files'),
    path('voice-samples/', views.voice_samples, name='get_voice_samples'),
    path('get-project/', views.get_user_projects, name='get_user_projects'),
    path('get-thumbnails/', views.get_thumbnail_images, name='get_thumbnails')
    # path('set-voice/', views.set_voice, name='set_voice'),
    # path('video/', views.get_video, name='get_video'),
]
