# import os
# from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from io import BytesIO
from django.conf import settings
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import datetime
from botocore.signers import CloudFrontSigner

# load_dotenv()
ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID #os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY #os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = settings.AWS_STORAGE_BUCKET_NAME #os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_CLOUDFRONT_DOMAIN = settings.AWS_S3_CUSTOM_DOMAIN #os.getenv('AWS_CLOUDFRONT_DOMAIN')
AWS_CLOUDFRONT_KEY_ID = settings.AWS_CLOUDFRONT_KEY_ID #os.getenv("AWS_CLOUDFRONT_KEY_ID")
AWS_CLOUDFRONT_KEY = settings.AWS_CLOUDFRONT_KEY #os.getenv("AWS_CLOUDFRONT_KEY")

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)



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


def rsa_signer(message):
    private_key = serialization.load_pem_private_key(
        AWS_CLOUDFRONT_KEY,
        password=None,
        backend=default_backend()
    )
    return private_key.sign(message, padding.PKCS1v15(), hashes.SHA1())


def cdn_path(path):
    # print(AWS_CLOUDFRONT_KEY, 'key')
    try:
        url = f'https://{AWS_CLOUDFRONT_DOMAIN}/{path}' #-- Distribution domain name
        current_time = datetime.datetime.utcnow()
        expire_date = current_time + datetime.timedelta(seconds=3600)
        cloudfront_signer = CloudFrontSigner(AWS_CLOUDFRONT_KEY_ID, rsa_signer)

        # Create a signed url that will be valid until the specific expiry date
        # provided using a canned policy.
        signed_url = cloudfront_signer.generate_presigned_url(
            url, date_less_than=expire_date)
        return signed_url
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

        # # Encrypt the path using the private key
        # private_key = serialization.load_pem_private_key(
        #     AWS_CLOUDFRONT_KEY,
        #     password=None  # Change this if your private key is password-protected
        # )
        # encrypted_path = private_key.sign(
        #     path.encode("utf-8"),
        #     padding.PKCS1v15(),
        #     hashes.SHA256()
        # )
        
        # # Convert the encrypted path to a hexadecimal string
        # encrypted_path_hex = encrypted_path.hex()
        
        # # Generate the CloudFront URL with the encrypted path and key ID as query parameters
        # cloudfront_url = f"{AWS_CLOUDFRONT_DOMAIN}?path={encrypted_path_hex}&key_id={AWS_CLOUDFRONT_KEY_ID}"
        