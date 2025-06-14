from flasgger import swag_from
from datetime import datetime
from service.analise import analise

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
              example: "Switch Principal"
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
                    example: "Porta Ethernet"
                  valor_recurso:
                    type: string
                    example: "Eth0/2"
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
    resultado = {
        'equipamento_id': equipamento_id,
        'timestamp_analise': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    try:
        resultado_analise = analise(equipamento_id)
        resultado.update(resultado_analise)
        return resultado
    except Exception as e:
        resultado['erro'] = f"Erro inesperado: {str(e)}"
        return resultado