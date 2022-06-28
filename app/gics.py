import pandas as pd


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

with open('GICs.txt', 'w') as f:
    f.write(str(options).strip('[]'))