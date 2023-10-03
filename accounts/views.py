from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.db.utils import IntegrityError
from stripeIntegration.views import CustomerView

def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.create_user(**serializer.validated_data)
            CustomerView.create_stripe_customer(user)
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Email or other unique field already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)  # For debugging
            return Response({'error': 'Something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_dashboard(request):
    uid = request.query_params.get('uid')
    user = User.objects.filter(id=uid).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)