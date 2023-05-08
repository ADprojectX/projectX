from elevenlabs import clone, generate, voices, set_api_key
import os
from dotenv import load_dotenv

load_dotenv()

set_api_key(os.getenv("XI_SECRET_KEY"))
voices = voices()
VOICE_KEY = "voice#{}"


def convert_to_audio(request_folder, k, narration, voice_number):
    audio_folder = request_folder + "/audio"
    None if os.path.exists(audio_folder) else os.makedirs(audio_folder)

    audio = generate(text=narration, voice=voices[voice_number])

    formatted_voice = VOICE_KEY.format(k) 
    voice_path = audio_folder + f"/{formatted_voice}.mp3"

    with open(voice_path, "wb") as f:
        f.write(audio)

    return voice_path

