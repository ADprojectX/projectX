from elevenlabs import clone, generate, voices,set_api_key
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

set_api_key(os.getenv('XI_SECRET_KEY'))


voices = voices()

def convert_to_audio(narration,voice_number):
    audio = generate(text=narration, voice=voices[voice_number])
    # play(audio)
    return(audio)