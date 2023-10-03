from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.decorators import api_view
from djstripe.models import Product
from accounts.models import User
from djstripe.models import Price, Product, Subscription, Customer, PaymentIntent, PaymentMethod, APIKey
from dotenv import load_dotenv
import os
import stripe
from stripe.error import StripeError
import traceback
# Get your secret Stripe API key from your Django settings (typically from environment variables)
from djstripe import settings as djstripe_settings
# print(dir(djstripe_settings.djstripe_settings))
# Print the Stripe secret key
# print("Stripe Secret Key:", djstripe_settings.djstripe_settings.STRIPE_SECRET_KEY)

# Print the Stripe public key
# print("Stripe Public Key:", djstripe_settings.djstripe_settings.STRIPE_PUBLIC_KEY)

def get_env_variables(key):
    load_dotenv(override=True)
    return os.getenv(key)

stripe_secret_key = get_env_variables("STRIPE_TEST_SECRET_KEY")
# print("Stripe Secret Key:", stripe_secret_key)

# Set the Stripe API key
stripe.api_key = stripe_secret_key

@api_view(['POST'])
def create_billing_session(request):
    # Replace 'customer_id' with the actual ID of the customer
    fireid = request.data.get('fireid')
    user = User.objects.get(fireid=fireid)
    if not user.customer:
        CustomerView.create_stripe_customer(user)
    try:
        session = stripe.billing_portal.Session.create(
            customer=user.customer.id,
            return_url='http://localhost:3000/products',  # Replace with your website's success URL
        )

        return Response({'url': session.url})
    except Exception as e:
        print('Error:', str(e))
        traceback.print_exc()  # Print the full traceback

        return Response({'error': str(e)}, status=500)

class CustomerView(APIView):

    def post(self, request):
        pass

    @staticmethod
    def create_stripe_customer(user):
        # Check if the user already has a Djstripe customer associated.
        if not Customer.objects.filter(subscriber=user).exists():
            # Create a new Stripe customer using the Stripe API
            # Customer doesn't exist in Djstripe, check in Stripe
            existing_stripe_customer = stripe.Customer.list(email=user.email, limit=1).data

            if existing_stripe_customer:
                # Retrieve the first matching customer from Stripe
                # print(existing_stripe_customer)
                stripe_customer = stripe.Customer.retrieve(existing_stripe_customer[0].id)
                print(type(stripe_customer),'jaane')
            else:
                # Create a new Stripe customer using the Stripe API
                stripe_customer = stripe.Customer.create(
                    email=user.email,
                    # Add other customer details as needed
                )
            # print(stripe_customer, type(stripe_customer))

            try:
                # Try to sync the Djstripe customer data with the Stripe data
                djstripe_customer = Customer.sync_from_stripe_data(stripe_customer)
                djstripe_customer.subscriber = user
                djstripe_customer.save()
                user.customer = djstripe_customer
                user.save()
            except Exception as sync_error:
                # Handle any exceptions that may occur during the Djstripe synchronization
                print(f"Error syncing Djstripe customer: {str(sync_error)}")

        else:
            djstripe_customer = Customer.objects.get(subscriber=user)

        return djstripe_customer


@api_view(['POST'])
def create_checkout_session(request):
    try:
        priceid = request.data.get('priceid')
        fireid = request.data.get('fireid')
        user = User.objects.get(fireid=fireid)
        if not user.customer:
            CustomerView.create_stripe_customer(user)
        
        price = Price.objects.get(id=priceid)
        # Create a Checkout Session
        # print(user.customer.id)
        checkout_session = stripe.checkout.Session.create(
            # payment_method_types=['card'],
            customer=user.customer.id,
            line_items=[
                {
                    'price': priceid,
                    'quantity': 1,
                },
            ],
            mode='payment' if price.type == 'one_time' else 'subscription',
            success_url='http://localhost:3000/dashboard',
            cancel_url='http://localhost:3000/products',
        )

        # Return the session ID to your React app
        return Response({'sessionId': checkout_session.id})
    except Exception as e:
        return Response({'error': str(e)})


@api_view(['GET'])
def get_products(request):
    products = Product.objects.filter(active=True)
    serialized_products = []

    for product in products:
        serialized_product = {
            "id": product.id,
            "name": product.name,
            "prices": []
        }

        # Filter prices to only include active ones
        prices = Price.objects.filter(product=product, active=True)

        for price in prices:
            serialized_price = {
                "id": price.id,
                "unit_amount": price.unit_amount,
            }
            serialized_product["prices"].append(serialized_price)

        serialized_products.append(serialized_product)

    return Response(serialized_products)