from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Request, Script, ProjectAssets, Scene
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
import jwt
from accounts.models import User
import os
import base64
import zipfile
import json
from utility.backendProcessInterface import process_scenes, process_image_desc, path_to_request, generate_initial_assets, get_current_images
from utility.text_to_audio import get_voice_samples
from django.http import StreamingHttpResponse
from django.http import HttpResponse
from wsgiref.util import FileWrapper

OBJECT_STORE = os.path.join(os.getcwd(), "OBJECT_STORE")

def user_authorization(jwt_token):
    try:
        payload = jwt.decode(jwt_token, 'secrett', algorithms=['HS256'])
        user_id = payload.get('id')
        user = User.objects.get(id=user_id)
        if not user.is_authenticated:
            return Response({'message': 'User is not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)
        return user
    except jwt.exceptions.InvalidTokenError:
        return Response({'message': 'Invalid JWT token'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def create_request(request):
    jwt_token = request.COOKIES.get('jwt')
    # if not jwt_token:
    #     return Response({'message': 'JWT token not found'}, status=status.HTTP_401_UNAUTHORIZED)
    user = user_authorization(jwt_token)
    if user is None:
        return Response({'message': 'User authentication failed'}, status=status.HTTP_401_UNAUTHORIZED)

    topic = request.data.get('topic')
    print(topic, 'asfyat')
    req = Request.objects.create(user=user, topic=topic)

    # Process the request and generate the script as a dictionary
    script_dict = process_scenes(request)

    try:
        # Retrieve the existing Script object for the Request (if it exists)
        script = Script.objects.get(request=req)
        script.save()
        script.add_entire_script(script_dict)  # Update the script_data field
        script.save()  # Save the changes to the existing Script object
    except Script.DoesNotExist:
        # If the Script object doesn't exist, create a new one
        script = Script.objects.create(request=req)
        script.save()
        script.add_entire_script(script_dict)
        script.save()
    return Response({'message': 'Request created successfully', 'script': script_dict, 'reqid': req.id})


@api_view(['GET'])
def get_script(request):
    req_id = request.query_params.get('reqid')
    try:
        req = Request.objects.get(id=req_id)
        try:
            script = Script.objects.get(request=req)
            current_script = script.get_current_script()
            # script_dict = script.script_data
            print(current_script)
            return Response({'message': 'Script retrieved successfully', 'script': current_script})
        except Script.DoesNotExist:
            return Response({'message': 'Script not found'}, status=status.HTTP_404_NOT_FOUND)
    except Request.DoesNotExist:
        return Response({'message': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

# Your other views here (save_script, get_video_files, voice_samples, voice_view)

@api_view(['POST'])
def save_script(request):
    payload = request.data
    req_id = payload.get('reqid')
    voice = payload.get('voice')
    final_scene = payload.get('scenes')

    if final_scene and req_id:
        try:
            # Retrieve the associated Request object
            req = Request.objects.get(id=req_id)
            req.voice = voice
            req.save()
            # Deserialize the final_scene JSON string to a Python object
            script_dict = json.loads(final_scene)
            
            # Check if a Script object exists for the Request
            script, created = Script.objects.get_or_create(request=req)  # Use request_id for the lookup
            
            # Update the script_data field in the Script model
            initial_script = process_image_desc(script_dict)
            script.add_entire_script(initial_script)
            
            request_path = path_to_request(req)
            generate_initial_assets(req, script.current_scenes, request_path, 'mjx')

            if not created:
                return Response({'success': True})
            
            # If the Script object was created, return a different response indicating it's an update
            return Response({'success': True, 'message': 'Script updated successfully'})
            
        except Request.DoesNotExist:
            return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format in finalScene parameter'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'finalScene or reqid parameter not provided'}, status=status.HTTP_400_BAD_REQUEST)



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

@api_view(["GET"])
def voice_samples(request):
    voice_samples = get_voice_samples()  # Assuming you have the logic to populate the voice_samples dictionary
    serialized_voice_samples = {}
    for audio_name, audio_data in voice_samples.items():
        base64_audio = base64.b64encode(audio_data).decode('utf-8')
        serialized_voice_samples[audio_name] = base64_audio

    return Response(serialized_voice_samples)

@api_view(["GET"])
def get_thumbnail_images(request):
    # req_id = request.query_params.get('reqid')
    req = Request.objects.get(id=77)
    img_asset = ProjectAssets.objects.get(request=req)
    return Response()

@api_view(["GET"])
def get_user_projects(request):
    jwt_token = request.COOKIES.get('jwt')
    user = user_authorization(jwt_token)
    user_requests = Request.objects.filter(user=user).values()
    return Response(user_requests)
# @api_view(["GET"])
# def set_voice(request):
#     req_id = request.GET.get('reqid')
#     selected_voice = request.GET.get('selectedValue')

#     try:
#         # Validate that req_id is a valid integer
#         req_id = int(req_id)
#     except (TypeError, ValueError):
#         return Response({'error': 'Invalid reqid'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         req = Request.objects.get(id=req_id)
#         req.voice = selected_voice
#         req.save()
        
#         # Fetch the associated Script object using the related name
#         script = Script.objects.get(request=req)
#         # Access the script_data attribute
#         script_data = script.script_data
        
#         # Perform actions based on the request object (req)
#         # Access req attributes like req.user, req.topic, etc.
#         # Process the request and update the script_data in the Script model
#         user_folder = OBJECT_STORE + "/" + str(request.user.id)
#         None if os.path.exists(user_folder) else os.makedirs(user_folder)
#         request_folder = user_folder + "/" + str(req_id)
#         None if os.path.exists(request_folder) else os.makedirs(request_folder)
#         voice = req.voice
        
#         # Process the request and use the script_data as needed
        
#         # Return a response (example)
#         data = {
#             'message': f'You selected: {selected_voice}',
#             'script_data': script_data,
#         }
#         return Response(data)

#     except Request.DoesNotExist:
#         return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
#     except Script.DoesNotExist:
#         return Response({'error': 'Script not found'}, status=status.HTTP_404_NOT_FOUND)