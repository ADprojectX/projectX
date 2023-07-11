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
import zipfile
# print(os.getcwd())
# from projectX.utility.backendProcess import process_request
from utility.backendProcess import process_request
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from wsgiref.util import FileWrapper

@api_view(['POST'])
def create_request(request):
    jwt_token = request.COOKIES.get('jwt')
    if not jwt_token:
        return Response({'message': 'JWT token not found'}, status=status.HTTP_401_UNAUTHORIZED)
    
    try:
        payload = jwt.decode(jwt_token, 'secrett', algorithms=['HS256'])
        user_id = payload.get('id')
        user = User.objects.get(id=user_id)
        # print(user)
        if not user.is_authenticated:
            print('here')
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.InvalidTokenError:
        return Response({'message': 'Invalid JWT token'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

    topic = request.data.get('topic')
    # voice = request.data.get('voice')
    req = Request.objects.create(user=user, topic=topic)#, voice=voice)
    req.script = process_request(request, user_id, req.id)
    req.save()
    print(req.id, 'request')
    return Response({'message': 'Request created successfully','script': req.script,'reqid':req.id})

@api_view(['GET'])
def get_script(request):
    req_id = request.query_params.get('reqid')
    print(req_id, 'fetch')
    try:
        req = Request.objects.get(id=req_id)
        print(req.script)
        # Process the request and generate the script
        # Modify this function based on your requirements
        return Response({'message': 'Script retrieved successfully', 'script': req.script})
    except Request.DoesNotExist:
        return Response({'message': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_video_files(request):
    # Assuming your video files are stored in a specific directory
    video_directory = os.path.join(os.getcwd(), 'OBJECT_STORE', '12', '54', 'output')

    # Get the list of video file names
    video_files = os.listdir(video_directory)

    # Create a temporary zip file
    temp_zip_path = os.path.join(video_directory, 'temp.zip')

    # Iterate through the video files and add them to the zip file
    with zipfile.ZipFile(temp_zip_path, 'w') as zip_file:
        for file_name in video_files:
            file_path = os.path.join(video_directory, file_name)
            zip_file.write(file_path, arcname=file_name)

    # Open the zip file in binary mode and create a file wrapper
    file_wrapper = FileWrapper(open(temp_zip_path, 'rb'))

    # Create a response with the file wrapper as the content
    response = HttpResponse(file_wrapper, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="video_files.zip"'

    # Delete the temporary zip file
    os.remove(temp_zip_path)

    return response