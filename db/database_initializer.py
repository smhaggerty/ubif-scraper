import sqlite3

db = sqlite3.connect("repairs.db")
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE prices(id INTEGER PRIMARY KEY, device TEXT, repair TEXT, price TEXT, url TEXT)
''')
db.commit()
db.close()
