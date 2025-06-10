from flask import jsonify, request
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

    query = f"SELECT EXISTS(SELECT 1 FROM RecursosRede WHERE (equipamento_id = ? AND tipo_recurso = ? AND status_alocacao = 'Disponível') LIMIT 1)"
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

    # equipamento_id, tipo_recurso e, opcionalmente, cliente_associado
    equipamento_id = request_data['equipamento_id'] # como eu posso fazer uma busca no sqlite3 que me retorne um valor booleano caso uma determinada coluna tenha um determindado valor
    tipo_recurso = request_data['tipo_recurso']

    res = verificarStatusDoRecurso(equipamento_id, tipo_recurso)

    if res :
        alocar(equipamento_id, tipo_recurso)
        return jsonify({"sucesso": "recurso alocado com sucesso"})
    else:
        return jsonify({"error": "Este recurso já está alocado"}), 401
        
    # SELECT * FROM recursos where (equipamento_id = ? && status_alocacao = 'disponível')