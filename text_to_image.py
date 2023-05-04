# from dis_bot import pending
import os
import database as db
import re


def pending(prompt, image_folder):
    db.add_pending_tasks(prompt, image_folder)


def convert_to_image(request_folder, sender, prompt):
    image_folder = request_folder + "/image"
    None if os.path.exists(image_folder) else os.makedirs(image_folder)

    r = sender.send(prompt)
    prompt = prompt.lower()
    prompt = re.sub(r"[^a-zA-Z0-9\s]+", "", prompt).strip()

    pending(prompt, image_folder)
    # message_id = r.json()['id']
    # print(message_id)
    pass
