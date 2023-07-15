from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.signup_user, name='signup'),
    path("login_user/", views.login_user, name='login_user'),
    path("dashboard/", views.user_dashboard, name='dashboard'),
    path("logout/", views.logout_user, name='logout'),
    path("alive/", views.check_active, name='user-alive'),
]
