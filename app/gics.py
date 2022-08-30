from deepdiff import DeepDiff
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import discord
import os
import ast

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
url = "https://genderkit.org.uk/resources/wait-times"
pd.options.mode.chained_assignment = None
# get table of wait times from Gender Kit
table = pd.read_html(url, match="hormones")
df = table[0]
df['Service'] = df['Service'].map(lambda x: x[:-len("more info")])
df['Service'] = df['Service'].map(lambda x: x.strip())


df['To beseen(in months)'] = df['To beseen(in months)'].astype('Int64')

for i in range(len(df['Service'])):
    # Rename to GIC names
    if df['Service'][i] == "Belfast":
        df['Service'][i] = "Belfast Brackenburn Clinic"
    elif df['Service'][i] == "Edinburgh":
        df['Service'][i] = "Edinburgh Chalmers Centre"
    elif df['Service'][i] == "Exeter":
        df['Service'][i] = "Exeter Devon Partnership Trust"
    elif df['Service'][i] == "Glasgow":
        df['Service'][i] = "Glasgow Sandyford"
    elif df['Service'][i] == "Glasgow Youth":
        df['Service'][i] = "Glasgow Youth Sandyford"
    elif df['Service'][i] == "Inverness":
        df['Service'][i] = "Inverness Highland Sexual Health"
    elif df['Service'][i] == "Leeds":
        df['Service'][i] = "Leeds and York Partnership Trust"
    elif df['Service'][i] == "London GIC":
        df['Service'][i] = "London Tavistock and Portman Trust"
    elif df['Service'][i] == "London GIDS":
        df['Service'][i] = "London GIDS Tavistock and Portman Trust"
    elif df['Service'][i] == "Newcastle":
        df['Service'][i] = "Newcastle Northern Region Gender Dysphoria Service"
    elif df['Service'][i] == "Northants":
        df['Service'][i] = "Northants Northamptonshire Healthcare Trust"
    elif df['Service'][i] == "Nottingham":
        df['Service'][i] = "Nottingham Centre for Transgender Health"
    elif df['Service'][i] == "Sheffield":
        df['Service'][i] = "Sheffield Porterbrook Clinic"

        # assign country to each service
    if "Belfast" in df['Service'][i]:
        options.append(("Northern Ireland", df['Service'][i] +
                       " - Wait time (months): " + str(df['To beseen(in months)'][i])))
    elif "Cardiff" in df['Service'][i]:
        options.append(
            ("Wales", df['Service'][i] + " - Wait time (months): " + str(df['To beseen(in months)'][i])))
    elif "Edinburgh" in df['Service'][i] or "Glasgow" in df['Service'][i] or "Grampian" in df['Service'][i] or "Inverness" in df['Service'][i]:
        options.append(
            ("Scotland", df['Service'][i] + " - Wait time (months): " + str(df['To beseen(in months)'][i])))
    else:
        options.append(
            ("England", df['Service'][i] + " - Wait time (months): " + str(df['To beseen(in months)'][i])))

# removing youth services until specific youth document is developed
for gic in options:
    if "GIDS" in gic[1] or "KOI" in gic[1] or "Youth" in gic[1]:
        options.remove(gic)

# sort options
options.sort()

with open(path / 'GICs.txt') as f:
    old_options = f.read()
# convert options to list of tuples
old_options = list(ast.literal_eval(old_options))

# on any change, write changes to file and send message of difference to discord
if old_options != options:
    diff = DeepDiff(old_options, options, ignore_order=True)
    discord_msg = f"GICs have changed!\n\nDifferences: \n\n{diff}"
    with open(path / 'GICs.txt', 'w') as f:
        f.write(str(options))
    client.run(discord_token)
    print("GICs have changed")
