from moviepy.editor import VideoFileClip, concatenate_videoclips
from celery import shared_task, current_task
from celery.utils.log import get_task_logger
from elevenlabs.api.error import APIError
from utility.text_to_image import convert_to_image
from utility.text_to_audio import convert_to_audio
from utility.sender import Sender
from utility.create_video import create_vid
from utility.generate_caption import generate_captions
from videogenerator.models import PendingTask
import os
import json
from videogenerator.models import Request
from time import sleep
from utility.aws_connector import *
from tempfile import NamedTemporaryFile
from time import time, sleep

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
        prompt = prompt.lower().strip()
        # prompt = re.sub(r"[^a-zA-Z0-9\s]+", "", prompt).strip()

        # try to create a task
        PendingTask.create_pending_task(request, prompt, image_folder)
        
        # todo: check if PendingTask attempt was successful if not then retry sent_request until success

        # Perform the actual image processing only when PendingTask attempt above is successful and return the result
        convert_to_image(sender, prompt)
        i = 0
        while PendingTask.objects.filter(request=request, prompt=prompt, folder=image_folder).exists():
            i+=1
            if i%2==0:
                i=0
                convert_to_image(sender, prompt)
            sleep(300)
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

@shared_task(name='captionated_video', retry_backoff=1.1, serializer='json', queue='video_generator_queue')
def captionated_video(assets, narration, imv_path):
    image = None
    image_live = None
    video = None
    audio = None
    
    for k, v in assets.items():
        if k == 'audio':
            while not check_file_exists(v):
                sleep(60)
                continue 
            audio = get_file_from_s3(v)
        if k == 'image':
            start = time()
            while not check_file_exists(v):
                sleep(60)
                if time() - start > 2400:
                    break
                continue
            image = get_file_from_s3(v) if check_file_exists(v) else None
        if image == None:
            return
    
    # Create temporary audio and image files
    with NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
        temp_audio_file.write(audio)
        temp_audio_file_path = temp_audio_file.name
    
    with NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
        temp_image_file.write(image)
        temp_image_file_path = temp_image_file.name
    
    try:
        if image and audio and not image_live:
            image_live = create_vid(temp_audio_file_path, temp_image_file_path)
        
        imv_scene = generate_captions(image_live, temp_audio_file_path, narration)
        upload_file_to_s3(imv_scene,imv_path)
        # Upload the final scene and other files to S3
        
        # Clean up temporary files
        os.remove(temp_audio_file_path)
        os.remove(temp_image_file_path)
    
    except Exception as e:
        # Clean up temporary files in case of an exception
        if os.path.exists(temp_audio_file_path):
            os.remove(temp_audio_file_path)
        if os.path.exists(temp_image_file_path):
            os.remove(temp_image_file_path)
        raise e

        # if k == 'video' and not video:
        #     while not check_file_exists(v):
        #         continue
        #     video = get_file_from_s3(v)
    
@shared_task(name='download_project', retry_backoff=1.1, serializer='json', queue='video_generator_queue')
def generate_final_project(assets, video_folder):
    clips = []
    for url in assets:
        while not check_file_exists(url):
            continue
        file_data = get_file_from_s3(url)
        if file_data:
            # Save to a temporary file
            temp_file = NamedTemporaryFile(delete=False, suffix='.mp4')
            temp_file.write(file_data)
            temp_file.close()

            clips.append(VideoFileClip(temp_file.name))

            # After processing, remove the temporary file
            os.remove(temp_file.name)

    if clips:
        final_clip = concatenate_videoclips(clips)

        # Save the final_clip to a temporary file
        output_temp_file = NamedTemporaryFile(delete=False, suffix='.mp4')
        final_clip.write_videofile(output_temp_file.name)

        # Read the final_clip from the temporary file
        with open(output_temp_file.name, 'rb') as f:
            final_clip_data = f.read()

        # Upload to S3
        upload_file_to_s3(final_clip_data, video_folder)

        # Remove the temporary output file
        os.remove(output_temp_file.name)