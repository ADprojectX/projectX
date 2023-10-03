from rest_framework.response import Response
import stripe
from djstripe.models import Event 
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework.decorators import api_view
from dotenv import load_dotenv
import os

# endpoint_secret = 'whsec_74c33570eb2b6fb5aaeb130506a4d4da1855a7d6882fe7bba3b4b640a9f0d3ce'
def get_env_variables(key):
    load_dotenv(override=True)
    return os.getenv(key)

stripe_secret_key = get_env_variables("STRIPE_TEST_SECRET_KEY")
# print("Stripe Secret Key:", stripe_secret_key)

# Set the Stripe API key
stripe.api_key = stripe_secret_key
endpoint_secret = 'whsec_7PYw23FTkNQgkJ71a43aI2Vq9aroMgc8'

@api_view(["POST"])
@csrf_exempt
def webhook(request):
  event = None
  payload = request.body.decode('utf-8')
  signature = request.headers.get('Stripe-Signature')
  try:
    event = stripe.Webhook.construct_event(
      payload=payload,
      sig_header=signature,
      secret=endpoint_secret,
    )
  except ValueError as e:
    # Invalid payload
    raise e
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    raise e
  
  # Handle the event
  if event['type'] == 'balance.available':
    balance = event['data']['object']
  elif event['type'] == 'billing_portal.configuration.created':
    configuration = event['data']['object']
  elif event['type'] == 'billing_portal.configuration.updated':
    configuration = event['data']['object']
  elif event['type'] == 'billing_portal.session.created':
    session = event['data']['object']
  elif event['type'] == 'checkout.session.async_payment_failed':
    session = event['data']['object']
  elif event['type'] == 'checkout.session.async_payment_succeeded':
    session = event['data']['object']
  elif event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    print(session)
  elif event['type'] == 'checkout.session.expired':
    session = event['data']['object']
  elif event['type'] == 'customer.created':
    customer = event['data']['object']
  elif event['type'] == 'customer.deleted':
    customer = event['data']['object']
  elif event['type'] == 'customer.updated':
    customer = event['data']['object']
  elif event['type'] == 'customer.discount.created':
    discount = event['data']['object']
  elif event['type'] == 'customer.discount.deleted':
    discount = event['data']['object']
  elif event['type'] == 'customer.discount.updated':
    discount = event['data']['object']
  elif event['type'] == 'customer.source.created':
    source = event['data']['object']
  elif event['type'] == 'customer.source.deleted':
    source = event['data']['object']
  elif event['type'] == 'customer.source.expiring':
    source = event['data']['object']
  elif event['type'] == 'customer.source.updated':
    source = event['data']['object']
  elif event['type'] == 'customer.subscription.created':
    subscription = event['data']['object']
  elif event['type'] == 'customer.subscription.deleted':
    subscription = event['data']['object']
  elif event['type'] == 'customer.subscription.paused':
    subscription = event['data']['object']
  elif event['type'] == 'customer.subscription.pending_update_applied':
    subscription = event['data']['object']
  elif event['type'] == 'customer.subscription.pending_update_expired':
    subscription = event['data']['object']
  elif event['type'] == 'customer.subscription.resumed':
    subscription = event['data']['object']
  elif event['type'] == 'customer.subscription.trial_will_end':
    subscription = event['data']['object']
  elif event['type'] == 'customer.subscription.updated':
    subscription = event['data']['object']
  elif event['type'] == 'subscription_schedule.aborted':
    subscription_schedule = event['data']['object']
  elif event['type'] == 'subscription_schedule.canceled':
    subscription_schedule = event['data']['object']
  elif event['type'] == 'subscription_schedule.completed':
    subscription_schedule = event['data']['object']
  elif event['type'] == 'subscription_schedule.created':
    subscription_schedule = event['data']['object']
  elif event['type'] == 'subscription_schedule.expiring':
    subscription_schedule = event['data']['object']
  elif event['type'] == 'subscription_schedule.released':
    subscription_schedule = event['data']['object']
  elif event['type'] == 'subscription_schedule.updated':
    subscription_schedule = event['data']['object']
  # ... handle other event types
  else:
    print('Unhandled event type {}'.format(event['type']))

  return Response({"success":True})


@csrf_exempt
def stripe_webhook(request):
    # Retrieve the webhook payload
    payload = request.body.decode('utf-8')
    
    # Verify and parse the webhook event
    try:
        event = stripe.Event.construct_from(
            json.loads(payload), 
            stripe.api_key,
            stripe_version=None  # Use the latest API version
        )
    except ValueError as e:
        return JsonResponse({'error': 'Invalid payload'}, status=400)

    # Handle the specific event type (e.g., 'payment_intent.succeeded')
    if event.type == 'payment_intent.succeeded':
        # Add your event handling code here
        pass

    return JsonResponse({'status': 'Webhook received successfully'})
# def stripe_webhook(request):
#     if request.method == "POST":
#         payload = request.body
#         sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, sig_header,"whsec_74c33570eb2b6fb5aaeb130506a4d4da1855a7d6882fe7bba3b4b640a9f0d3ce"
#             )
#         except ValueError as e:
#             # Invalid payload
#             return Response(status=400)

#         # Handle the specific event type (e.g., 'checkout.session.completed')
#         if event.type == "checkout.session.completed":
#             # The event corresponds to a successful subscription
#             # You can access the subscription and customer data from 'event.data.object'
#             subscription_data = event.data.object

#             # Now, save the relevant data to your Djstripe models
#             # Example: Create an Event object
#             Event.objects.create(
#                 stripe_id=event.id,
#                 kind=event.type,
#                 webhook_message=json.loads(payload),
#             )

#             # You can process and save additional data to other Djstripe models here

#         return Response(status=200)
#     return Response(status=405)