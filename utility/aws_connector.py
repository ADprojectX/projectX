import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from io import BytesIO

load_dotenv()
ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.getenv('AWS_BUCKET_STORE')

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
def count_files_in_s3_folder(folder_path):
    # Initialize the S3 client
    # List objects in the specified folder
    objects = s3.list_objects_v2(Bucket=AWS_BUCKET, Prefix=folder_path)
    
    # Count the number of files
    file_count = len(objects.get('Contents', []))
    
    return file_count

def check_file_exists(image_key):
    try:
        # Check if the image exists in the specified bucket
        response = s3.head_object(Bucket=AWS_BUCKET, Key=image_key)
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            return False
        else:
            # Handle other errors if needed
            print(f"An error occurred: {e}")
            return False

def get_file_from_s3(file_key):
    try:
        response = s3.get_object(Bucket=AWS_BUCKET, Key=file_key)
        file_data = response['Body'].read()
        return file_data
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None
    
# def upload_audio_to_s3(audio_data, file_name):
#   
#     try:
#         # Create a file-like object from the audio data
#         audio_file = BytesIO(audio_data)
#         # Upload the audio file-like object to S3
#         s3.upload_fileobj(audio_file, AWS_BUCKET, file_name)
#         print("Upload Successful")
#         return True
#     except NoCredentialsError:
#         print("Credentials not available")
#         return False


def upload_file_to_s3(file_data, file_name):
    try:
        # Create a file-like object from the file data
        file_obj = BytesIO(file_data)
        # Upload the file-like object to S3
        s3.upload_fileobj(file_obj, AWS_BUCKET, file_name)
        print("Upload Successful")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False

