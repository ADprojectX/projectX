from utility import openai_request as osr, text_processing as tp, text_to_audio as tta, text_to_image as tti
import os
from utility.sender import Sender
import uuid
from videogenerator.models import ProjectAssets, Scene, Request
from utility.tasks import sent_mj_image_request, sent_audio_request, captionated_video, generate_final_project, sent_sdxl_image_request
from utility.aws_connector import cdn_path, check_file_exists, is_s3_directory_empty
from django.core import serializers
from rest_framework.response import Response

def process_scenes(request):
    topic = request.data.get('topic')
    processed_topic = tp.process_input(topic)  # request str process(text)
    script_response = osr.request_script(processed_topic) #openai request for script
    scene_dic = tp.script_processing(script_response)#(temp_script)  # dictionary generating for narration and img desc
    return scene_dic

def process_image_desc(script, topic):
    for index, scene, narration in script:
        script[index].append(osr.request_image_descriptions(narration, topic))
    return script
    
def path_to_request(request):
    user_folder = f"OBJECT_STORE/{str(request.user.id)}" #AWS_OBJECT_STORE + "/" + str(request.user.id)
    None if os.path.exists(user_folder) else os.makedirs(user_folder)
    request_folder = user_folder + "/" + str(request.id)
    None if os.path.exists(request_folder) else os.makedirs(request_folder)
    return request_folder

def path_to_asset(*args, **kwargs):
    sub_path = ''
    for arg in args:
        sub_path+=arg+'/'
    return sub_path[:-1] if sub_path else None
    
def generate_initial_assets(request, script, path, img_service='sdxl', *args, **kwargs):
    image_asset = path_to_asset('image',img_service)
    voice_asset = path_to_asset('audio','XIL')
    im_video_asset = path_to_asset('intermediate_video', f"{img_service}_XIL")
    image_folder = path + f"{'/'+ image_asset if image_asset else None}" 
    audio_folder = path + f"{'/'+ voice_asset if voice_asset else None}"
    im_video_folder = path + f"{'/'+ im_video_asset if im_video_asset else None}"
    
    for scene_id in script:
        img_id = str(uuid.uuid4())
        sender = Sender(str(img_id))
        sender_json = sender.to_json()
        scene = Scene.objects.get(id = scene_id)
        asset, _ = ProjectAssets.objects.update_or_create(scene_id=scene)
        image_file = image_folder + f"/{scene_id}/{img_id}"#/{scene.image_desc.replace(' ', '_').lower()}.jpg"
        voice_file = audio_folder + f"/{scene_id}/{request.voice}/0.mp3"
        im_video_file = im_video_folder + f"/{scene_id}/{img_id}_{request.voice}.mp4"
        
        # # add celery chain
        if img_service == 'mjx':
            asset.add_new_asset(image = [image_file+f"_option1.jpg", scene.image_desc], audio = voice_file, intermediate_video = im_video_file)
            sent_mj_image_request.delay(image_file, sender_json, scene.image_desc, request.id)
            image_file = image_file+f"_option1.jpg"
        else:
            # Serialize the Scene object
            image_file = image_file+".jpg"
            asset.add_new_asset(image = [image_file, scene.image_desc], audio = voice_file, intermediate_video = im_video_file)
            serialized_scene = serializers.serialize("json", [scene])
            sent_sdxl_image_request.delay(image_file, sender_json, scene.image_desc, serialized_scene)

        sent_audio_request.delay(voice_file, scene.narration, request.voice if request.voice else 'Adam')
        
        captionated_video.delay({"image":image_file, "audio":voice_file}, scene.narration, im_video_file)

def generate_additional_image(prompt, img_service, scene, path, request):
    image_asset = path_to_asset('image',img_service)
    image_folder = path + f"{'/'+ image_asset if image_asset else None}" 
    img_id = str(uuid.uuid4())
    sender = Sender(str(img_id))
    sender_json = sender.to_json()
    image_file = image_folder + f"/{scene.id}/{img_id}"
    asset, _ = ProjectAssets.objects.update_or_create(scene_id=scene)
    
    if img_service == 'sdxl':
        image_file = image_file+".jpg"
        asset.add_asset(image = [image_file, scene.image_desc])
        serialized_scene = serializers.serialize("json", [scene])
        sent_sdxl_image_request.delay(image_file, sender_json, prompt, serialized_scene)
    elif img_service == 'mjx':
        #check if extras have other images available
        # if is_s3_directory_empty(image_folder+f"/{scene.id}/extras/"):
            # asset.add_asset(image = image_file+f"_option1.jpg")
            # sent_mj_image_request.delay(image_file, sender_json, scene.image_desc, reqid)
            # pass
        asset.add_asset(image = [image_file+f"_option1.jpg", scene.image_desc])
        sent_mj_image_request.delay(image_file, sender_json, prompt, request.id)

    return

def generate_final_video(script, request_path, req):
    video_assets = []
    for scene_id in script:
        scene_obj = Scene.objects.get(id=scene_id)
        project_asset = ProjectAssets.objects.get(scene_id=scene_obj).currently_used_asset
        intermediate_video = project_asset.get('intermediate_video')
        video_assets.append(intermediate_video)
    project_path = request_path+f"/final_video/{req.id}.mp4"
    req.final_video_asset = project_path
    req.save()
    generate_final_project.delay(video_assets, project_path)
    return cdn_path(project_path)

def update_url_by_reqid(request):
    reqid = request.query_params.get('reqid')
    req = Request.objects.get(id=reqid)
    asset = req.final_video_asset
    cloudfront_url = cdn_path(asset)
    return Response({'cloudfront_url': cloudfront_url})

def update_url_by_sceneid_and_category(request):
    scene_id = request.query_params.get('sceneid')
    category = request.query_params.get('category')

    scene_obj = Scene.objects.get(id=scene_id)
    project_asset = ProjectAssets.objects.get(scene_id=scene_obj).currently_used_asset
    asset = project_asset.get(category)

    if asset:
        cloudfront_url = cdn_path(asset)
        return Response({'cloudfront_url': cloudfront_url})
    else:
        return Response({'error': 'Asset not found'}, status=404)
