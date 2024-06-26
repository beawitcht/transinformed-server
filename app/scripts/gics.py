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

# get youth wait times for England and Wales
youth_table = pd.read_html(url, match="Longest wait")
youth_df = youth_table[0]
youth_times = youth_df["Longest wait"][0]
# Map names to full names
name_mappings = {
    "Belfast": "Belfast Brackenburn Clinic",
    "Cardiff": "Welsh Gender Service - Cardiff",
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
    youth_services = ["GIDS", "KOI", "Youth", "Hub"]

    # Determine the country based on the service name
    if "Belfast" in service:
        country = "Northern Ireland"
    elif "Cardiff" in service:
        country = "Wales"
    elif re.search(r"\b(Edinburgh|Glasgow|Grampian|Inverness)\b", service):
        country = "Scotland"
    else:
        country = "England"

    # Determine if youth service
    for identifier in youth_services:
        if identifier in service:
            country = "Y-" + country
    
    if "Not accepting new patients" not in str(to_be_seen):
        options.append((country, f"{service} - Wait time (months): {to_be_seen}" if pd.notna(to_be_seen) else f"{service} - Wait time (months): Unknown"))



# Filter services not taking new referrals from GP/self
invalid_services = ["London TransPlus", "The Northern Hub", "The Southern Hub"]
options = [gic for gic in options if all(service not in gic[1] for service in invalid_services)]

# filter out < > from options
options = [(country, re.sub(r'<|>', '', option)) for country, option in options]

# Add NRSS or the very concise name: NATIONAL REFERRAL SUPPORT SERVICE FOR THE NHS GENDER INCONGRUENCE SERVICE FOR CHILDREN AND YOUNG PEOPLE
options.append(("Y-England", f"National Referral Support Service - Wait time: {youth_times}"))
options.append(("Y-Wales", f"National Referral Support Service - Wait time: {youth_times}"))

# Sort options by months remaining
options = sorted(options, key=lambda x: int(re.search(r'\d+', str(x[1].split(': ')[1] if len(x) == 2 and 'Unknown' not in x[1] else '0')).group()))

new_options = {"GICs": options}
new_options = json.dumps(new_options)

with open(path / 'forms' / 'GICs.json') as f:
    old_options = json.loads(f.read())


# Compare items with the same name in the diff
old_options_dict = {item[1].split(" - ")[0]: item for item in old_options["GICs"]}
new_options_dict = {item[1].split(" - ")[0]: item for item in json.loads(new_options)["GICs"]}

# Find added and removed items
added = [item for item in new_options_dict.items() if item[0] not in old_options_dict]
removed = [item for item in old_options_dict.items() if item[0] not in new_options_dict]

diff = []
for name, new_item in new_options_dict.items():
    if name in old_options_dict:
        # Existing item: Compare old and new item
        old_item = old_options_dict[name]
        if old_item != new_item:
            diff.append((old_item, new_item))

# Include added and removed items in the diff
for name, old_item in removed:
    # Removed item
    diff.append((old_item, None))
for name, new_item in added:
    # Added item
    diff.append((None, new_item))

# on any change, write changes to file and send message of difference to discord
if diff:
    diff_message = "GICs have changed!\n\nDifferences:\n\n"
    for old_item, new_item in diff:
        if old_item is not None and new_item is not None:
            # Existing item: Show old and new values
            diff_message += f"Old: {old_item[1]}\nNew: {new_item[1]}\n\n"
        elif old_item is not None:
            # Removed item: Show old value
            diff_message += f"Removed: {old_item[1]}\n\n"
        else:
            # Added item: Show new value
            diff_message += f"Added: {new_item[1]}\n\n"
    if len(diff_message) > 1900:
        discord_msg = "GICs Changes too long check file"
    elif is_dev == '1':
        discord_msg = f"DEVELOPMENT TEST: {diff_message}"
    else:
        discord_msg = diff_message
    with open(path / 'forms' / 'GICs.json', 'w') as f:
        f.write(new_options)
    client.run(discord_token)
    
    print("GICs have changed")
    Path(touch_path).touch()