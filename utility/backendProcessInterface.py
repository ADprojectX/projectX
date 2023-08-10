from utility import openai_request as osr, text_processing as tp, text_to_audio as tta, text_to_image as tti
import os
from utility.sender import Sender
from utility.script import temp_script
from concurrent.futures import ThreadPoolExecutor, wait
from utility.script import img_desc
import time
from videogenerator.serializers import RequestSerializer
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
        sub_path+arg+'/'
    return sub_path[:-1] if sub_path else None
    
def generate_initial_assets(request, script, path, img_service, *args, **kwargs):
    sender = Sender(str(request.id))
    sender_json = sender.to_json()
    image_asset = path_to_asset('image',img_service)
    voice_asset = path_to_asset('audio','XIL')
    image_folder = path + f"{'/'+ image_asset if image_asset else None}"  #f"/image/{img_type}"
    audio_folder = path + f"{'/'+ voice_asset if voice_asset else None}"  #f"/audio/{voice_folder}" 
    for scene_id in script:
        scene = Scene.objects.get(id = scene_id)
        asset, created = ProjectAssets.objects.update_or_create(scene_id=scene)
        image_file = image_folder + f"/{scene_id}/{scene.image_desc.replace(' ', '_').lower()}.jpg"
        # audio_file = audio_folder + f"/{v[0].repl}"
        # formatted_voice = f"{voice_folder}/{k}" #VOICE_KEY.format(k)
        voice_file = audio_folder + f"/{scene_id}.mp3"
        # print(image_file, voice_file)
        # asset.add_first_scene(k, image_file, voice_file)
        # add celery chain
        # sent_image_request.delay(image_folder, sender_json, v[1], request.id)
        # sent_audio_request.delay(voice_file, v[0], request.voice if request.voice else 'Adam')

    captionated_video.delay(asset)


def get_current_images(request):
    pass









   





















########################################################################################################################################################################################################################################################################
        # narration_dic[k] = tta.convert_to_audio(path, k, v[0], request.voice if request.voice else 'Romi')
        # img_desc_dic[k] = tti.convert_to_image(path, sender, v[1], request)
    # b = time.time()
    # print(f'time:{b-a}')


    # # narration_dic = {}
    # # img_desc_dic = {}
    # # Create a sender for audio processing
    # sender = Sender(request_id)
    # scene_dic = {}
    # # Process audios and images in parallel
    # with concurrent.futures.ThreadPoolExecutor(max_workers=IMAGE_BUFFER_SIZE + 1) as executor:
    #     # Process audios
    #     narration_dic = {}
    #     for k, v in scene_dic.items():
    #         narration_dic[k] = executor.submit(tta.convert_to_audio, request_folder, k, v[0], 0)

    #     # Process images
    #     image_tasks = []
    #     for k, v in scene_dic.items():
    #         image_task = executor.submit(tti.convert_to_image, request_folder, sender, v[1])
    #         image_tasks.append(image_task)

    #     # Wait for all audio and image tasks to complete
    #     concurrent.futures.wait(narration_dic.values() + image_tasks)

    #     # Retrieve results from audio tasks
    #     for k, future in narration_dic.items():
    #         narration_dic[k] = future.result()

# def process_image_with_semaphore(request_folder, sender, prompt, semaphore, request):
#     with semaphore:
#         return tti.convert_to_image(request_folder, sender, prompt, request)








    # sender = Sender(request_id)

    # for k, v in scene_dic.items():
    #     # calling audio conversion and img coversion and storing into above dictionaries
    #     # narration_dic[k] = tta.convert_to_audio(request_folder, k, v[0], 0)# voice)
    #     img_desc_dic[k] = tti.convert_to_image(request_folder, sender, v[1])
    # # return HttpResponse("Request processed successfully!")

    
    # if not os.path.exists(image_folder):
    #     try:
    #         os.makedirs(image_folder)
    #     except FileExistsError:
    #         # Handle the case when the directory is created by another process/thread
    #         pass
    # if not os.path.exists(audio_folder):
    #     try:
    #         os.makedirs(audio_folder)
    #     except FileExistsError:
    #         # Handle the case when the directory is created by another process/thread
    #         pass