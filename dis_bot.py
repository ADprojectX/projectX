import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
from PIL import Image
import os
import re

# from text_to_image import pending_tasks
import database as db


dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)
CHANNEL_ID = os.getenv("CHANNEL_ID")
discord_token = os.getenv("DISCORD_BOT_TOKEN")
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())
# directory = os.getcwd()
# p


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


async def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        prompt, ext = os.path.splitext(filename)
        prompt = re.sub(
            r"_\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", "", prompt.lower()[7:]
        ).strip()
        pending_prompt = prompt.replace("_", " ").strip()
        print(pending_prompt, "dis_bot_checker")
        output_folder = db.remove_pending_tasks(pending_prompt)
        print(output_folder)

        if output_folder == None:
            return
        input_folder = output_folder + "/input"
        # Check if the input folder exists, and create it if necessary
        None if os.path.exists(input_folder) else os.makedirs(input_folder)
        file_ext = f"{prompt}.{ext}"
        with open(f"{input_folder}/{file_ext}", "wb") as f:
            f.write(response.content)
        print(f"Image downloaded: {file_ext}")

        input_file = os.path.join(input_folder, file_ext)

        if "UPSCALED_" not in filename:
            # file_prefix = os.path.splitext(filename)[0]
            file_prefix = prompt
            # Split the image
            top_left, top_right, bottom_left, bottom_right = split_image(input_file)
            # Save the output images with dynamic names in the output folder
            top_left.save(
                os.path.join(output_folder, "option1_" + file_prefix + ".jpg")
            )
            top_right.save(
                os.path.join(output_folder, "option2_" + file_prefix + ".jpg")
            )
            bottom_left.save(
                os.path.join(output_folder, "option3_" + file_prefix + ".jpg")
            )
            bottom_right.save(
                os.path.join(output_folder, "option4_" + file_prefix + ".jpg")
            )

        # else:
        #     os.rename(f"{directory}/{input_folder}/{filename}", f"{directory}/{output_folder}/{filename}")
        # Delete the input file
        os.remove(f"{input_file}")


@client.event
async def on_ready():
    print("Bot connected")


@client.event
async def on_message(message):
    print(message.content)
    for attachment in message.attachments:
        if "Upscaled by" in message.content:
            file_prefix = "UPSCALED_"
        else:
            file_prefix = ""
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            await download_image(attachment.url, f"{file_prefix}{attachment.filename}")


client.run(discord_token)

# <Message id=1102464819505942590 channel=<TextChannel id=1102068352932909158 name='general' position=0 nsfw=False news=False category_id=1102068352932909156>
# type=<MessageType.default: 0> author=<Member id=936929561302675456 name='Midjourney Bot' discriminator='9282' bot=True nick=None
# guild=<Guild id=1102068352366690336 name='Midjourney ProjectX' shard_id=0 chunked=True member_count=4>> flags=<MessageFlags value=0>>

# prompt = prompt.lower()
# prompt = prompt[8:]
# prompt = re.sub(r"_\w{8}-\w{4}-\w{4}-\w{4}-\w{12}", "", prompt)
# prompt = prompt.strip()
# pending_prompt = prompt.replace("_", " ")
