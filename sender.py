import requests
import json
import time
import re
import argparse
import sys

class Sender:

    def __init__(self, rid):
        # self.params = params
        self.sender_initializer()
        self.rid = rid

    def sender_initializer(self):
        with open('sender_params.json', "r") as json_file:
            params = json.load(json_file)

        self.channelid=params['channelid']
        self.authorization=params['authorization']
        self.application_id = params['application_id']
        self.guild_id = params['guild_id']
        self.session_id = params['session_id']
        self.version = params['version']
        self.id = params['id']
        self.flags = params['flags']
        
        
    def send(self, prompt):
        header = {
            'authorization': self.authorization
        }
        
        prompt = prompt.replace('_', ' ')
        prompt = " ".join(prompt.split())
        prompt = re.sub(r'[^a-zA-Z0-9\s]+', '', prompt).strip()
        # prompt = prompt.lower()
        print(prompt, 'sender.py')

        payload = {'type': 2, 
        'application_id': self.application_id,
        'guild_id': self.guild_id,
        'channel_id': self.channelid,
        'session_id': self.session_id,
        'data': {
            'version': self.version,
            'id': self.id,
            'name': 'imagine',
            'type': 1,
            'options': [{'type': 3, 'name': 'prompt', 'value': str(prompt) + ' ' + self.flags}],
            'attachments': []}
            }
        
        r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)
        while r.status_code != 204:
            print('trying')
            r = requests.post('https://discord.com/api/v9/interactions', json = payload , headers = header)

        print('prompt [{}] successfully sent!'.format(prompt))
        return prompt
        




# json <bound method Response.json of <Response [204]>>
# text 
# content b''
# body b'{"type": 2, "application_id": "936929561302675456", "guild_id": "1102068352366690336", "channel_id": "1102068352932909158", 
# "session_id": "955fa3205f5306c1bd19317a9078040d", "data": {"version": "1077969938624553050", "id": "938956540159881230", "name": "imagine",
#  "type": 1, "options": [{"type": 3, "name": "prompt", "value": "a brain with gears turning inside --v 5"}], "attachments": []}}'














# def parse_args(args):
    
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--params',        help='Path to discord authorization and channel parameters', required=True)
#     parser.add_argument('--prompt',           help='prompt to generate', required=True)
        
#     return parser.parse_args(args)


# if __name__ == "__main__":

#     args = sys.argv[1:]
#     args = parse_args(args)
#     params = args.params
#     prompt = args.prompt

#     sender = Sender(params)
#     sender.send(prompt)