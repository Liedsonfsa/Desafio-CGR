import sqlite3 as sql
from database.conexao import conectar
from service.notificacoes import notificar_equipamento_offline

def buscar_equipamentos():
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = 'SELECT * FROM EquipamentosRede'

        cursor.execute(query)

        return cursor.fetchall()
    except sql.Error as e:
        print(f"Erro ao buscar equipamentos: {e}")
        return []
    finally:
        if conn:
            conn.close()

def buscar_equipamento(id: int):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = 'SELECT * FROM EquipamentosRede WHERE id = ?'

        cursor.execute(query, (id,))

        return cursor.fetchone()
    except sql.Error as e:
        print(f"Erro ao buscar equipamento ID {id}: {e}")
        return None
    finally:
        if conn:
            conn.close()

def atualizar_status(id: int, novo_status: str):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = 'SELECT status FROM EquipamentosRede WHERE id = ?'
        cursor.execute(query, (id, ))
        status_anterior = cursor.fetchone()[0]

        query = 'UPDATE EquipamentosRede SET status = ? WHERE id = ?'

        cursor.execute(query, (novo_status, id))

        conn.commit()

        if status_anterior != "Offline" and novo_status == "Offline":
            notificar_equipamento_offline(id)
        return True
    except sql.Error as e:
        print(f"Erro ao atualizar status do equipamento ID {id}: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def buscar_recursos(equipamento_id: int):
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()
    
        cursor.execute("SELECT id FROM EquipamentosRede WHERE id = ?", (equipamento_id,))
        equipamento = cursor.fetchone()
        if not equipamento:
            return {
                "success": False,
                "message": f"Equipamento com ID {equipamento_id} não encontrado"
            }
        
        cursor.execute("SELECT id, valor_recurso FROM RecursosRede WHERE equipamento_id = ?",(equipamento_id,))
        recursos = cursor.fetchall()
    
        if not recursos:
            return {
                "sucesso": False,
                "message": f"Equipamento {equipamento_id} não possui recursos"
            }
        
        return recursos
    except sql.Error as e:
        print(f"Erro ao buscar recursos do equipamento ID {equipamento_id}: {e}")
        return {
            "success": False,
            "message": "Erro interno ao buscar recursos"
        }
    finally:
        if conn:
            conn.close()