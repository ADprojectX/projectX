from moviepy.editor import *
import os
import numpy as np
from moviepy.editor import *
from moviepy.video.tools.segmenting import findObjects

directory = os.getcwd()
# Load the audio file
audio = AudioFileClip(f"{directory}/0/1/audio/voice#scene#0.mp3")

# Load the image file
image = ImageClip(
    f"{directory}/0/1/image/option1_a_brain_with_gears_turning_inside.jpg"
).set_duration(audio.duration)
# # Create a video clip with the image and audio

video = image.set_audio(audio)
width, height = video.size
screensize = (width, height)
txtClip = TextClip(
    "Introduction to the pysocological world",
    color="lightgreen",
    font="Arial",
    kerning=5,
    fontsize=50,
)

cvc = CompositeVideoClip([txtClip.set_pos("center")], size=screensize)

rotMatrix = lambda a: np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])


def effect1(screenpos, i, nletters):

    # damping
    d = lambda t: 1.0 / (0.3 + t**8)
    # angle of the movement
    a = i * np.pi / nletters

    # using helper function
    v = rotMatrix(a).dot([-1, 0])

    if i % 2:
        v[1] = -v[1]

    # returning the function
    return lambda t: screenpos + 400 * d(t) * rotMatrix(0.5 * d(t) * a).dot(v)


letters = findObjects(cvc)


def moveLetters(letters, funcpos):

    return [
        letter.set_pos(funcpos(letter.screenpos, i, len(letters)))
        for i, letter in enumerate(letters)
    ]


clips = [
    CompositeVideoClip(moveLetters(letters, effect1), size=screensize).subclip(0, 5)
]
final_clip = concatenate_videoclips(clips)

final_video = CompositeVideoClip([video, final_clip])

final_video.write_videofile(
    f"{directory}/output_file.mp4",
    codec="libx264",
    fps=24,
    audio=True,
    audio_codec="aac",
)
