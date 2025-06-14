from flask import jsonify
from models.logs import pegar_logs
from flasgger import swag_from

def logs():
  """
    Obtém todos os logs do sistema
    ---
    tags:
      - Logs
    responses:
      200:
        description: Lista de logs
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Logs recuperados com sucesso"
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  equipamento_id:
                    type: integer
                    example: 5
                  tipo_evento:
                    type: string
                    example: "Status Change"
                  descricao:
                    type: string
                    example: "Equipamento atualizado"
                  data_hora:
                    type: string
                    format: date-time
                    example: "2023-05-20 14:30:00"
      404:
        description: Nenhum log encontrado
      500:
        description: Erro interno do servidor
    """
  try:
      logs = pegar_logs()

      if not logs:
          return jsonify({
              "sucesso": False,
              "message": "Nenhum log encontrado",
              "logs": []
          }), 404

      return jsonify({
          "sucesso": True,
          "message": "Logs recuperados com sucesso",
          "logs": logs
      })
  except Exception as e:
      return jsonify({
          "sucesso": False,
          "message": "Erro interno ao buscar logs"
      }), 500
