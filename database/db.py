import sqlite3 as sql

def getConnection():
    conn = sql.connect('../equipamentos.db')
    return conn.cursor()