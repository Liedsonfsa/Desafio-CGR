import sqlite3 as sql

def buscar_equipamentos():
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos'

    cursor.execute(query)

    equipamentos = cursor.fetchall()

    conn.close()

    return equipamentos

def buscar_equipamento(id: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM EquipamentosRede WHERE id = ?'

    cursor.execute(query, (id,))

    equipamento = cursor.fetchone()
    
    conn.close()

    return equipamento

def atualizar_status(id: int, novo_status: str):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'UPDATE EquipamentosRede SET status = ? WHERE id = ?'

    cursor.execute(query, (novo_status, id))

    conn.commit()

    conn.close()

def buscar_recursos(equipamento_id: int):
    conn = sql.connect('equipamentos.db')
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

    conn.close()
    
    if not recursos:
        return {
            "success": False,
            "message": f"Equipamento {equipamento_id} não possui recursos"
        }
    
    return recursos