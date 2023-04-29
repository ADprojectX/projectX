from elevenlabs import generate, play

audio = generate("Hi! I'm the world's most advanced text-to-speech system, made by elevenlabs.")
# print(type(audio))

play(audio)


# import requests
# import os
# from dotenv import load_dotenv

# url = "https://api.elevenlabs.io/v1/voices"
# dotenv_path = os.path.join(os.getcwd(), '.env')
# load_dotenv(dotenv_path)
# XI_API_KEY = os.getenv('XI_SECRET_KEY')

# headers = {
#   "Accept": "application/json",
#   "xi-api-key": XI_API_KEY
# }

# response = requests.get(url, headers=headers)

# print(response.text)
