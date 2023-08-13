from utility import openai_request as osr, text_processing as tp, text_to_audio as tta, text_to_image as tti
import os
from utility.sender import Sender
from utility.script import temp_script
from concurrent.futures import ThreadPoolExecutor, wait
from utility.script import img_desc
import time
from videogenerator.serializers import RequestSerializer, ProjectAssetsSerializer
from videogenerator.models import ProjectAssets, Scene
from utility.tasks import sent_image_request, sent_audio_request, captionated_video


# The number of simultaneous requests allowed by the buffer
IMAGE_BUFFER_SIZE = 13

# OBJECT_STORE = os.path.join(os.getcwd(), "OBJECT_STORE")

def process_scenes(request):
    topic = request.data.get('topic')
    # processed_topic = tp.process_input(topic)  # request str process(text)
    # script_response = osr.request_script(processed_topic) #openai request for script
    scene_dic = tp.script_processing(temp_script)  # dictionary generating for narration and img desc
    return scene_dic

def process_image_desc(script):

    ######################temporary#################################
    # Split the string based on new lines
    img_desc_list = img_desc.split('\n')
    # Remove the "Image Description: " prefix from each string
    img_desc_list = [desc.replace('Image Description: ', '') for desc in img_desc_list]
    for i, uuid, scene in script:

        # i = int(i)
        # script[int(i)] = int(i)
        script[i].append(img_desc_list[i])
        
        # if len(script[i])<4:
        # else:
        #     script[i][3]=img_desc_list[i]
    ######################temporary#################################
    
    # for scene,narration in script.items():
    #     script[scene].append(osr.request_image_descriptions(narration[0]))
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
    
def generate_initial_assets(request, script, path, img_service, *args, **kwargs):
    sender = Sender(str(request.id))
    sender_json = sender.to_json()
    image_asset = path_to_asset('image',img_service)
    voice_asset = path_to_asset('audio','XIL')
    im_video_asset = path_to_asset('intermediate_video', f"{img_service}_XIL")
    image_folder = path + f"{'/'+ image_asset if image_asset else None}"  #f"/image/{img_type}"
    audio_folder = path + f"{'/'+ voice_asset if voice_asset else None}"  #f"/audio/{voice_folder}" 
    im_video_folder = path + f"{'/'+ im_video_asset if im_video_asset else None}"
    # asset_list = []
    for scene_id in script:
        scene = Scene.objects.get(id = scene_id)
        asset, _ = ProjectAssets.objects.update_or_create(scene_id=scene)
        image_file = image_folder + f"/{scene_id}"#/{scene.image_desc.replace(' ', '_').lower()}.jpg"
        # audio_file = audio_folder + f"/{v[0].repl}"
        # formatted_voice = f"{voice_folder}/{k}" #VOICE_KEY.format(k)
        voice_file = audio_folder + f"/{scene_id}/{request.voice}/0.mp3"
        im_video_file = im_video_folder + f"/{scene_id}/option1_{request.voice}.mp4"
        
        # print(image_file, voice_file)
        asset.add_new_asset(image = image_file, audio = voice_file, intermediate_video = im_video_file)
        # # asset_list.append([image_file, voice_file])
        # # add celery chain
        sent_image_request.delay(image_file, sender_json, scene.image_desc, request.id)
        sent_audio_request.delay(voice_file, scene.narration, request.voice if request.voice else 'Adam')
        captionated_video.delay({"image":image_file+f"/option1_{scene.image_desc.replace(' ', '_').lower()}.jpg", "audio":voice_file}, scene.narration, im_video_file)
    # serializer = ProjectAssetsSerializer(instance=asset)
    # serialized_data = serializer.data

def get_current_images(request):
    pass

