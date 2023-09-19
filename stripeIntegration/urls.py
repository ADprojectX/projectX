from django.urls import path, include
from . import views

urlpatterns = [
    path('/', views.PricingView.as_view(), name='pricing_page'),
    path('page/', views.pricing_page, name='pricing_page'),
]