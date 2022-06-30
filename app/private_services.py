from dotenv import load_dotenv
from pathlib import Path
from deepdiff import DeepDiff
import discord
import os
import ast
import urllib
import bs4


load_dotenv(Path(__file__).resolve().parent / '.env')
path = Path(__file__).parent.resolve()
# setup discord client
discord_token = os.getenv("DISCORD_TOKEN")
discord_server = os.getenv("DISCORD_SERVER")
discord_channel = os.getenv("DISCORD_CHANNEL")
client = discord.Client()


@client.event
async def on_ready():
    channel = client.get_channel(int(discord_channel))
    await channel.send(discord_msg)
    await client.close()


options = []
url = "https://genderkit.org.uk/resources/gender-services/"
soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "lxml")
# find the list of paid services
list = soup.find(text="Paid UK-based services").findNext('ul')
# extract name of each service
for li in list.findAll('li'):
    options.append(li.find('a').text)

# remove services that don't include endocrinology
if "Dr Lenihan" in options:
    options.remove("Dr Lenihan")
if "Kelly Psychology" in options:
    options.remove("Kelly Psychology")

# add other services not included in the list
options.append("GenderGP")

# sort options
options.sort()

# add other options
options.append("Other (UK Based, GMC Registered)")
options.append("Other (Non-UK Based)")

with open(path / 'private_services.txt') as f:
    old_options = f.read()
# convert options to list of tuples
old_options = ast.literal_eval(old_options)

# on any change, write changes to file and send message of difference to discord
if old_options != options:
    diff = DeepDiff(old_options, options, ignore_order=True)
    discord_msg = f"Private Services have changed!\n\nDifferences: \n\n{diff}"
    with open(path / 'private_services.txt', 'w') as f:
        f.write(str(options))
    client.run(discord_token)
