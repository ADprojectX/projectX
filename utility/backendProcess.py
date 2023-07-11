from utility import openai_request as osr, text_processing as tp, text_to_audio as tta, text_to_image as tti
import os
from utility.sender import Sender
import json
from django.http import HttpResponse
from utility.script import temp_script

OBJECT_STORE = '/Users/ad_demon/Documents/GitHub/projectX/OBJECT_STORE'

def process_request(request, user_id, request_id):

    # folder creation
    user_folder = OBJECT_STORE + "/" + str(user_id)
    None if os.path.exists(user_folder) else os.makedirs(user_folder)
    request_folder = user_folder + "/" + str(request_id)
    None if os.path.exists(request_folder) else os.makedirs(request_folder)

    topic = request.data.get('topic')
    # voice = request.data.get('voice')

    # processed_topic = tp.process_input(topic)  # request str process(text)
    # script_response = osr.request_script(processed_topic) #openai request for script
    scene_dic = tp.script_processing(temp_script)  # dictionary generatin for narration and img desc
    return scene_dic
    # narration_dic = {}
    # img_desc_dic = {}
    
    # sender = Sender(request_id)

    # for k, v in scene_dic.items():
        # calling audio conversion and img coversion and storing into above dictionaries
        # narration_dic[k] = tta.convert_to_audio(request_folder, k, v[0], 0)# voice)
        # img_desc_dic[k] = tti.convert_to_image(request_folder, sender, v[1])
    # return HttpResponse("Request processed successfully!")