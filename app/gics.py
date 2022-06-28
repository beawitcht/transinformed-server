import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import discord
import os, ast

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
url="https://genderkit.org.uk/resources/wait-times"
# get table of wait times from Gender Kit
table= pd.read_html(url, match="hormones")
df = table[0]
df['Service'] = df['Service'].map(lambda x: x[:-len("more info")])
df['Service'] = df['Service'].map(lambda x: x.strip())

# assign country to each service
for i in range(len(df['Service'])):
    if "Belfast" in df['Service'][i]:
        options.append(("Northern Ireland", df['Service'][i] + " - Wait time (months): " + df['To beseen(in months)'][i]))
    elif "Cardiff" in df['Service'][i]:
        options.append(("Wales", df['Service'][i] + " - Wait time (months): " + df['To beseen(in months)'][i]))
    elif "Edinburgh" in df['Service'][i] or "Glasgow" in df['Service'][i] or "Grampian" in df['Service'][i] or "Inverness" in df['Service'][i]:
        options.append(("Scotland", df['Service'][i] + " - Wait time (months): " + df['To beseen(in months)'][i]))
    else:
        options.append(("England", df['Service'][i] + " - Wait time (months): " + df['To beseen(in months)'][i]))



with open(path / 'GICs.txt') as f:
    old_options = f.read()
# convert options to list of tuples
old_options = list(ast.literal_eval(old_options))

# on any change, write changes to file and send message of difference to discord
if old_options != options:
    discord_msg = f"GICs have changed!\nDifferences (Old, New): \n{set(old_options).symmetric_difference(options)}"
    with open(path / 'GICs.txt', 'w') as f:
        f.write(str(options).strip('[]'))
    client.run(discord_token)
    


