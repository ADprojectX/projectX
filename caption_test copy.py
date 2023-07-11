import speech_recognition as sr
from moviepy.editor import *
from pydub import AudioSegment
from moviepy.config import change_settings
import sys
sys.path.append('/Users/aatishdhami/Desktop/ProjectX/latest/projectX/mygentle')
from mygentle.align2 import align_audio_text

def generate_captions(video_file, audio_file, text):
    alignment = align_audio_text(audio_file, text)
    video = VideoFileClip(video_file)
    subtitles = []

    # Specify the font name and URL
    font_url = "./KOMIKAX_.ttf"

    for word in alignment['words']:
        if 'start' in word and 'end' in word:
            start_time = word['start']
            end_time = word['end']
            # fontsize=24

            # Create a TextClip object with a thick stroke for the outline
            outline_clip = TextClip(word['word'], fontsize=24, font=font_url, color='black', stroke_color='black', stroke_width=3)

            # Create a TextClip object with the regular text color
            text_clip = TextClip(word['word'], fontsize=28,  font=font_url, color='white', bg_color='transparent')
            text_width = text_clip.w
            final_clip = CompositeVideoClip([outline_clip.set_position((1, 1)), text_clip.set_position((3, 3))], size=(text_width + 10, text_clip.h + 10))
            final_clip = final_clip.set_start(start_time).set_end(end_time).set_position(('center', video.size[1]-50))
            subtitles.append(final_clip)

    final_video = CompositeVideoClip([video] + subtitles)
    # return final_video
    final_video.write_videofile("output_video.mp4", codec="libx264", audio_codec="aac")


if __name__ == "__main__":
    video_file = "./sample_video.mp4"
    audio_file = "./sample_audio.wav"
    text = "Welcome to today's video, where we'll explore 15 psychological facts that will blow your mind. Let's dive right in!"
    output_video = generate_captions(video_file, audio_file, text)
    print(type(output_video))

