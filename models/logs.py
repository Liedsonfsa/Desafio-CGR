import sqlite3 as sql
from database.conexao import conectar

def pegar_logs():
    conn = None
    try:
        conn = conectar()
        cursor = conn.cursor()

        query = 'SELECT * FROM EventosLogs'

        cursor.execute(query)

        return cursor.fetchall()
    except sql.Error as e:
        print(f"Erro ao buscar logs: {e}")
        return []
    finally:
        if conn:
            conn.close()

def gerar_log(equipamentoID: int, tipo_evento: str, descricao: str):
    conn = None
    try:   
        conn = conectar()
        cursor = conn.cursor()

        query = 'INSERT INTO EventosLogs (equipamento_id, tipo_evento, descricao) VALUES (?, ?, ?)'

        cursor.execute(query, (equipamentoID, tipo_evento, descricao))
        conn.commit()
        
        return True
    except sql.Error as e:
        print(f"Erro ao gerar log: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

    