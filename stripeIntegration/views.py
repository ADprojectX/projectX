from django.shortcuts import render
from rest_framework.views import APIView
from djstripe.models import Product
# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def pricing_page(request):
    products = Product.objects.all()
    # Serialize the products data into JSON format
    serialized_products = [{'name': product.name, 'plans': [{'nickname': plan.nickname, 'price': plan.human_readable_price} for plan in product.plan_set.all()]} for product in products]
    return Response({'products': serialized_products})
# @api_view(['GET'])
# def pricing_page(request):
#     return render(request, 'pricing_page.html', {
#         'products': Product.objects.all()
#     })
class PricingView(APIView):
    def get(self, request):
        return render(request, 'pricing_page.html', {
        'products': Product.objects.all()
    })

