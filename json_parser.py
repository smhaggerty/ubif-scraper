import json

with open('output.json') as data_file:
    data = json.load(data_file)

data = sorted(data, key=lambda x : x['url'])
# dump dict to json string
json_string = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
# save sorted json as sorted_output.json
with open('sorted_output.json', 'w') as sorted_data_file:
     sorted_data_file.write(json_string)