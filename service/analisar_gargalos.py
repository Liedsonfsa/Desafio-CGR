import sqlite3
from datetime import datetime

def analisar_gargalos(equipamento_id: int):
    conn = sqlite3.connect('equipamentos.db')
    cursor = conn.cursor()
    
    resultado = {
        'equipamento_id': equipamento_id,
        'total_recursos': 0,
        'recursos_problematicos': 0,
        'lista_problemas': [],
        'timestamp_analise': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        cursor.execute("SELECT nome FROM EquipamentosRede WHERE id = ?", (equipamento_id,))
        equipamento = cursor.fetchone()
        
        if not equipamento:
            resultado['erro'] = "Equipamento não encontrado"
            return resultado
        
        resultado['nome_equipamento'] = equipamento[0]
        
        cursor.execute("""
            SELECT COUNT(*) 
            FROM RecursosRede 
            WHERE equipamento_id = ?
        """, (equipamento_id,))
        resultado['total_recursos'] = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT id, tipo_recurso, valor_recurso, status_alocacao, ultima_atualizacao
            FROM RecursosRede
            WHERE equipamento_id = ?
              AND status_alocacao IN ('Indisponível', 'Com Problema')
            ORDER BY ultima_atualizacao DESC
        """, (equipamento_id,))
        
        recursos_problematicos = cursor.fetchall()
        resultado['recursos_problematicos'] = len(recursos_problematicos)
        
        if resultado['total_recursos'] > 0:
            porcentagem = (resultado['recursos_problematicos'] / resultado['total_recursos']) * 100
            resultado['porcentagem_problemas'] = f"{porcentagem:.2f}%"
            
            if porcentagem > 30:
                resultado['alerta'] = "CRÍTICO: Mais de 30% dos recursos com problemas"
        
        for recurso in recursos_problematicos:
            id_recurso, tipo, valor, status, ultima_atualizacao = recurso
            
            resultado['lista_problemas'].append({
                'recurso_id': id_recurso,
                'tipo_recurso': tipo,
                'valor_recurso': valor,
                'status': status,
                'ultima_atualizacao': ultima_atualizacao,
                'dias_sem_atualizacao': (datetime.now() - datetime.strptime(ultima_atualizacao, "%Y-%m-%d %H:%M:%S")).days
            })
        
        return resultado
    
    except Exception as e:
        resultado['erro'] = f"Erro inesperado: {str(e)}"
        return resultado
    
    finally:
        conn.close()