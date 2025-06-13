import sqlite3
from datetime import datetime
from flasgger import swag_from

def analisar_gargalos(equipamento_id: int):
    """
    ---
    tags:
      - Análise
    summary: Analisa gargalos em um equipamento
    description: |
      Identifica recursos problemáticos em um equipamento específico e calcula métricas de saúde.
      
      **Métricas calculadas**:
      - Total de recursos
      - Recursos com problemas
      - Porcentagem de problemas
      - Lista detalhada de recursos problemáticos
      - Alertas críticos (quando >30% de recursos com problemas)
    parameters:
      - name: equipamento_id
        in: path
        type: integer
        required: true
        description: ID do equipamento a ser analisado
        example: 1
    responses:
      200:
        description: Análise realizada com sucesso
        schema:
          type: object
          properties:
            equipamento_id:
              type: integer
              example: 1
            nome_equipamento:
              type: string
              example: "Servidor Principal"
            total_recursos:
              type: integer
              example: 10
            recursos_problematicos:
              type: integer
              example: 3
            porcentagem_problemas:
              type: string
              example: "30.00%"
            alerta:
              type: string
              example: "CRÍTICO: Mais de 30% dos recursos com problemas"
            lista_problemas:
              type: array
              items:
                type: object
                properties:
                  recurso_id:
                    type: integer
                    example: 5
                  tipo_recurso:
                    type: string
                    example: "CPU"
                  valor_recurso:
                    type: string
                    example: "Intel Xeon 3.5GHz"
                  status:
                    type: string
                    example: "Indisponível"
                  ultima_atualizacao:
                    type: string
                    example: "2023-05-20 14:30:00"
                  dias_sem_atualizacao:
                    type: integer
                    example: 2
            timestamp_analise:
              type: string
              example: "2023-05-22 10:15:00"
      404:
        description: Equipamento não encontrado
        schema:
          type: object
          properties:
            equipamento_id:
              type: integer
              example: 999
            erro:
              type: string
              example: "Equipamento não encontrado"
            timestamp_analise:
              type: string
              example: "2023-05-22 10:15:00"
      500:
        description: Erro interno no servidor
        schema:
          type: object
          properties:
            equipamento_id:
              type: integer
              example: 1
            erro:
              type: string
              example: "Erro inesperado: could not connect to database"
            timestamp_analise:
              type: string
              example: "2023-05-22 10:15:00"
    """
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