from flask import jsonify, request
from models.equipamentos import buscar_equipamentos, buscar_equipamento, atualizar_status, buscar_recursos
from models.logs import gerar_log
from models.recursos import setar_status_falha
from random import sample, choice

def buscar_todos_equipamentos():
    """
    Retorna todos os equipamentos cadastrados no sistema
    ---
    tags:
      - Equipamentos
    summary: Lista todos os equipamentos
    description: |
      Este endpoint retorna uma lista completa de todos os equipamentos registrados no sistema,
      incluindo seus detalhes como ID, nome, status e outras informações relevantes.
      
      **Observações**:
      - Retorna array vazio se não houver equipamentos cadastrados
      - A lista é ordenada por ID de equipamento
    produces:
      - application/json
    responses:
      200:
        description: Lista de equipamentos retornada com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    description: ID único do equipamento
                    example: 1
                  nome:
                    type: string
                    description: Nome descritivo do equipamento
                    example: "Servidor Principal"
                  tipo:
                    type: string
                    description: Tipo/categoria do equipamento
                    example: "Servidor"
                  status:
                    type: string
                    description: Status atual do equipamento
                    example: "Ativo"
                  ultima_atualizacao:
                    type: string
                    format: date-time
                    description: Data/hora da última atualização
                    example: "2023-05-20T14:30:00Z"
      404:
        description: Nenhum equipamento encontrado
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Equipamento não encontrado"
      500:
        description: Erro interno no servidor
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Erro interno ao buscar equipamentos"
    """
    try:
        equipamentos = buscar_equipamentos()

        if equipamentos is None or equipamentos == []:
            return jsonify({"error": "Equipamento não encontrado"}), 404
        else:
            return jsonify(equipamentos)
    except Exception as e:
        return jsonify({"error": "Erro interno ao buscar equipamentos"}), 500

def buscar_equipamento_por_ID(id: int):
    """
    Busca um equipamento pelo ID
    ---
    tags:
      - Equipamentos
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID do equipamento
    responses:
      200:
        description: Dados do equipamento
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            message:
              type: string
              example: "Equipamento encontrado"
            data:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                nome:
                  type: string
                  example: "Servidor Principal"
                status:
                  type: string
                  example: "Ativo"
      404:
        description: Equipamento não encontrado
      500:
        description: Erro interno do servidor
    """
    try:
        equipamento = buscar_equipamento(id)

        if equipamento is None or equipamento == []:
            return jsonify({"error": "Recurso não encontrado"}), 404
        else:
            return jsonify(equipamento)
    except Exception as e:
        return jsonify({"error": "Erro interno ao buscar equipamento"}), 500

def alterar_status_equipamento(id: int):
    try:
        request_data = request.get_json()

        novo_status = request_data['status']
        descricao = request_data['descricao']

        if not atualizar_status(id, novo_status):
            return jsonify({"error": "Falha ao atualizar status"}), 500
        
        if not gerar_log(id, 'Status Change', descricao):
            return jsonify({"error": "Falha ao gerar o log"}), 500

        return jsonify(
            {
                "equipamento_id": id,
                "novo_status": novo_status, 
                "tipo_evento": 'Status Change',
                "descricao": descricao
            }
        )
    except Exception as e:
        return jsonify({"error": "Erro interno ao alterar status"}), 500

def simular_falha(equipamento_id: int):
    try:
        recursos = buscar_recursos(equipamento_id)

        if not recursos:
            return jsonify({
                "success": False,
                "message": "Nenhum recurso encontrado para o equipamento"
            }), 404

        num_falhas = max(1, round(len(recursos) * 0.3))
        recursos_afetados = sample(recursos, num_falhas)

        falhas_possiveis = ['Indisponível', 'Com Problema']

        for recurso_id, valor_recurso in recursos_afetados:
            novo_status = choice(falhas_possiveis)

            setar_status_falha(novo_status, recurso_id)

            descricao = f"Recurso {valor_recurso} marcado como {novo_status} (simulação)"

            gerar_log(equipamento_id, 'Failure', descricao)
        
        return jsonify({
            "success": True,
            "message": f"Simulação de falha concluída. {num_falhas} recursos afetados.",
            "equipamento_id": equipamento_id,
            "recursos_afetados": len(recursos_afetados)
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": "Erro durante a simulação de falha"
        }), 500
