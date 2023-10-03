from django.urls import path, include
from . import views
from . import stripewebhooks

urlpatterns = [
     path('checkout-session/', views.create_checkout_session, name='checkout_session'),
     path('get-products/', views.get_products, name='get_products'),
     path('stripe-webhook/', stripewebhooks.webhook, name='stripe_webhook'),
     path('create_billing_session/', views.create_billing_session, name='create_billing_session'),
#     path('/', views2.PricingView.as_view(), name='pricing_page'),
#     path('page/', views2.pricing_page, name='pricing_page'),
]