from celery import shared_task, current_task
from celery.utils.log import get_task_logger
from elevenlabs.api.error import APIError
from utility.text_to_image import convert_to_image
from utility.text_to_audio import convert_to_audio
from utility.sender import Sender
from utility.create_video import create_vid
from utility.generate_caption import generate_captions
from videogenerator.models import PendingTask
import re
import json
from videogenerator.models import Request
from time import sleep
from utility.aws_connector import *
from tempfile import NamedTemporaryFile

# retry_backoff should be a random and different integer for each instance to avoid eventual conflict
logger = get_task_logger(__name__)
@shared_task(name='sent_image_request', retry_backoff=0.5, serializer='json', queue='image_queue')
def sent_image_request(image_folder, sender_json, prompt, request_id):
    try:
        # Check if the buffer has less than 12 entries before proceeding
        while not PendingTask.has_less_than_buffer_entries():
            sleep(5)  # Wait for 5 seconds before checking again
        request = Request.objects.get(id=request_id)
        # Deserialize the Sender JSON back to a Sender object
        sender = Sender(**json.loads(sender_json))
        prompt = prompt.lower()
        prompt = re.sub(r"[^a-zA-Z0-9\s]+", "", prompt).strip()

        # try to create a task
        PendingTask.create_pending_task(request, prompt, image_folder)
        
        # todo: check if PendingTask attempt was successful if not then retry sent_request until success

        # Perform the actual image processing only when PendingTask attempt above is successful and return the result
        convert_to_image(sender, prompt)
    except Exception as e:
        # Log the exception and retry the task if it's a retryable error
        logger.error(f"Error processing the request: {e}")
        raise sent_image_request.retry(exc=e)  # Automatically retry the task

@shared_task(name='sent_audio_request', retry_backoff=1.1, serializer='json', queue='audio_queue')
def sent_audio_request(audio_folder, narration, voice):
    try:
        convert_to_audio(audio_folder, narration, voice)
    except APIError as e:
        # Retry the task when the APIError occurs
        current_task.retry(exc=e)

# @shared_task(name='captionated_video', retry_backoff=1.1, serializer='json', queue='video_generator_queue')
def captionated_video(assets, narration, imv_path):
    image = None
    image_live = None
    video = None
    audio = None
    for k,v in assets.items():
        if k == 'audio':
            while not check_file_exists(v):
                print('here')
                print(v)
                continue
            audio = get_file_from_s3(v)
        if k == 'image':
            print('here')
            print(v)
            while not check_file_exists(v):
                continue
            image = get_file_from_s3(v)
    with NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        temp_audio_file.write(audio)
        temp_audio_file_path = temp_audio_file.name
    with NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
        temp_image_file.write(image)
        temp_image_file_path = temp_image_file.name
    if image and audio and not image_live:
        image_live = create_vid(temp_audio_file_path, temp_image_file_path)
    imv_scene = generate_captions(image_live, temp_audio_file_path, narration)
    upload_file_to_s3(imv_scene,imv_path)
        # if k == 'video' and not video:
        #     while not check_file_exists(v):
        #         continue
        #     video = get_file_from_s3(v)
    
    
    
        
        