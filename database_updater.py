import sqlite3
import json

# connect to database and setup cursor
db = sqlite3.connect("prices.db")
cursor = db.cursor()

# import the price data json file
with open('prices.json') as data_file:
    prices = json.load(data_file)

# loop through each price in the json file
for device_info in prices:
    device = " ".join(device_info["url"].split("/")[-2].split("-")[:-1])
    price = device_info['price']
    url = device_info['url']

    cursor.execute('''INSERT INTO prices(device, price, url) VALUES(?,?,?)''', (device, price, url))
    print('Device inserted')

db.commit()
db.close()