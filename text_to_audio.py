from elevenlabs import clone, generate, voices,set_api_key
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

set_api_key(os.getenv('XI_SECRET_KEY'))
voices = voices()
VOICE_KEY='voice#{}'

def convert_to_audio(request_folder, k, narration,voice_number):
    audio_folder = request_folder+"/audio"
    None if os.path.exists(audio_folder) else os.makedirs(audio_folder)

    audio = generate(text=narration, voice=voices[voice_number])

    formatted_voice = VOICE_KEY.format(k)#voice#scene#1
    voice_path = audio_folder+f"/{formatted_voice}.mp3"

    with open(voice_path, "wb") as f:
        f.write(audio)

    # var = os.getcwd()+VOICENUMBER
    # .saveas(var)
    # voice#0:var
    # play(audio)
    return voice_path
    # return(audio)


# # Write the bytes to a file
# with open("audio.mp3", "wb") as f:
#     f.write(audio_bytes)