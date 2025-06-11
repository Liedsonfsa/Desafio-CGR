import sqlite3 as sql

def buscar():
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos'

    cursor.execute(query)

    equipamentos = cursor.fetchall()

    conn.close()

    return equipamentos

def buscarPorID(id: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos WHERE id = ?'

    cursor.execute(query, (id,))

    equipamento = cursor.fetchone()
    
    conn.close()

    return equipamento

def alterarStatusPorID(id: int, new_status: str):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'UPDATE equipamentos SET status = ? WHERE id = ?'

    cursor.execute(query, (new_status, id))

    conn.commit()

    conn.close()