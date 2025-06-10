from flask import jsonify, request
from routes.logs import generateLog
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
    
def verificarStatusDoRecurso(id: int, tipo_recurso: str):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = "SELECT EXISTS(SELECT 1 FROM RecursosRede WHERE (equipamento_id = ? AND tipo_recurso = ? AND status_alocacao = 'Disponível') LIMIT 1)"
    cursor.execute(query, (id, tipo_recurso))
    
    resultado = cursor.fetchone()[0]
    conn.close()

    return bool(resultado)

def alocar(id: int, tipo_recurso: str):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = "UPDATE RecursosRede SET status_alocacao = 'Alocado' WHERE equipamento_id = ? AND tipo_recurso = ?"

    cursor.execute(query, (id, tipo_recurso))

    conn.commit()
    conn.close()

def alocarRecurso():
    request_data = request.get_json()

    equipamento_id = request_data['equipamento_id']
    tipo_recurso = request_data['tipo_recurso']

    res = verificarStatusDoRecurso(equipamento_id, tipo_recurso)

    if res :
        alocar(equipamento_id, tipo_recurso)
        # generateLog(equipamento_id, 'Resource Allocated', '')
        return jsonify({"sucesso": "recurso alocado com sucesso"})
    else:
        return jsonify({"error": "Este recurso já está alocado"}), 401

def desalocarRecurso():
    request_data = request.get_json()

    recurso_id = request_data['recurso_id']

    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = "UPDATE RecursosRede SET status_alocacao = 'Disponível' WHERE id = ?"

    cursor.execute(query, (recurso_id, ))

    conn.commit()
    conn.close()

    return jsonify({"sucesso": "Recurso desalocado com sucesso"})