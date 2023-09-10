from moviepy.editor import *
import tempfile

def create_vid(audio, image):
    image_clip = ImageClip(image)
    audio_clip = AudioFileClip(audio)

    # Set the duration of the image clip to the duration of the audio
    image_clip = image_clip.set_duration(audio_clip.duration)

    # Set the audio of the image clip
    final_clip = image_clip.set_audio(audio_clip)

    # Create a temporary file to store the video output
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp_video_file:
        temp_video_path = temp_video_file.name
        final_clip.write_videofile(temp_video_path, fps=24, codec='libx264')

    return temp_video_path