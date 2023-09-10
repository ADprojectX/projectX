from moviepy.editor import *
import tempfile
# sys.path.append(os.path.join(os.getcwd()))#('/Users/ad_demon/Documents/GitHub/projectX/captions')
from captions.align2 import align_audio_text
import os

dir_path = os.path.join(os.getcwd(),'temp')

# Check if the directory exists
if not os.path.exists(dir_path):
    try:
        # Create the directory
        os.makedirs(dir_path)
        print(f"Directory '{dir_path}' created successfully.")
    except OSError as e:
        print(f"Error creating directory '{dir_path}': {e}")
else:
    print(f"Directory '{dir_path}' already exists.")

# FLAG FOR SWITCHING OFF CAPTIONS IF USER SELECTS HIDE CAPTION FOR PARTICULAR SCENE
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

            # Create a TextClip object with a thick stroke for the outline
            outline_clip = TextClip(word['word'], fontsize=24, font=font_url, color='black', stroke_color='black', stroke_width=3)

            # Create a TextClip object with the regular text color
            text_clip = TextClip(word['word'], fontsize=28,  font=font_url, color='white', bg_color='transparent')
            text_width = text_clip.w
            final_clip = CompositeVideoClip([outline_clip.set_position((1, 1)), text_clip.set_position((3, 3))], size=(text_width + 10, text_clip.h + 10))
            final_clip = final_clip.set_start(start_time).set_end(end_time).set_position(('center', video.size[1]-50))
            subtitles.append(final_clip)

    final_video = CompositeVideoClip([video] + subtitles)
    # Create a temporary file to store the video output
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False, dir=dir_path) as temp_video_file:
        temp_video_path = temp_video_file.name
        final_video.write_videofile(temp_video_path, codec='libx264')

    # Read the temporary video file as bytes-like object
    with open(temp_video_path, 'rb') as temp_file:
        video_data = temp_file.read()

    print("Returning from generate captions")
    return video_data