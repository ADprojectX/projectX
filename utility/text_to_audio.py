from elevenlabs import clone, generate, voices, set_api_key
from elevenlabs.api.error import APIError
from celery import shared_task, current_task
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import NoCredentialsError
from io import BytesIO
from utility.aws_connector import *
# load_dotenv()
set_api_key(os.getenv("XI_SECRET_KEY"))
voices = voices()
VOICE_KEY = "{}"#"voice#{}"
voice_folder = "voice_samples"
# ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
# SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_BUCKET = os.getenv('AWS_BUCKET_STORE')#.split("//")[1].split("/")[0]
# print(AWS_BUCKET)

def save_new_voice_samples():
    voice_list = {}
    existing_files = os.listdir(voice_folder)

    for voice in voices:
        file_path = voice_folder + f"/{voice.name}.mp3"

        # Check if the file already exists in the voice_samples folder
        if voice.name + ".mp3" not in existing_files:
            audio = generate(text = "Explore a world of diverse voices with our captivating voice samples.", voice = voice)
            voice_path = voice_folder + f"/{voice.name}.mp3"
            with open(voice_path, "wb") as f:
                f.write(audio)

    return voice_list

def get_voice_samples():
    voice_list={}
    for voice in voices:
        file_path = voice_folder + f"/{voice.name}.mp3"
        with open(file_path, 'rb') as audio_file:
            audio_data = audio_file.read()
        voice_list[voice.name] = audio_data
    return voice_list

def save_voice_samples():
    for voice in voices:
        audio = generate(text = "Explore a world of diverse voices with our captivating voice samples.", voice = voice)
        voice_path = voice_folder + f"/{voice.name}.mp3"
        with open(voice_path, "wb") as f:
            f.write(audio)

# def upload_audio_to_s3(audio_data, file_name):
#     s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
#     try:
#         # Create a file-like object from the audio data
#         audio_file = BytesIO(audio_data)
#         # Upload the audio file-like object to S3
#         s3.upload_fileobj(audio_file, AWS_BUCKET, file_name)
#         print("Upload Successful")
#         return True
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False


def convert_to_audio(voice_file, narration, voice_name):
    # Find the voice object based on the given voice_name
    voice = next((v for v in voices if v.name == voice_name), None)
    if voice is None:
        raise ValueError(f"Voice with name '{voice_name}' not found.")
    try:
        audio = generate(text=narration, voice=voice)
        upload_file_to_s3(audio, voice_file)
    except APIError as e:
        # Retry the task when the APIError occurs
        raise current_task.retry(exc=e)
    # upload_audio_to_s3(audio, voice_file)

    # formatted_voice = VOICE_KEY.format(k) 
    # voice_path = audio_folder + f"/{formatted_voice}.mp3"

    # with open(voice_file, "wb") as f:
    #     f.write(audio)


# save_new_voice_samples()
# get_voice_samples()
# save_voice_samples()




# voices=[
# Voice(voice_id='21m00Tcm4TlvDq8ikWAM', name='Rachel', category='premade', description=None, labels={}, samples=None, 
# settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None), 
# Voice(voice_id='AZnzlk1XvdvUeBnXmlld', name='Domi', category='premade', description=None,
# labels={}, samples=None, settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None), 
# Voice(voice_id='EXAVITQu4vr4xnSDxMaL', name='Bella',category='premade', description=None, labels={}, samples=None, 
# settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None),   
# Voice(voice_id='ErXwobaYiN019PkySvjV', name='Antoni', category='premade', description=None, labels={}, samples=None, 
# settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None), 
# Voice(voice_id='MF3mGyEYCl7XYWbV9V6O', name='Elli', category='premade', description=None, labels={}, samples=None, 
# settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None), 
# Voice(voice_id='TxGEqnHWrfWFTfGW9XjX', name='Josh', category='premade', description=None, labels={}, samples=None,
# settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None),
# Voice(voice_id='VR6AewLTigWG4xSOukaG', name='Arnold', category='premade', description=None, labels={}, samples=None, settings=VoiceSettings(stability=0.5, 
# similarity_boost=0.75), design=None), 
# Voice(voice_id='pNInz6obpgDQGcFmaJgB', name='Adam', category='premade', description=None, labels={}, samples=None,
# settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None), 
# Voice(voice_id='yoZ06aMxZJJ28mfd3POQ', name='Sam', category='premade', description=None, labels={}, samples=None, 
# settings=VoiceSettings(stability=0.5, similarity_boost=0.75), design=None), 
# Voice(voice_id='2hXKQA43uu4NN8DuU4i5', name='[ElevenVoices] Indian Female Young', category='generated', description='', 
# labels={'accent': 'indian', 'age': 'young', 'voicefrom': 'ElevenVoices', 'gender': 'female'}, samples=None, 
# settings=VoiceSettings(stability=1.0, similarity_boost=1.0), design=None), 
# Voice(voice_id='mioOrhYPlB3ZCM6kCMF1', name='[ElevenVoices] Indian Male Young', category='generated', description='', 
# labels={'accent': 'indian', 'age': 'young', 'voicefrom': 'ElevenVoices', 'gender': 'male'}, samples=None, settings=VoiceSettings(stability=0.5, 
# similarity_boost=1.0), design=None)]