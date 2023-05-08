from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Request
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import jwt
from accounts.models import User
import os
import sys
# print(os.getcwd())
# from projectX.utility.backendProcess import process_request
from utility.backendProcess import process_request

@api_view(['POST'])
def create_request(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return Response({'message': 'JWT token not found'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(jwt_token, 'secrett', algorithms=['HS256'])
        user_id = payload.get('id')
        user = User.objects.get(id=user_id)
        print(user)
        if not user.is_authenticated:
            print('here')
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.InvalidTokenError:
        return Response({'message': 'Invalid JWT token'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    topic = request.data.get('topic')
    voice = request.data.get('voice')
    req = Request.objects.create(user=user, topic=topic, voice=voice)
    script = process_request(request, user_id, req.id)
    return Response({'message': 'Request created successfully','script': script,'reqid':req.id})
