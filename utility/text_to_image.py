# from dis_bot import pending
from celery import shared_task
import os
from utility import database as db
import re
from videogenerator.models import PendingTask
from collections import deque
import time
from .sender import Sender
from videogenerator.serializers import RequestSerializer
# def pending(prompt, image_folder):
#     db.add_pending_tasks(prompt, image_folder)
pending = deque([])

class Task:
    def __init__(self, request_folder, sender, prompt, request):
        self.request_folder = request_folder
        self.sender = sender
        self.prompt = prompt
        self.request = request

@shared_task(serializer='json')
def task_assigner():
    while True:
        print('stuck')
        if len(pending) !=0 :
            while PendingTask.objects.count<13:
                time.sleep(10)
            priority = pending.pop(0)
            priority.sender.send(priority.prompt)
            prompt = priority.prompt.lower()
            prompt = re.sub(r"[^a-zA-Z0-9\s]+", "", prompt).strip()
            PendingTask.objects.create(request=priority.request, prompt=prompt, folder=priority.image_folder)

# @shared_task(serializer='json')
def convert_to_image(request_folder, sender, prompt, request):
    print('fucking sender error here')
    image_folder = request_folder + "/image"
    None if os.path.exists(image_folder) else os.makedirs(image_folder)
    sender_json = Sender.to_json(sender)
    request_json = RequestSerializer(request).data
    print('fucking sender error here2')
    task = Task(request_folder, sender_json, prompt, request_json)
    print('fucking sender error here3')
    pending.push(task)
   
    # r = sender.send(prompt)
    # print(prompt, 'jere')
    # pending(prompt, image_folder)
    return image_folder


task_assigner.delay