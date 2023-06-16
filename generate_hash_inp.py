import json
with open('j_data_file.json', 'w') as outfile:
    json.dump(j_data, outfile,indent=4)