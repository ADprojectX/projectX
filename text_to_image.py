import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
from PIL import Image
import os
import pyautogui as pg
import time

dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)
CHANNEL_ID = os.getenv("CHANNEL_ID")
discord_token = os.getenv("DISCORD_BOT_TOKEN")
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())

directory = os.getcwd()
print(directory)

@client.event
async def on_ready():
    print("Bot connected")
    await call_discord(prompt, text)

async def call_discord(prompt, text):
    await client.wait_until_ready()  # wait until the bot is ready
    channel = client.get_channel(1102068352932909158)#(int(CHANNEL_ID))  # replace channel_id with the ID of the channel you want to send the message to
    await channel.send(prompt)
    await channel.send(text)

# @client.command()
# async def greet(ctx):
#     text = "/imagine\ta man eating indian food."
#     await ctx.send(text)
#     # await call_discord(prompt,text)

prompt = '/imagine'
text = "a man eating indian food."
client.run(discord_token)

# def convert_to_image(request_folder, image_desc):
#     return 0