"""Get GICs maintained by TransActual for use in doc generator"""
import os
import re
import json
from pathlib import Path

from dotenv import load_dotenv
import pandas as pd
import discord


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
    """Discord alerts for changes to GICs"""
    channel = client.get_channel(int(discord_channel))
    await channel.send(discord_msg)
    await client.close()


options = []
URL = "https://transactual.org.uk/medical-transition/gender-dysphoria-clinics/"
pd.options.mode.chained_assignment = None
# get table of wait times from Gender Kit
table = pd.read_html(URL, match="hormones")

df = table[0]
# set column names equal to values in row index position 0
df.columns = df.iloc[0]

# remove first row from DataFrame
df = df[1:]

# format service names
df["Service"] = df["Service"].map(lambda x: x.split("–", 1)[1])
df["Service"] = df["Service"].map(lambda x: x.strip())
# rename
name_mappings = {
    "Gender Identity Wales": "Welsh Gender Service"
}
df['Service'] = df['Service'].map(lambda x: name_mappings.get(x, x))


youth_times = df["To be seen (in months)"]

for _, row in df.iterrows():
    country = ""
    service = row.iloc[0]
    to_be_seen = row.iloc[1]
    youth_services = ["Young People", "young people"]

    # Determine the country based on the service name
    if re.search(r"\b(Brackenburn|KOI)\b", service):
        country = "Northern Ireland"
    elif "Welsh" in service:
        country = "Wales"
    elif re.search(r"\b(Edinburgh|Glasgow|Grampian|Inverness|Sandyford|Highland)\b", service):
        country = "Scotland"
    else:
        country = "England"

    # Determine if youth service
    for identifier in youth_services:
        if identifier in service:
            country = "Y-" + country

    # replace not known with unknown
    if "Not known" in to_be_seen:
        to_be_seen = "Unknown"

    if "?" not in str(to_be_seen):
        options.append((country, f"{service} - Wait time (months): {to_be_seen}" if
                        pd.notna(to_be_seen) else f"{service} - Wait time (months): Unknown"))


# Filter services not taking new referrals from GP/self or limited access
invalid_services = ["London TransPlus", "The Northern Hub", "The Southern Hub",
                    "for under 18s, coming soon", "Indigo Gender Service (New style clinic)",
                    "Sussex Gender Service (Pilot clinic)", "TransPlus (New style clinic)"]
options = [gic for gic in options if all(
    service not in gic[1] for service in invalid_services)]
# filter out < > from options
options = [(country, re.sub(r'<|>|\*', '', option))
           for country, option in options]
# replace nonstandard spaces
options = [(country, option.replace(u'\xa0', u' '))
           for country, option in options]


# Add NRSS or the very concise name: NATIONAL REFERRAL SUPPORT SERVICE FOR THE NHS GENDER INCONGRUENCE SERVICE FOR CHILDREN AND YOUNG PEOPLE
options.append(
    ("Y-England", "National Referral Support Service - Wait time: Unknown"))
options.append(
    ("Y-Wales", "National Referral Support Service - Wait time: Unknown"))

# Sort options by months remaining
options.sort(key=lambda x: int(
    re.search(r'(\d+)', x[1]).group(0)) if "Unknown" not in x[1] else 9999)
new_options = {"GICs": options}
new_options = json.dumps(new_options)

with open(path / 'forms' / 'GICs.json', encoding="utf-8") as f:
    old_options = json.loads(f.read())

# Compare items with the same name in the diff
old_options_dict = {item[1].split(
    " - ")[0]: item for item in old_options["GICs"]}
new_options_dict = {item[1].split(
    " - ")[0]: item for item in json.loads(new_options)["GICs"]}

# Find added and removed items
added = [item for item in new_options_dict.items() if item[0]
         not in old_options_dict]
removed = [item for item in old_options_dict.items() if item[0]
           not in new_options_dict]

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
    with open(path / 'forms' / 'GICs.json', 'w', encoding="utf-8") as f:
        f.write(new_options)
    client.run(discord_token)

    print("GICs have changed")
    Path(touch_path).touch()
