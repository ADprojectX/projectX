import script
import openai_request as osr
import text_processing as tp
import text_to_audio as tta
import text_to_image as tti
import os
from sender import Sender
from receiver import Receiver
import json


if __name__ == '__main__':
    # topic = input()
    # voice_number = input()'

    # folder creation
    cwd = os.getcwd()
    uid = 0
    rid = 1
    user_folder = cwd+"/"+str(uid)
    None if os.path.exists(user_folder) else os.makedirs(user_folder)
    request_folder = user_folder+"/"+str(rid)
    None if os.path.exists(request_folder) else os.makedirs(request_folder)

    topic = 'Top 15 Psycological facts for men.'
    voice_number = 0

    processed_topic = tp.process_input(topic) #request str process(text)
    # script_response = osr.request_script(processed_topic) #openai reqest for script
    scene_dic = tp.script_processing(script.temp_script) #dictionary generatin for narration and img desc
    narration_dic={}
    img_desc_dic={}

    # with open('sender_params.json', 'r') as f:
    #     # load the JSON data into a dictionary
    #     params = json.load(f)
    
    sender = Sender(rid)
    # receiver = Receiver(request_folder+"/images", rid)

    
    for k,v in scene_dic.items(): #calling audio conversion and img coversion and storing into above dictionaries
        # narration_dic[k] = tta.convert_to_audio(request_folder, k, v[0], voice_number)
        img_desc_dic[k] = tti.convert_to_image(request_folder,sender, v[1])
    
