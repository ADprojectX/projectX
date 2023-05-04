from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import authenticate
# from django.contrib.auth.backends import ModelBackend

# @api_view(['POST'])
# def login_user(request):
#     username = request.data.get('username')
#     password = request.data.get('password')

#     user = ModelBackend().authenticate(request=request, username=username, password=password)

#     if user is not None:
#         return Response({'success': True}, status=status.HTTP_200_OK)
#     else:
#         return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['POST'])
def signup(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'username already taken'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(username=username, password=password)
        user.save()
        return Response({'success': True}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class UserViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'success': True})
        else:
            return Response({'success': False, 'message': serializer.errors})


@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(request, username=username, password=password, model = User)

    if user is not None:
        return Response({'success': True}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)