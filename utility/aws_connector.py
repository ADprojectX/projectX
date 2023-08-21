import boto3
from time import sleep
from botocore.exceptions import ClientError, NoCredentialsError
from io import BytesIO
from django.conf import settings
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import datetime
from botocore.signers import CloudFrontSigner
from dotenv import load_dotenv
import os

def get_env_variables(key):
    load_dotenv(override=True)
    return os.getenv(key)

s3 = boto3.client('s3', aws_access_key_id=get_env_variables('AWS_ACCESS_KEY_ID'), aws_secret_access_key=get_env_variables('AWS_SECRET_ACCESS_KEY'))

def check_file_exists(image_key):
    try:
        # Check if the image exists in the specified bucket
        response = s3.head_object(Bucket=get_env_variables('AWS_STORAGE_BUCKET_NAME'), Key=image_key)
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
        response = s3.get_object(Bucket=get_env_variables('AWS_STORAGE_BUCKET_NAME'), Key=file_key)
        file_data = response['Body'].read()
        return file_data
    except ClientError as e:
        print(f"An error occurred: {e}")
        return None

def file_exists_in_s3(file_name):
    """
    Check if file exists in the specified S3 bucket.
    """
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(get_env_variables('AWS_STORAGE_BUCKET_NAME'))
    
    objs = list(bucket.objects.filter(Prefix=file_name))
    return any([w.key == file_name for w in objs])

def upload_file_to_s3(file_data, file_name):
    try:
        # Create a file-like object from the file data
        file_obj = BytesIO(file_data)
        # Upload the file-like object to S3
        while not file_exists_in_s3(file_name):
            s3.upload_fileobj(file_obj, get_env_variables('AWS_STORAGE_BUCKET_NAME'), file_name)
            sleep(120)
        print("Upload Successful")
        return True
    except NoCredentialsError:
        print("Credentials not available")
        return False


def rsa_signer(message):
    private_key_data = os.getenv("AWS_CLOUDFRONT_KEY").replace("\\n", "\n")
    private_key = serialization.load_pem_private_key(
        private_key_data.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def cdn_path(path):
    try:
        cloudfront_key_id = get_env_variables("AWS_CLOUDFRONT_KEY_ID")
        cloudfront_domain = get_env_variables("AWS_CLOUDFRONT_DOMAIN")
        
        url = f'https://{cloudfront_domain}/{path}'
        current_time = datetime.datetime.utcnow()
        expire_date = current_time + datetime.timedelta(seconds=3600)
        cloudfront_signer = CloudFrontSigner(cloudfront_key_id, rsa_signer)

        signed_url = cloudfront_signer.generate_presigned_url(
            url, date_less_than=expire_date)
        return signed_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

################################################################################################################################################################################################################################
# get_env_variables('AWS_ACCESS_KEY_ID') = settings.AWS_ACCESS_KEY_ID #os.getenv('AWS_ACCESS_KEY_ID')
# SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY #os.getenv('AWS_SECRET_ACCESS_KEY')
# get_env_variables('AWS_STORAGE_BUCKET_NAME') = settings.AWS_STORAGE_BUCKET_NAME #os.getenv('AWS_STORAGE_BUCKET_NAME')
# AWS_CLOUDFRONT_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN #os.getenv('AWS_CLOUDFRONT_DOMAIN')
# AWS_CLOUDFRONT_KEY_ID = settings.AWS_CLOUDFRONT_KEY_ID #os.getenv("AWS_CLOUDFRONT_KEY_ID")
# AWS_CLOUDFRONT_KEY = settings.AWS_CLOUDFRONT_KEY #os.getenv("AWS_CLOUDFRONT_KEY")

    # ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    # SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    # AWS_BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME')
    # AWS_CLOUDFRONT_DOMAIN = os.getenv('AWS_CLOUDFRONT_DOMAIN')
    # AWS_CLOUDFRONT_KEY_ID = os.getenv("AWS_CLOUDFRONT_KEY_ID")
    # AWS_CLOUDFRONT_KEY = os.getenv("AWS_CLOUDFRONT_KEY")