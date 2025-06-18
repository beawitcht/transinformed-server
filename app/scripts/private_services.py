"""Get private services maintained by TransActual for use in doc generator"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv

from deepdiff import DeepDiff
import pandas as pd
import discord


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
    """Discord alerts for changes to private services"""
    channel = client.get_channel(int(discord_channel))
    await channel.send(discord_msg)
    await client.close()

URL = "https://transactual.org.uk/medical-transition/private-care/"
pd.options.mode.chained_assignment = None
# get table of services
df = pd.read_html(URL, match="Service")

# Extract services to options list
options = df[0]['Service'].tolist()

# remove services that don't include endocrinology or other criteria
exclusions = ["Dr Lenihan", "Dignity Gender Assessment Services"]
options = [service for service in options if service not in exclusions]

# modify names where needed
if "Gender Identity SW" in options:
    options.remove("Gender Identity SW")
    options.append("Gender Identity South West")

if "GenderPlus with Kelly Psychology" in options:
    options.remove("GenderPlus with Kelly Psychology")
    options.append("GenderPlus")

# add other services not included in the list
options.append("GenderGP")

# sort options
options.sort()

# add other options
options.append("Other (UK Based, GMC Registered)")
options.append("Other (Non-UK Based)")


# output as json
options = {"Private Services": options}

with open(path / 'forms' / 'private_services.json', encoding="utf-8") as f:
    old_options = json.loads(f.read())

# on change, write changes to file and send message of difference to discord
if old_options != options:

    diff = json.dumps(DeepDiff(
        old_options["Private Services"], options["Private Services"], ignore_order=True), indent=4)
    if len(str(diff)) > 1900:
        discord_msg = "Private Services Changes too long check file"
    elif is_dev == "1":
        discord_msg = f"DEVELOPMENT TEST: Private Services have changed!\n\nDifferences: \n\n{diff}"
    else:
        discord_msg = f"Private Services have changed!\n\nDifferences: \n\n{diff}"
    with open(path / 'forms' / 'private_services.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(options))
    client.run(discord_token)
    print("Private Services have changed")
    Path(touch_path).touch()
