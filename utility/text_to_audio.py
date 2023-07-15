from elevenlabs import clone, generate, voices, set_api_key
import os
from dotenv import load_dotenv

load_dotenv()
set_api_key(os.getenv("XI_SECRET_KEY"))
voices = voices()
VOICE_KEY = "voice#{}"
voice_folder = "voice_samples"

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

    return voice_path
    # voice_samples_directory = "voice_samples"  # Directory to store the voice samples
    # os.makedirs(voice_samples_directory, exist_ok=True)

    # # voice_list = voices()
    # for i, voice in enumerate(voices):
    #     voice_name = voice.get("name")
    #     voice_url = voice.get("url")
    #     print(f"Cloning voice: {voice_name}")

    #     cloned_voice = clone(voice_url)
    #     voice_id = cloned_voice.get("id")

    #     if voice_id:
    #         print(f"Generating voice samples for: {voice_name}")

    #         # Generate the voice samples
    #         generate(voice_id, output_directory=voice_samples_directory)

    #         print(f"Voice samples generated for: {voice_name}")
    #     else:
    #         print(f"Failed to clone voice: {voice_name}")


def convert_to_audio(request_folder, k, narration, voice_number):
    audio_folder = request_folder + "/audio"
    None if os.path.exists(audio_folder) else os.makedirs(audio_folder)

    audio = generate(text=narration, voice=voices[voice_number])

    formatted_voice = VOICE_KEY.format(k) 
    voice_path = audio_folder + f"/{formatted_voice}.mp3"

    with open(voice_path, "wb") as f:
        f.write(audio)

    return voice_path

get_voice_samples()
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