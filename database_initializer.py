import sqlite3

db = sqlite3.connect("prices.db")
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE prices(id INTEGER PRIMARY KEY, device TEXT, price TEXT, url TEXT)
''')
db.commit()
db.close()