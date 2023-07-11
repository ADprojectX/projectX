from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, JwtCsrfTokens
from .serializers import UserSerializer, LoginSerializer
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
import jwt, datetime
from rest_framework.exceptions import AuthenticationFailed
import uuid
from django.utils import timezone
from django.middleware import csrf
from rest_framework_simplejwt.authentication import JWTAuthentication

@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Get the password from the serializer data
        password = serializer.validated_data.pop('password')
        # Hash the password
        hashed_password = make_password(password)
        # Create the user with the hashed password
        user = User.objects.create(password=hashed_password, **serializer.validated_data)
        user.save()
        return Response({'id': user.id}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @csrf_exempt
@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            # Login successful
            user.last_login = timezone.now()
            user.save()
            payload = {
                'uuid': str(uuid.uuid4()),
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S.%f') if user.last_login else None,
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secrett', algorithm='HS256')
            response = Response()
            csrf_token = csrf.get_token(request)
            response['Access-Control-Allow-Origin'] = ['http://localhost:3000', "http://172.24.31.46:3000"]
            response.set_cookie(key='jwt', value=token, httponly=False, samesite='Lax',  secure=False)
            response['X-CSRFToken'] = csrf_token
            response['Authorization'] = f'Bearer {token}'
            jct = JwtCsrfTokens.objects.create(jwt_token=token, csrf_token=csrf_token)
            jct.save()
            return response
        else:
            # Login failed
            return Response({'success': False, 'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET',])
def user_dashboard(request):
    token = request.COOKIES.get('jwt')
    if not token or not JwtCsrfTokens.objects.filter(jwt_token=token).exists():
        print('here')
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secrett', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def logout_user(request):
    JwtCsrfTokens.objects.filter(jwt_token=request.COOKIES.get('jwt')).delete()
    response = Response()
    response['Access-Control-Allow-Origin'] = ['http://localhost:3000', "http://172.24.31.46:3000"]
    response.delete_cookie('jwt')
    response.data = {'message': 'Logged out successfully'}
    return response