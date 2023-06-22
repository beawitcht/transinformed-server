from deepdiff import DeepDiff
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import discord
import os
import re
import json

path = Path(__file__).parent.parent.resolve()
load_dotenv(path / '.env')

# setup discord client
discord_token = os.getenv("DISCORD_TOKEN")
discord_server = os.getenv("DISCORD_SERVER")
discord_channel = os.getenv("DISCORD_CHANNEL")
is_dev = os.getenv("IS_DEV")
intents = discord.Intents.default()
client = discord.Client(intents=intents)
touch_path = os.getenv("TOUCH_PATH")


@client.event
async def on_ready():
    channel = client.get_channel(int(discord_channel))
    await channel.send(discord_msg)
    await client.close()


options = []
url = "https://genderkit.org.uk/resources/wait-times"
pd.options.mode.chained_assignment = None
# get table of wait times from Gender Kit
table = pd.read_html(url, match="hormones")
df = table[0]
df['Service'] = df['Service'].map(lambda x: x[:-len("more info")])
df['Service'] = df['Service'].map(lambda x: x.strip())



# Map names to full names
name_mappings = {
    "Belfast": "Belfast Brackenburn Clinic",
    "Edinburgh": "Edinburgh Chalmers Centre",
    "Exeter": "Exeter Devon Partnership Trust",
    "Glasgow": "Glasgow Sandyford",
    "Glasgow Youth": "Glasgow Youth Sandyford",
    "Inverness": "Inverness Highland Sexual Health",
    "Leeds": "Leeds and York Partnership Trust",
    "London GIC": "London Tavistock and Portman Trust",
    "London GIDS": "London GIDS Tavistock and Portman Trust",
    "Newcastle": "Newcastle Northern Region Gender Dysphoria Service",
    "Northants": "Northants Northamptonshire Healthcare Trust",
    "Nottingham": "Nottingham Centre for Transgender Health",
    "Sheffield": "Sheffield Porterbrook Clinic"
}
df['Service'] = df['Service'].map(lambda x: name_mappings.get(x, x))

for _, row in df.iterrows():
    country = ""
    service = row['Service']
    to_be_seen = row['To beseen(in months)']
    
    if "Belfast" in service:
        country = "Northern Ireland"
    elif "Cardiff" in service:
        country = "Wales"
    elif re.search(r"\b(Edinburgh|Glasgow|Grampian|Inverness)\b", service):
        country = "Scotland"
    else:
        country = "England"

    options.append((country, f"{service} - Wait time (months): {to_be_seen}" if pd.notna(to_be_seen) else "Unknown"))

# Filter out specific services
options = [gic for gic in options if "GIDS" not in gic[1] and "KOI" not in gic[1] and "Youth" not in gic[1]]

# Sort options by months remaining
options.sort(key=lambda x: int(x[1].split(': ')[1][-2:]) if x[1].split(': ')[1] != 'nan' else 9999)

options = {"GICs": options}
options = json.dumps(options)

with open(path / 'GICs.json') as f:
    old_options = json.loads(f.read())


# on any change, write changes to file and send message of difference to discord
if old_options != json.loads(options):
    diff = json.dumps(DeepDiff(old_options["GICs"], json.loads(options)['GICs'], ignore_order=True), indent=4)
    if len(str(diff)) > 1900:
        discord_msg = "GICs Changes too long check file"
    elif is_dev == '1':
        discord_msg = f"DEVLEOPMENT TEST: GICs have changed!\n\nDifferences: \n\n{diff}"
    else:
        discord_msg = f"GICs have changed!\n\nDifferences: \n\n{diff}"
    with open(path / 'GICs.json', 'w') as f:
        f.write(options)
    client.run(discord_token)
    print("GICs have changed")
    Path(touch_path).touch()
