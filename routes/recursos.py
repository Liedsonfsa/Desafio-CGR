from flask import jsonify
import sqlite3 as sql

def buscarRecursosDeUmEquipamentoPorID(equipamentoId: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM RecursosRede WHERE equipamento_id = ?'

    cursor.execute(query, (equipamentoId,))

    recursos = cursor.fetchall()

    conn.close()

    if recursos is None or recursos == []:
        return jsonify({"error": "Recurso não encontrado"}), 404
    else:
        return jsonify(recursos)