from moviepy.editor import *
import os
import json
# Set the directory path for audio and image files
directory = "OBJECT_STORE"
with open('script_desc.json', 'r') as f:
    scene_desc = json.load(f)
# Loop over all the image files in the directory
i = 0
for filename in os.listdir(f"{directory}/12/54/image"):
    if filename.endswith(".jpg") and filename.startswith("option1"):
        # Get the image file path
        image_path = os.path.join(f"{directory}/12/54/image", filename)

        # Get the corresponding audio file path
        audio_filename = f"voice#scene#{i}.mp3"
        audio_path = os.path.join(f"{directory}/12/54/audio", audio_filename)

        # Load the audio file
        audio = AudioFileClip(audio_path)
        
        # Load the image file
        image = ImageClip(image_path).set_duration(audio.duration)

        # Create a video clip with the image and audio
        filename = filename[8:-4]
        # for key, value in scene_desc.items():
        #     if value == filename.replace('_',' '):
        #         scene = key
        #         print(scene)
        # scene=''
        video = image.set_audio(audio)

        # Set the output file name
        output_filename = f"{filename.split('.')[0]}.mp4"
        None if os.path.exists(f"{directory}/12/54/output") else os.mkdir(f"{directory}/12/54/output")
        output_path = os.path.join(f"{directory}/12/54/output", output_filename)

        # Write the video file to disk
        video.write_videofile(output_path, fps=24)
        i+=1


# from moviepy.editor import *
# import os
# import numpy as np
# from moviepy.video.tools.segmenting import findObjects

# directory = os.getcwd()
# # Load the audio file
# audio = AudioFileClip(f"{directory}/0/1/audio/voice#scene#0.mp3")

# # Load the image file
# image = ImageClip(
#     f"{directory}/0/1/image/option1_a_brain_with_gears_turning_inside.jpg"
# ).set_duration(audio.duration)
# # # Create a video clip with the image and audio

# video = image.set_audio(audio)
# width, height = video.size
# screensize = (width, height)
# txtClip = TextClip(
#     "Introduction to the pysocological world",
#     color="lightgreen",
#     font="Arial",
#     kerning=5,
#     fontsize=50,
# )

# cvc = CompositeVideoClip([txtClip.set_pos("center")], size=screensize)

# rotMatrix = lambda a: np.array([[np.cos(a), np.sin(a)], [-np.sin(a), np.cos(a)]])


# def effect1(screenpos, i, nletters):

#     # damping
#     d = lambda t: 1.0 / (0.3 + t**8)
#     # angle of the movement
#     a = i * np.pi / nletters

#     # using helper function
#     v = rotMatrix(a).dot([-1, 0])

#     if i % 2:
#         v[1] = -v[1]

#     # returning the function
#     return lambda t: screenpos + 400 * d(t) * rotMatrix(0.5 * d(t) * a).dot(v)


# letters = findObjects(cvc)


# def moveLetters(letters, funcpos):

#     return [
#         letter.set_pos(funcpos(letter.screenpos, i, len(letters)))
#         for i, letter in enumerate(letters)
#     ]


# clips = [
#     CompositeVideoClip(moveLetters(letters, effect1), size=screensize).subclip(0, 5)
# ]
# final_clip = concatenate_videoclips(clips)

# final_video = CompositeVideoClip([video, final_clip])

# final_video.write_videofile(
#     f"{directory}/output_file.mp4",
#     codec="libx264",
#     fps=24,
#     audio=True,
#     audio_codec="aac",
# )
