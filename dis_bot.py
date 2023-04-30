import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
from PIL import Image
import os

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
CHANNEL_ID = os.getenv("CHANNEL_ID")
discord_token = os.getenv("DISCORD_BOT_TOKEN")
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

directory = os.getcwd()
print(directory)

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

        # Define the input and output folder paths
        input_folder = "input"
        output_folder = "output"

        # Check if the output folder exists, and create it if necessary
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        # Check if the input folder exists, and create it if necessary
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)

        with open(f"{directory}/{input_folder}/{filename}", "wb") as f:
            f.write(response.content)
        print(f"Image downloaded: {filename}")

        input_file = os.path.join(input_folder, filename)

        if "UPSCALED_" not in filename:
            file_prefix = os.path.splitext(filename)[0]
            # Split the image
            top_left, top_right, bottom_left, bottom_right = split_image(input_file)
            # Save the output images with dynamic names in the output folder
            top_left.save(os.path.join(output_folder, file_prefix + "_top_left.jpg"))
            top_right.save(os.path.join(output_folder, file_prefix + "_top_right.jpg"))
            bottom_left.save(os.path.join(output_folder, file_prefix + "_bottom_left.jpg"))
            bottom_right.save(os.path.join(output_folder, file_prefix + "_bottom_right.jpg"))

        else:
            os.rename(f"{directory}/{input_folder}/{filename}", f"{directory}/{output_folder}/{filename}")
        # Delete the input file
        os.remove(f"{directory}/{input_folder}/{filename}")

@client.event
async def on_ready():
    print("Bot connected")

@client.event
async def on_message(message):
    # <Message id=1102082878805913653 channel=<TextChannel id=1102068352932909158 name='general' position=0 nsfw=False news=False category_id=1102068352932909156> type=<MessageType.default: 0> author=<Member id=709717610530340895 name='**Aatish**' discriminator='9476' bot=False nick=None guild=<Guild id=1102068352366690336 name='Midjourney ProjectX' shard_id=0 chunked=True member_count=4>> flags=<MessageFlags value=0>>
    # print(type(message)) //<class 'discord.message.Message'>
    for attachment in message.attachments:
        if "Upscaled by" in message.content:
            file_prefix = 'UPSCALED_'
        else:
            file_prefix = ''
        if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            await download_image(attachment.url, f"{file_prefix}{attachment.filename}")

async def call_discord(text):
    await client.wait_until_ready()  # wait until the bot is ready

    channel = client.get_channel(CHANNEL_ID)  # replace channel_id with the ID of the channel you want to send the message to
    await channel.send(text)


@client.command()
async def greet(ctx):
    text = "/imagine a man eating indian food."
    await ctx.send(text)
    await call_discord(text)


client.run(discord_token)
# call_discord("/imagine a man eating indian food.")