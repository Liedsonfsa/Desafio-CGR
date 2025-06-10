from flask import jsonify
import sqlite3 as sql
from datetime import datetime

def getLogs():
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM EventosLogs'

    cursor.execute(query)

    logs = cursor.fetchall()

    return jsonify(logs)

def generateLog(equipamentoID: int, event_type: str, descricao: str):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'INSERT INTO EventosLogs (equipamento_id, tipo_evento, descricao) VALUES (?, ?, ?)'

    cursor.execute(query, (equipamentoID, event_type, descricao))
    conn.commit()

    conn.close()

    