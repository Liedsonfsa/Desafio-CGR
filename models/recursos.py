import sqlite3 as sql

def buscarRecursosPorID(equipamentoId: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM RecursosRede WHERE equipamento_id = ?'

    cursor.execute(query, (equipamentoId,))

    recursos = cursor.fetchall()

    conn.close()

    return recursos
    
def verificarStatus(id: int, tipo_recurso: str):
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
    

def desalocar(recurso_id: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = "UPDATE RecursosRede SET status_alocacao = 'Disponível' WHERE id = ?"

    cursor.execute(query, (recurso_id, ))

    conn.commit()
    conn.close()

    return {"sucesso": "Recurso desalocado com sucesso"}