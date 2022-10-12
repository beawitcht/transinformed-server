import requests
import discord
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / '.env')
path = Path(__file__).parent.resolve()
# setup discord client
discord_token = os.getenv("DISCORD_TOKEN")
discord_server = os.getenv("DISCORD_SERVER")
discord_channel = os.getenv("DISCORD_CHANNEL")
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    channel = client.get_channel(int(discord_channel))
    await channel.send(discord_msg)
    await client.close()


ping = requests.get("https://www.transinformed.co.uk/")
status_code = ping.status_code
error_message = ping.text


if status_code >=500:
    discord_msg = "SITE ERROR CODE: " + str(status_code) + "\n" + error_message
    client.run(discord_token)