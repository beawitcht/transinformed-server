import os, time
from datetime import datetime

# Script to update total number of files generated


path = '/var/log/www.transinformed.co.uk.access.log'
output_path = '/home/Beawitched/files_generated.txt'
timestamp_path = '/home/Beawitched/last_update_timestamp.txt'

with open(timestamp_path) as old_time:
    prev_update = datetime.strptime(old_time.read(), '%Y-%m-%d %H:%M:%S')

# get modified time and make it a datetime obj
modified = os.path.getmtime(path)
mod_time = datetime.fromtimestamp(time.mktime(time.strptime(time.ctime(modified))))

# when the file is modified append any new post requests to file
if mod_time > prev_update:
    with open(timestamp_path,'w') as old_time:
        old_time.write(str(mod_time))

    with open(output_path) as output:
        saved_data = output.readlines()

    with open(path) as log:
        data = log.readlines()
        for entry in data:
            if "POST" and "200" in entry and entry not in saved_data:
                with open(output_path, 'a') as f:
                    f.write(entry)
