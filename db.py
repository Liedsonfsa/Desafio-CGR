import sqlite3 as sql

conn = sql.connect('equipamentos.db')

cursor = conn.cursor()

query = ''''''

cursor.execute(query)

conn.commit()
