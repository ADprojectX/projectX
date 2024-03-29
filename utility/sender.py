import requests
import json
from dotenv import load_dotenv
import os
import base64
from utility.aws_connector import upload_file_to_s3

def refresh_env(key):
    load_dotenv(override = True)
    return os.getenv(key)

sdxl_text_to_image_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"

class SenderEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.__dict__

class Sender:
    def __init__(self, rid):
        # self.params = params
        self.rid = rid

    def to_json(self):
        # Serialize the Sender object to a JSON string using the custom encoder
        return json.dumps(self, cls=SenderEncoder)

    def sdxl_sender_initializer(self, *args, **kwargs):
        with open("sdxl_params.json", "r") as json_file:
            params = json.load(json_file)
        self.steps = kwargs.get("steps", params.get("steps"))
        print(self.steps)
        self.width = kwargs.get("width", params.get("width"))
        self.height = kwargs.get("height", params.get("height"))
        self.seed = kwargs.get("seed", params.get("seed"))
        self.cfg_scale = kwargs.get("cfg_scale", params.get("cfg_scale"))
        self.samples = kwargs.get("samples", params.get("samples"))
            

    def sdxl_sender(self,prompt,*args, **kwargs):
        self.sdxl_sender_initializer(**kwargs)
        body = {
                "steps": self.steps,
                "width": self.width,
                "height": self.height,
                "seed": self.seed,
                "cfg_scale": self.cfg_scale,
                "samples": self.samples,
                "text_prompts": [
                    {
                    "text": prompt,
                    "weight": 1
                    },
                    {
                    "text": "blurry, bad",
                    "weight": -1
                    }
                    ],
                }
        headers = {
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                    "Authorization": refresh_env("SDXL_API_KEY"),
                    }
        response = requests.post(
                                sdxl_text_to_image_url,
                                headers=headers,
                                json=body,
                                )
        if response.status_code != 200:
            raise Exception("Non-200 response: " + str(response.text))

        data = response.json()
        return data
        

    def discord_sender_initializer(self):
        with open("sender_params.json", "r") as json_file:
            params = json.load(json_file)

        self.channelid = params["channelid"]
        self.authorization = params["authorization"]
        self.application_id = params["application_id"]
        self.guild_id = params["guild_id"]
        self.session_id = params["session_id"]
        self.version = params["version"]
        self.id = params["id"]
        self.flags = params["flags"]


    def discord_sender(self, prompt):
        self.discord_sender_initializer()
        header = {"authorization": self.authorization}

        # prompt = prompt.replace("_", " ")
        # prompt = " ".join(prompt.split())
        # prompt = re.sub(r"[^a-zA-Z0-9\s]+", "", prompt).strip()
        # prompt = prompt.lower()

        payload = {
            "type": 2,
            "application_id": self.application_id,
            "guild_id": self.guild_id,
            "channel_id": self.channelid,
            "session_id": self.session_id,
            "data": {
                "version": self.version,
                "id": self.id,
                "name": "imagine",
                "type": 1,
                "options": [
                    {
                        "type": 3,
                        "name": "prompt",
                        "value": str(prompt)# + " " + self.flags,
                    }
                ],
                "attachments": [],
            },
        }

        r = requests.post(
            "https://discord.com/api/v9/interactions", json=payload, headers=header
        )
        while r.status_code != 204:
            print("trying")
            r = requests.post(
                "https://discord.com/api/v9/interactions", json=payload, headers=header
            )

        print("prompt [{}] successfully sent!".format(prompt))
        return prompt
    
# sender = Sender(50)
# sender.send('a good man')
# json <bound method Response.json of <Response [204]>>
# text
# content b''
# body b'{"type": 2, "application_id": "936929561302675456", "guild_id": "1102068352366690336", "channel_id": "1102068352932909158",
# "session_id": "955fa3205f5306c1bd19317a9078040d", "data": {"version": "1077969938624553050", "id": "938956540159881230", "name": "imagine",
#  "type": 1, "options": [{"type": 3, "name": "prompt", "value": "a brain with gears turning inside --v 5"}], "attachments": []}}'
        # self.channelid = "1102068352932909158"#params["channelid"]
        # self.authorization = "NzA5NzE3NjEwNTMwMzQwODk1.Gadpmg.RJt3txgm9406TB5MOLC-WVr-2ha97sEi6D56V0"#params["authorization"]
        # self.application_id = "936929561302675456" #params["application_id"]
        # self.guild_id = "1102068352366690336" #params["guild_id"]
        # self.session_id = "0c5f26dc31f7c3f9f4683d1553817627"#params["session_id"]
        # self.version = "1118961510123847772" #params["version"]
        # self.id ="938956540159881230" #params["id"]
        # self.flags = "--v 5"#params["flags"]
