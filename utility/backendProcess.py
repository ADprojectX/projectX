from utility import openai_request as osr, text_processing as tp, text_to_audio as tta, text_to_image as tti
import os
from utility.sender import Sender
from utility.script import temp_script
from concurrent.futures import ThreadPoolExecutor, wait
from utility.script import img_desc
import time
from videogenerator.serializers import RequestSerializer


# The number of simultaneous requests allowed by the buffer
IMAGE_BUFFER_SIZE = 13

OBJECT_STORE = os.path.join(os.getcwd(), "OBJECT_STORE")

def process_scenes(request):
    topic = request.data.get('topic')
    # processed_topic = tp.process_input(topic)  # request str process(text)
    # script_response = osr.request_script(processed_topic) #openai request for script
    scene_dic = tp.script_processing(temp_script)  # dictionary generatin for narration and img desc
    return scene_dic

def process_image_desc(script):

    ######################temporary#################################
    # Split the string based on new lines
    img_desc_list = img_desc.split('\n')
    # Remove the "Image Description: " prefix from each string
    img_desc_list = [desc.replace('Image Description: ', '') for desc in img_desc_list]
    for i, scene in enumerate(script.keys()):
        script[scene].append(img_desc_list[i])
    ######################temporary#################################
    
    # for scene,narration in script.items():
    #     script[scene].append(osr.request_image_descriptions(narration[0]))
    return script
    
def path_to_request(request):
    user_folder = OBJECT_STORE + "/" + str(request.user.id)
    None if os.path.exists(user_folder) else os.makedirs(user_folder)
    request_folder = user_folder + "/" + str(request.id)
    None if os.path.exists(request_folder) else os.makedirs(request_folder)
    return request_folder


# def process_image_with_semaphore(request_folder, sender, prompt, semaphore, request):
#     with semaphore:
#         return tti.convert_to_image(request_folder, sender, prompt, request)

def generate_video(request, script, path):
    sender = Sender(request.id)
    # sender_json = sender.to_json()
    # request_json = RequestSerializer(request).data

    # Process audios and images in parallel
    a = time.time()
    # Process audios
    narration_dic = {}
    img_desc_dic = {}
    for k, v in script.items():
        narration_dic[k] = tta.convert_to_audio(path, k, v[0], request.voice if request.voice else 'Romi')
        img_desc_dic[k] = tti.convert_to_image(path, sender, v[1], request)
    b = time.time()
    print(f'time:{b-a}')

   





















########################################################################################################################################################################################################################################################################
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









    # sender = Sender(request_id)

    # for k, v in scene_dic.items():
    #     # calling audio conversion and img coversion and storing into above dictionaries
    #     # narration_dic[k] = tta.convert_to_audio(request_folder, k, v[0], 0)# voice)
    #     img_desc_dic[k] = tti.convert_to_image(request_folder, sender, v[1])
    # # return HttpResponse("Request processed successfully!")