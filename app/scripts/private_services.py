from dotenv import load_dotenv
from pathlib import Path
from deepdiff import DeepDiff
import discord
import os
import urllib
import bs4
import json

path = Path(__file__).parent.parent.resolve()
load_dotenv(path / '.env')

# setup discord client
discord_token = os.getenv("DISCORD_TOKEN")
discord_server = os.getenv("DISCORD_SERVER")
discord_channel = os.getenv("DISCORD_CHANNEL")
touch_path = os.getenv("TOUCH_PATH")
intents = discord.Intents.default()
client = discord.Client(intents=intents)
is_dev = os.getenv("IS_DEV")

@client.event
async def on_ready():
    channel = client.get_channel(int(discord_channel))
    await channel.send(discord_msg)
    await client.close()


options = []
url = "https://genderkit.org.uk/resources/gender-services/"
soup = bs4.BeautifulSoup(urllib.request.urlopen(url).read(), "lxml")
# find the list of paid services
service_list = soup.find(text="Paid UK-based services").findNext('ul')
# extract name of each service
for li in service_list.findAll('li'):
    options.append(li.find('a').text)

exclusions = ["Dr Lenihan", "Kelly Psychology", "GenderPlus"]
# remove services that don't include endocrinology or other criteria
options = [service for service in options if service not in exclusions]

# modify names where needed
if "Gender Identity SW" in options:
    options.remove("Gender Identity SW")
    options.append("Gender Identity South West")


# add other services not included in the list
options.append("GenderGP")

# sort options
options.sort()

# add other options
options.append("Other (UK Based, GMC Registered)")
options.append("Other (Non-UK Based)")

# output as json
options = {"Private Services": options}

with open(path / 'forms' / 'private_services.json') as f:
        old_options = json.loads(f.read())
        
# on any change, write changes to file and send message of difference to discord
if old_options != options:
    
    diff = json.dumps(DeepDiff(old_options["Private Services"], options["Private Services"], ignore_order=True), indent=4)
    if len(str(diff)) > 1900:
        discord_msg = "Private Services Changes too long check file"
    elif is_dev == "1":
        discord_msg = f"DEVLEOPMENT TEST: Private Services have changed!\n\nDifferences: \n\n{diff}"
    else:
        discord_msg = f"Private Services have changed!\n\nDifferences: \n\n{diff}"
    with open(path / 'forms' / 'private_services.json', 'w') as f:
        f.write(json.dumps(options))
    client.run(discord_token)
    Path(touch_path).touch()
