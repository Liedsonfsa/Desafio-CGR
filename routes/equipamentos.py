from flask import jsonify, request
from routes.logs import generateLog
from datetime import datetime
import sqlite3 as sql

def buscarEquipamentos():
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos'

    cursor.execute(query)

    equipamentos = cursor.fetchall()

    conn.close()

    if equipamentos is None or equipamentos == []:
        return jsonify({"error": "Recurso não encontrado"}), 404
    else:
        return jsonify(equipamentos)

def buscarEquipamentoPorID(id: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos WHERE id = ?'

    cursor.execute(query, (id,))

    equipamento = cursor.fetchone()
    
    conn.close()

    if equipamento is None or equipamento == []:
        return jsonify({"error": "Recurso não encontrado"}), 404
    else:
        return jsonify(equipamento)

def pegarStatusDoEquipamentoPorID(id: int):
    dados_recebidos = request.get_json()

    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'UPDATE equipamentos SET status = ? WHERE id = ?'

    cursor.execute(query, (dados_recebidos['status'], id))

    conn.commit()

    conn.close()

    generateLog(id, 'Status Change', dados_recebidos['descricao'])

    return jsonify(
        {
            "equipamento_id": id,
            "new_status": dados_recebidos['status'], 
            "tipo_evento": 'Status Change',
            "descricao": dados_recebidos['descricao']
        }
    )
