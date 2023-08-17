import discord
from discord.ext import commands, tasks
import requests
from dotenv import load_dotenv
from PIL import Image
import os
import re
import database as db
import boto3
from botocore.exceptions import NoCredentialsError
import tempfile

load_dotenv()
CHANNEL_ID = os.getenv("CHANNEL_ID")
discord_token = os.getenv("DISCORD_BOT_TOKEN")
# intents.typing = False
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_BUCKET = os.getenv('AWS_STORAGE_BUCKET_NAME')

s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
def count_files_in_s3_folder(folder_path):
    # Initialize the S3 client
    # List objects in the specified folder
    objects = s3.list_objects_v2(Bucket=AWS_BUCKET, Prefix=folder_path)
    
    # Count the number of files
    file_count = len(objects.get('Contents', []))
     
    return file_count

def upload_image_to_s3(image, file_name):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID, aws_secret_access_key=SECRET_ACCESS_KEY)
    try:
        # Create a temporary file to save the image
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
            image.save(temp_file, format="JPEG")
            temp_file.flush()
            # Upload the temporary file to S3
            s3.upload_file(temp_file.name, AWS_BUCKET, file_name)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False


def split_image(image_file):
    with Image.open(image_file) as im:
        # Get the width and height of the original image
        width, height = im.size
        # Calculate the middle points along the horizontal and vertical axes
        mid_x = width // 2
        mid_y = height // 2
        # Split the image into four equal parts
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))

        return top_left, top_right, bottom_left, bottom_right


async def download_image(url, filename, prompt):
    response = requests.get(url)
    if response.status_code == 200:
        _, ext = os.path.splitext(filename)
        output_folder = db.find_pending_task(prompt)
        if output_folder == None:
            return
        input_folder = output_folder
        # Check if the input folder exists, and create it if necessary
        None if os.path.exists(input_folder) else os.makedirs(input_folder)
        # print(prompt, ext, 'demodummy')

        with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as temp_file:
            temp_file.write(response.content)
            temp_file_path = temp_file.name

        print(f"Image downloaded: {prompt}")

        if "UPSCALED_" not in filename:
            # file_prefix = prompt.replace(" ", '_').lower()
            top_left, top_right, bottom_left, bottom_right = split_image(temp_file_path)
            # i = count_files_in_s3_folder(output_folder)
            i = 0
            upload_image_to_s3(top_left, f"{output_folder}_option{i+1}.jpg")
            upload_image_to_s3(top_right, f"{output_folder}_option{i+2}.jpg")
            upload_image_to_s3(bottom_left, f"{output_folder}_option{i+3}.jpg")
            upload_image_to_s3(bottom_right, f"{output_folder}_option{i+4}.jpg")

        db.delete_pending_task(prompt)
        os.remove(temp_file_path)


# @tasks.loop(minutes=15)  # Adjust the interval as needed
# async def update_presence():
#     await client.change_presence(activity=discord.Game(name="Staying Active"))

@client.event
async def on_ready():
    print("Bot connected")
    # update_presence.start()


@client.event
async def on_message(message):
    for attachment in message.attachments:
        # **a group of people with one person standing out due to their positive trait** - <@709717610530340895> (fast)
        result = re.search(r"\*\*(.*?)\*\*", message.content)
        if result:
            prompt = result.group(1)[:-6]
            print(prompt)
        else:
            print("No match found.")
        if "Upscaled by" in message.content:
            file_prefix = "UPSCALED_"
        else:
            file_prefix = ""
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            await download_image(attachment.url, f"{file_prefix}{attachment.filename}", prompt)


client.run(discord_token)

# <Message id=1102464819505942590 channel=<TextChannel id=1102068352932909158 name='general' position=0 nsfw=False news=False category_id=1102068352932909156>
# type=<MessageType.default: 0> author=<Member id=936929561302675456 name='Midjourney Bot' discriminator='9282' bot=True nick=None
# guild=<Guild id=1102068352366690336 name='Midjourney ProjectX' shard_id=0 chunked=True member_count=4>> flags=<MessageFlags value=0>>

# prompt = prompt.lower()
# prompt = prompt[8:]
# prompt = re.sub(r"_\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", "", prompt)
# prompt = prompt.strip()
# pending_prompt = prompt.replace("_", " ")

        # file_ext = f"{ext}"
        # with open(f"{input_folder}/{file_ext}", "wb") as f:
        #     f.write(response.content)
        # print(f"Image downloaded: {prompt}{ext}")

        # input_file = os.path.join(input_folder, file_ext)

        # if "UPSCALED_" not in filename:
        #     # file_prefix = os.path.splitext(filename)[0]
        #     file_prefix = prompt.replace(" ", '_').lower()
        #     # Split the image
        #     top_left, top_right, bottom_left, bottom_right = split_image(input_file)
        #     # Save the output images with dynamic names in the output folder
        #     i = count_files_in_s3_folder(output_folder)
        #     upload_image_to_s3(top_left, f"{output_folder}_option{i+1}.jpg")
        #     upload_image_to_s3(top_right, f"{output_folder}_option{i+2}.jpg")
        #     upload_image_to_s3(bottom_left, f"{output_folder}_option{i+3}.jpg")
        #     upload_image_to_s3(bottom_right, f"{output_folder}_option{i+4}.jpg")
        # os.remove(f"{input_file}")