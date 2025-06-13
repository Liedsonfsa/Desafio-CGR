import sqlite3 as sql
from datetime import datetime

def conectar():
    return sql.connect('equipamentos.db')
