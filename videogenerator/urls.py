from django.urls import path, include
from . import views

urlpatterns = [
    path("project/", views.create_request, name='createprojectrequest'),
    # path('project/<int:reqid>/', views.project, name='projectView'),
]
