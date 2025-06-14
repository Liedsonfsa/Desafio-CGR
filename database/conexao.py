import sqlite3 as sql

def conectar():
    return sql.connect('database/equipamentos.db')
