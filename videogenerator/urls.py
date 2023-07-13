from django.urls import path, include
from . import views

urlpatterns = [
    path("project/", views.create_request, name='createprojectrequest'),
    path("fetch-script/", views.get_script, name='fetch-script'),
    path("save-script/", views.save_script, name='save-script'),
    # path('project/<int:reqid>/', views.project, name='projectView'),
    path('video-files/', views.get_video_files, name='get_video_files'),
]
