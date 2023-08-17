import aws_connector
import create_video
import generate_caption
import sys
import os
from tempfile import NamedTemporaryFile
sys.path.append(os.path.join(os.getcwd(), 'captions'))
audio_file = "OBJECT_STORE/c6f3321a-4827-49f0-9c57-cbc5f13b3fc3/717864c2-3cf3-46b1-9ab0-ff8cba2c610d/audio/XIL/1589a4a0-1f80-430f-a099-ca3616f4c22d/Emily/0.mp3"
image_file = "OBJECT_STORE/c6f3321a-4827-49f0-9c57-cbc5f13b3fc3/717864c2-3cf3-46b1-9ab0-ff8cba2c610d/image/mjx/1589a4a0-1f80-430f-a099-ca3616f4c22d/fa68f175-87e7-4f44-b115-957fca57765b_option1.jpg"
imv_path = "OBJECT_STORE/c6f3321a-4827-49f0-9c57-cbc5f13b3fc3/717864c2-3cf3-46b1-9ab0-ff8cba2c610d/intermediate_video/1589a4a0-1f80-430f-a099-ca3616f4c22d/mjx_Emily.mp4"
narration = "To begin, heat a tablespoon of olive oil in a pan over medium heat. Add boneless chicken breasts and cook them until they turn golden brown on both sides. Remove the chicken from the pan and set it aside."
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