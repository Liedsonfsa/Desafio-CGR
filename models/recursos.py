import sqlite3 as sql
from datetime import datetime
from database.conexao import conectar

def buscar_recursos_por_id(equipamentoId: int):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = 'SELECT * FROM RecursosRede WHERE equipamento_id = ?'

        cursor.execute(query, (equipamentoId,))

        return cursor.fetchall()
    except sql.Error as e:
        return {"error": f'Error ao buscar recursos: {e}'}
    finally:
        conn.close()

    
def verificar_status(id: int, tipo_recurso: str):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = "SELECT EXISTS(SELECT 1 FROM RecursosRede WHERE (equipamento_id = ? AND tipo_recurso = ? AND status_alocacao = 'Disponível') LIMIT 1)"
        cursor.execute(query, (id, tipo_recurso))
        
        return bool(cursor.fetchone()[0])
    except:
        return False
    finally:
        conn.close()

def alocar(id: int, tipo_recurso: str):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = "UPDATE RecursosRede SET status_alocacao = 'Alocado' WHERE equipamento_id = ? AND tipo_recurso = ?"

        cursor.execute(query, (id, tipo_recurso))

        conn.commit()
    except sql.Error as e:
        print(f"Erro ao alocar recurso: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()
    
def desalocar(recurso_id: int):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = "UPDATE RecursosRede SET status_alocacao = 'Disponível' WHERE id = ?"

        cursor.execute(query, (recurso_id, ))
        conn.commit()

        return {"sucesso": "Recurso desalocado com sucesso"}
    except sql.Error as e:
        print(f"Erro ao desalocar recurso: {e}")
        if conn:
            conn.rollback()
        return {"erro": "Falha ao desalocar recurso"}
    finally:
        if conn:
            conn.close()

def alocacao_inteligente(tipo_recurso: str, equipamento_id: any):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = ""
        params = ()

        if isinstance(equipamento_id, dict):
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
        else:
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
                "message": "Nenhum recurso disponível encontrado para os critérios informados"
            }
        
        if len(recurso) == 2:
            recurso_id, valor_recurso = recurso
            equip_id = equipamento_id['equipamento_id']
        else:
            recurso_id, equip_id, valor_recurso = recurso
        
        return {
            "success": True,
            "recurso_id": recurso_id,
            "equipamento_id": equip_id,
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
        if conn:
            conn.close()

def setar_status_falha(novo_status: str, recurso_id: int):
    conn = None
    try:
        conn = sql.connect('equipamentos.db')
        cursor = conn.cursor()

        cursor.execute(
        "UPDATE RecursosRede SET status_alocacao = ?, ultima_atualizacao = ? WHERE id = ?",
        (novo_status, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), recurso_id)
        )

        conn.commit()
    except sql.Error as e:
        print(f"Erro ao atualizar status: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()