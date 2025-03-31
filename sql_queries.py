import sqlite3 

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()


cursor.execute("SELECT * FROM card_data")
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
