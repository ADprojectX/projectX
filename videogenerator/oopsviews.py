from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Request, Script, ProjectAssets, Scene
from utility.aws_connector import cdn_path
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from accounts.models import User
import os
import base64
import json
from utility.backendProcessInterface import *
from utility.text_to_audio import get_voice_samples
from django.views import View

OBJECT_STORE = os.path.join(os.getcwd(), "OBJECT_STORE")

class RequestView(View):
    @staticmethod
    @api_view(['POST'])
    def create_request(request):
        fireid = request.data.get('fireid')
        user = User.objects.get(fireid=fireid)
        topic = request.data.get('topic')
        req = Request.objects.create(user=user, topic=topic)

        # Process the request and generate the script as a dictionary
        script_dict = process_scenes(request)

        try:
            # Retrieve the existing Script object for the Request (if it exists)
            script = Script.objects.get(request=req)
            script.add_entire_script(script_dict)  # Update the script_data field
        except Script.DoesNotExist:
            # If the Script object doesn't exist, create a new one
            script = Script.objects.create(request=req)
            script.add_entire_script(script_dict)
        return Response({'message': 'Request created successfully', 'script': script_dict, 'reqid': req.id})


class ScriptView(View):

    @staticmethod
    @api_view(['GET'])
    def get_script(request):
        req_id = request.query_params.get('reqid')
        try:
            req = Request.objects.get(id=req_id)
            try:
                script = Script.objects.get(request=req)
                current_script = script.get_current_script()
                return Response({'message': 'Script retrieved successfully', 'script': current_script})
            except Script.DoesNotExist:
                return Response({'message': 'Script not found'}, status=status.HTTP_404_NOT_FOUND)
        except Request.DoesNotExist:
            return Response({'message': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
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
                script, created = Script.objects.get_or_create(request=req)
                
                # Update the script_data field in the Script model
                initial_script = process_image_desc(script_dict, req.topic)
                script.add_entire_script(initial_script)
                
                request_path = path_to_request(req)
                generate_initial_assets(req, script.current_scenes, request_path)

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


class ImageGenerationView(View):
    @staticmethod
    @api_view(['GET'])
    def generate_image(request):
        try:
            reqid = request.GET.get('reqid')
            sceneid = request.GET.get('sceneid')
            prompt = request.GET.get('prompt')
            service = request.GET.get('service')

            request = Request.objects.get(id=reqid)
            scene = Scene.objects.get(id=sceneid)
            request_path = path_to_request(request)

            img_url = generate_additional_image(prompt, service, scene, request_path, request)
            cloudfront_url = cdn_path(img_url)

            response_data = {
                'message': 'Image generated successfully',
                'cloudfront_url': cloudfront_url,
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as ve:
            return Response({'error': str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Scene.DoesNotExist:
            return Response({'error': 'Scene not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProjectDownloadView(View):
    @staticmethod
    @api_view(["GET"])    
    def download_project(request):
        try:
            req_id = request.query_params.get('reqid')
            req = Request.objects.get(id=req_id)
            if req.final_video_asset:
                return Response({'final_video': cdn_path(req.final_video_asset)})
            script = Script.objects.get(request=req)
            request_path = path_to_request(req)
            cdn_url = generate_final_video(script.current_scenes, request_path, req)
            return Response({'final_video': cdn_url})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VideoFilesView(View):
    @staticmethod
    @api_view(['GET'])
    def get_video_files(request):
        try:
            req_id = request.query_params.get('reqid')
            req = Request.objects.get(id=req_id)
            script = Script.objects.get(request=req)
            scene_lists = script.current_scenes
            asset_urls = []

            for i, scene in enumerate(scene_lists):
                try:
                    scene_obj = Scene.objects.get(id=scene)
                    project_asset = ProjectAssets.objects.get(scene_id=scene_obj).currently_used_asset
                    intermediate_video = project_asset.get('intermediate_video')

                    if intermediate_video:
                        cloudfront_url = cdn_path(intermediate_video)
                        asset_urls.append([i, scene, cloudfront_url])
                    else:
                        asset_urls.append([i, scene, cloudfront_url])
                except ObjectDoesNotExist:
                    asset_urls.append(None)
            return Response({'asset_urls': asset_urls})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class URLUpdateView(View):
    @staticmethod
    @api_view(['GET'])
    def update_url(request):
        try:
            if request.query_params.get('reqid'):
                return update_url_by_reqid(request)

            elif request.query_params.get('sceneid') and request.query_params.get('category'):
                return update_url_by_sceneid_and_category(request)

            return Response({'error': 'Invalid parameters'}, status=status.HTTP_400_BAD_REQUEST)

        except (Scene.DoesNotExist, ProjectAssets.DoesNotExist) as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VoiceSamplesView(View):
    @staticmethod
    @api_view(["GET"])
    def voice_samples(request):
        voice_samples = get_voice_samples()  # Assuming you have the logic to populate the voice_samples dictionary
        serialized_voice_samples = {}
        for audio_name, audio_data in voice_samples.items():
            base64_audio = base64.b64encode(audio_data).decode('utf-8')
            serialized_voice_samples[audio_name] = base64_audio

        return Response(serialized_voice_samples)

class UserProjectsView(View):
    @staticmethod
    @api_view(["GET"])
    def get_user_projects(request):
        fireid = request.query_params.get('fireid')
        user = User.objects.get(fireid=fireid)
        
        user_requests = Request.objects.filter(user=user).values()
        return Response(user_requests)

class ThumbnailImagesView(View):
    @staticmethod
    @api_view(['GET'])
    def get_thumbnail_images(request):
        try:
            req_id = request.query_params.get('reqid')
            req = Request.objects.get(id=req_id)
            script = Script.objects.get(request=req)
            scene_lists = script.current_scenes
            asset_urls = []
            for i, scene in enumerate(scene_lists):
                try:
                    scene_obj = Scene.objects.get(id=scene)
                    project_asset = ProjectAssets.objects.get(scene_id=scene_obj).currently_used_asset
                    image = project_asset.get('image')[0]

                    if image:
                        cloudfront_url = cdn_path(image)
                        asset_urls.append([i, scene, cloudfront_url])
                    else:
                        asset_urls.append([i, scene, cloudfront_url])
                except ObjectDoesNotExist:
                    asset_urls.append(None)
            return Response({'asset_urls': asset_urls})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    