from flask import jsonify
import sqlite3 as sql

def getLogs():
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM EventosLogs'

    cursor.execute(query)

    logs = cursor.fetchall()

    return jsonify(logs)