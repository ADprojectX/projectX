import aws_connector
import create_video
import generate_caption
import sys
import os
from tempfile import NamedTemporaryFile
sys.path.append(os.path.join(os.getcwd(), 'captions'))
audio_file = "OBJECT_STORE/95608c0d-442e-40bb-bf0b-a321080f9cb2/5d78e522-718f-454d-b8da-78bc59d7a478/audio/XIL/e4061372-ab05-4584-a6da-9d16f028509a/Arnold/0.mp3"
image_file = "OBJECT_STORE/95608c0d-442e-40bb-bf0b-a321080f9cb2/5d78e522-718f-454d-b8da-78bc59d7a478/image/mjx/e4061372-ab05-4584-a6da-9d16f028509a/option1_a_brain_with_gears_turning_inside.jpg"
imv_path = "OBJECT_STORE/95608c0d-442e-40bb-bf0b-a321080f9cb2/5d78e522-718f-454d-b8da-78bc59d7a478/intermediate_video/e4061372-ab05-4584-a6da-9d16f028509a/mjx_Arnold.mp4"
narration = "Welcome to today's videos, where we'll explore 15 psychological facts that will blow your mind. Let's dive right in!"
audio = aws_connector.get_file_from_s3(audio_file)
image = aws_connector.get_file_from_s3(image_file)
# Create temporary files for audio and image
with NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
    temp_audio_file.write(audio)
    temp_audio_file_path = temp_audio_file.name

with NamedTemporaryFile(suffix=".jpg", delete=False) as temp_image_file:
    temp_image_file.write(image)
    temp_image_file_path = temp_image_file.name

# Create the intermediate video with captions
image_live = create_video.create_vid(temp_audio_file_path, temp_image_file_path)
imv_scene = generate_caption.generate_captions(image_live, temp_audio_file_path, narration)

# Upload the intermediate video with captions to S3
aws_connector.upload_file_to_s3(imv_scene, imv_path)
print('completed')