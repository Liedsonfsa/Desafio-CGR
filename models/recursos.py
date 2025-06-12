import sqlite3 as sql
from datetime import datetime

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

def alocacaoInteligente(tipo_recurso: str, equipamento_id: any):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    try:
        query = str
        id = 0
        params = tuple
        try:
            id = int(equipamento_id['equipamento_id'])
            query = """
            SELECT id, valor_recurso 
            FROM RecursosRede 
            WHERE (tipo_recurso = ? 
            AND status_alocacao = 'Disponível' AND equipamento_id = ?)
            ORDER BY ultima_atualizacao ASC
            LIMIT 1
            """
            params = (tipo_recurso, id)
        except:
            query = """
            SELECT id, equipamento_id, valor_recurso 
            FROM RecursosRede 
            WHERE tipo_recurso = ? 
            AND status_alocacao = 'Disponível'
            ORDER BY ultima_atualizacao ASC
            LIMIT 1
            """
            params = (tipo_recurso, )
        
        cursor.execute(query, params)
        
        recurso = cursor.fetchone()
        
        if not recurso:
            return {
                "success": False,
                "message": "Nenhum recurso disponível encontrado para os critérios informados",
                "tipo_recurso": tipo_recurso,
            }
        
        if id != 0:
            recurso_id, valor_recurso = recurso
        else:
            recurso_id, id, valor_recurso = recurso
        
        return {
            "success": True,
            "recurso_id": recurso_id,
            "equipamento_id": id,
            "tipo_recurso": tipo_recurso,
            "valor_recurso": valor_recurso,
            "message": "Recurso encontrado",
        }
        
    except sql.Error as e:
        conn.rollback()
        return {
            "success": False,
            "message": f"Erro ao alocar recurso: {str(e)}",
        }
        
    finally:
        conn.close()
    