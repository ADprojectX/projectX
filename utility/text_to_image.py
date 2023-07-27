# from dis_bot import pending
import os
from utility import database as db
import re
from videogenerator.models import PendingTask

# def pending(prompt, image_folder):
#     db.add_pending_tasks(prompt, image_folder)


def convert_to_image(request_folder, sender, prompt, request):
    image_folder = request_folder + "/image"
    None if os.path.exists(image_folder) else os.makedirs(image_folder)
    r = sender.send(prompt)
    prompt = prompt.lower()
    prompt = re.sub(r"[^a-zA-Z0-9\s]+", "", prompt).strip()
    print(prompt, 'jere')
    PendingTask.objects.create(request=request, prompt=prompt, folder=image_folder)
    # pending(prompt, image_folder)
    return image_folder
    
