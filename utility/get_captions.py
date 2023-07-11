import json
import requests
import subprocess
import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment
from moviepy.config import change_settings
import os
import json

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)
    return r.recognize_google(audio)


def align_audio_with_gentle(audio_file, text):
    # Specify the path to the ImageMagick binary
    change_settings({"IMAGEMAGICK_BINARY": "/opt/homebrew/bin/convert"})

    with open("temp_text.txt", "w") as f:
        f.write(text)
    subprocess.run(["ffmpeg", "-i", audio_file, "temp_audio.wav"])
    url = 'http://localhost:8765/transcriptions?async=false'
    with open("temp_audio.wav", 'rb') as audio:
        r = requests.post(url, files={'audio': audio, 'transcript': open("temp_text.txt", 'rt')})
    os.remove("temp_audio.wav")
    return json.loads(r.text)


def generate_captions(video_file, audio_file):
    # text = transcribe_audio(audio_file)
    text = "Welcome to today's video, where we'll explore 15 psychological facts that will blow your mind. Let's dive right in!"
    alignment = align_audio_with_gentle(audio_file, text)
    print(alignment)
    video = VideoFileClip(video_file)
    subtitles = []

    # Specify the font name and URL
    font_url = "./KOMIKAX_.ttf"

    for word in alignment['words']:
        if 'start' in word and 'end' in word:
            start_time = word['start']
            end_time = word['end']

            outline_clip = TextClip(word['word'], fontsize=24, font=font_url, color='black', stroke_color='black', stroke_width=3)

            text_clip = TextClip(word['word'], fontsize=28,  font=font_url, color='white', bg_color='transparent')
            text_width = text_clip.w

            final_clip = CompositeVideoClip([outline_clip.set_position((1, 1)), text_clip.set_position((3, 3))], size=(text_width + 10, text_clip.h + 10))
            final_clip = final_clip.set_start(start_time).set_end(end_time).set_position(('center', video.size[1]-50))

            subtitles.append(final_clip)

    final_video = CompositeVideoClip([video] + subtitles)
    final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    video_file = "./sample_video.mp4"
    audio_file = "./sample_audio.wav"

    generate_captions(video_file, audio_file)
