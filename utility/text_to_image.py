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

def convert_to_image(sender, prompt):
    sender.send(prompt)
    print('success_image')
# def pending(prompt, image_folder):
#     db.add_pending_tasks(prompt, image_folder)

