from elevenlabs import generate, voices, set_api_key
from elevenlabs.api.error import APIError
from celery import current_task
import os
from dotenv import load_dotenv
from utility.aws_connector import *

VOICE_KEY = "{}"#"voice#{}"
voice_folder = "voice_samples"

def refresh_env_variable():
    load_dotenv(override=True)
    set_api_key(os.getenv("XI_SECRET_KEY"))
    all_voices = voices()
    return all_voices


def save_new_voice_samples():
    all_voices = refresh_env_variable()
    voice_list = {}
    existing_files = os.listdir(voice_folder)

    for voice in all_voices:
        # Check if the file already exists in the voice_samples folder
        if voice.name + ".mp3" not in existing_files:
            audio = generate(text = "Explore a world of diverse voices with our captivating voice samples.", voice = voice)
            voice_path = voice_folder + f"/{voice.name}.mp3"
            with open(voice_path, "wb") as f:
                f.write(audio)
    return voice_list


def get_voice_samples():
    all_voices = refresh_env_variable()
    voice_list={}
    for voice in all_voices:
        file_path = voice_folder + f"/{voice.name}.mp3"
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        voice_list[voice.name] = audio_data
    return voice_list

def convert_to_audio(voice_file, narration, voice_name):
    # Find the voice object based on the given voice_name
    all_voices = refresh_env_variable()
    voice = next((v for v in all_voices if v.name == voice_name), None)
    if voice is None:
        raise ValueError(f"Voice with name '{voice_name}' not found.")
    try:
        audio = generate(text=narration, voice=voice)
        upload_file_to_s3(audio, voice_file)
    except APIError as e:
        # Retry the task when the APIError occurs
        raise current_task.retry(exc=e)

# save_new_voice_samples()
# get_voice_samples()
# save_voice_samples()


# file_path = voice_folder + f"/{voice.name}.mp3"