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
import pyrebase
import os
# with open(f"{os.getcwd()}/firebase-projectX.json", 'r') as json_file:
#     cred = json.load(json_file)
# // Your web app's Firebase configuration
firebaseConfig = {
"apiKey": "AIzaSyAAiQ_KMPP8QTiCLVN87FoCAkSv2eIPHTo",
"authDomain": "projectx-392305.firebaseapp.com",
"databaseURL": "https://projectx-392305-default-rtdb.firebaseio.com",
"projectId": "projectx-392305",
"storageBucket": "projectx-392305.appspot.com",
"messagingSenderId": "745908786386",
"appId": "1:745908786386:web:389226871c33d8a766c90b",
"serviceAccount": f"{os.getcwd()}/firebase-projectX.json"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

@api_view(['POST'])
def signup_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        try:
            # Get the password from the serializer data
            password = serializer.validated_data.pop('password')
            firebase_user = auth.create_user_with_email_and_password(serializer.validated_data['email'], password)
            auth.send_email_verification(firebase_user['idToken'])
            # Hash the password
            hashed_password = make_password(password)
            # Create the user with the hashed password
            user = User.objects.create(password=hashed_password, **serializer.validated_data)
            user.save()
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        except:
            return Response({'error': 'Email already exists'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        try:
            firebase_user = auth.sign_in_with_email_and_password(
                serializer.validated_data['email'], 
                serializer.validated_data['password']
            )
            
            # Firebase authentication successful, you can use the ID token
            id_token = firebase_user['idToken']
            
            # Get the user details from the Firebase user if needed
            user_info = auth.get_account_info(id_token)
            # user_info will contain information about the user, including email, user ID, etc.
            
            response = Response()
            csrf_token = csrf.get_token(request)
            response['Access-Control-Allow-Origin'] = ['http://localhost:3000', "http://172.24.31.46:3000"]
            response['X-CSRFToken'] = csrf_token
            response['Authorization'] = f'Bearer {id_token}'
            
            return response
        except Exception as e:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @csrf_exempt
@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            # Login successful
            user.last_login = timezone.now()
            user.save()
            payload = {
                'uuid': str(uuid.uuid4()),
                'last_login': user.last_login.strftime('%Y-%m-%d %H:%M:%S.%f') if user.last_login else None,
                'id': str(user.id),
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

@api_view(['POST'])
def check_active(request):
    token = request.COOKIES.get('jwt')
    if not token or not JwtCsrfTokens.objects.filter(jwt_token=token).exists():
        # print('useasdvuyvaiusr')
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secrett', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user_id = payload['id']
    user = User.objects.filter(id=user_id).first()
    if user:
        email = user.email
        return Response({'email': email}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

