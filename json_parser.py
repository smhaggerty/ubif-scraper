import json
from pprint import pprint

# open the unsorted json data
with open('output.json') as data_file:
    data = json.load(data_file)
# sort json by url
sorted_results = sorted(data['repairs'], key=lambda x: x['url'])
# reappend 'repairs' key and rebuild json
sorted_json = {}
sorted_json['repairs'] = sorted_results
json_data = json.dumps(sorted_json)
# save sorted json
with open('sorted_output.json', 'w') as sorted_data_file:
     sorted_data_file.write(json_data)
