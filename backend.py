# import openai_secret_manager
import requests
import os
from dotenv import load_dotenv
import openai
import script

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
def request_script(text):    
    openai.api_key = os.getenv('OPENAI_SECRET_KEY')
    response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                            {"role": "system", "content": "You will act as a youtube expert who will generate a script perfectly for the topic given"},
                            {"role": "user", "content": text},
                            ],
                    max_tokens=15,
                )
                
    answer = response['choices'][0]['message']['content']

    print(f"The script for given topic is \n \n '{answer}'.")
    return answer

def process_input(topic):
    TEMPLATE = "Generate a script for youtube video on {}."
    output = TEMPLATE.format(topic)
    return output

def script_processing(temp_script):
    processed_script = temp_script.split("\n")
    new_list = []
    script_desc={}

    for i in processed_script:
        if i==" " or not i:
            continue
        new_list.append(i)
    # print(new_list)
    SCENE='scene#{}'
    i=0
    while i<len(new_list):
        ts = SCENE.format(i//2)
        script_desc[ts] = [new_list[i][11:-1]]
        i+=1
        script_desc[ts].append(new_list[i][20:-1])
        i+=1
    print(script_desc)
    # i=0
    # while i<new_list
    # narration_dict = {}
    # image_desc_dict = {}

# dict {1 : [narrtor, imagedescr]}

if __name__ == '__main__':
    # topic = input()
    topic = 'Top 15 Psycological facts for men.'
    processed_topic = process_input(topic)
    script_processing(script.temp_script)
    # script_response = request_script(processed_topic)
    
    
    # for ()