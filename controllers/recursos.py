from flask import jsonify, request
from models.recursos import buscar_recursos_por_id, verificar_status, alocar, desalocar, alocacao_inteligente
from models.logs import gerar_log
from flasgger import swag_from

def buscar_recursos_equipamento(equipamento_id: int):
  """
    ---
    tags:
      - Recursos
    summary: Busca recursos de um equipamento
    description: Retorna todos os recursos associados a um equipamento específico
    parameters:
      - name: equipamento_id
        in: path
        type: integer
        required: true
        description: ID do equipamento
    responses:
      200:
        description: Recursos encontrados
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: true
            equipamento_id:
              type: integer
              example: 1
            recursos:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  nome:
                    type: string
                    example: "Porta Ethernet"
                  status:
                    type: string
                    example: "Disponível"
      404:
        description: Nenhum recurso encontrado
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Nenhum recurso encontrado para este equipamento"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Erro interno ao buscar recursos"
    """
  try:
      recursos = buscar_recursos_por_id(equipamento_id)

      if not recursos:
          return jsonify({
              "sucesso": False,
              "error": "Nenhum recurso encontrado para este equipamento"
          }), 404

      
      return jsonify({
          "sucesso": True,
          "equipamento_id": equipamento_id,
          "recursos": recursos
      })
  
  except Exception as e:
      return jsonify({
          "sucesso": False,
          "error": "Erro interno ao buscar recursos"
      }), 500

def alocar_recurso():
    """
    ---
    tags:
      - Recursos
    summary: Aloca um recurso
    description: Aloca um recurso específico de um equipamento
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - equipamento_id
            - tipo_recurso
          properties:
            equipamento_id:
              type: integer
              example: 1
            tipo_recurso:
              type: string
              example: "Porta Ethernet"
    responses:
      200:
        description: Recurso alocado com sucesso
        schema:
          type: object
          properties:
            sucesso:
              type: string
              example: "recurso alocado com sucesso"
      400:
        description: Dados incompletos
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Dados incompletos no request"
      409:
        description: Recurso não disponível
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Recurso não disponível para alocação"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Erro interno ao alocar recurso"
    """
    try:
        request_data = request.get_json()

        if not request_data or 'equipamento_id' not in request_data or 'tipo_recurso' not in request_data:
            return jsonify({
                "sucesso": False,
                "error": "Dados incompletos no request"
        }), 400

        equipamento_id = int(request_data['equipamento_id'])
        tipo_recurso = str(request_data['tipo_recurso'])

        if not verificar_status(equipamento_id, tipo_recurso):
            return jsonify({
                "sucesso": False,
                "error": "Recurso não disponível para alocação"
            }), 409

        if not alocar(equipamento_id, tipo_recurso):
            return jsonify({
                "sucesso": False,
                "error": "Falha ao alocar recurso"
            }), 500
        
        gerar_log(equipamento_id, 'Resource Allocated', f'{tipo_recurso} alocado')
        return jsonify({"sucesso": "recurso alocado com sucesso"})
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": f"Erro interno ao alocar recurso: {e}",
        }), 500

def desalocar_recurso():
    """
    ---
    tags:
      - Recursos
    summary: Desaloca um recurso
    description: Desaloca um recurso previamente alocado
    parameters:
      - name: recurso_id
        in: query
        type: integer
        required: true
        description: ID do recurso a ser desalocado
    responses:
      200:
        description: Recurso desalocado com sucesso
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: true
            message:
              type: string
              example: "Recurso desalocado com sucesso"
            recurso_id:
              type: integer
              example: 1
      400:
        description: ID não fornecido
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "ID do recurso não fornecido"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Erro interno ao desalocar recurso"
    """
    try:
        recurso_id = request.args.get('recurso_id')

        if not recurso_id:
            return jsonify({
                "sucesso": False,
                "error": "ID do recurso não fornecido"
            }), 400

        resposta = desalocar(int(recurso_id))

        if not resposta.get('sucesso'):
            return jsonify({
                "sucesso": False,
                "error": resposta.get('mensagem', 'Falha ao desalocar recurso')
            }), 500
        
        gerar_log(recurso_id, 'Resource Deallocated', f'Recurso ID {recurso_id} desalocado')

        return jsonify({
            "sucesso": True,
            "message": "Recurso desalocado com sucesso",
            "recurso_id": recurso_id
        })
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": "Erro interno ao desalocar recurso"
        }), 500

def alocar_inteligentemente():
    """
    ---
    tags:
      - Recursos
    summary: Alocação inteligente de recurso
    description: Encontra e aloca o melhor recurso disponível para a necessidade
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - tipo_recurso
          properties:
            tipo_recurso:
              type: string
              example: "Porta Ethernet"
            equipamento_id:
              type: integer
              example: 1
              required: false
    responses:
      200:
        description: Recurso alocado com sucesso
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            recurso_id:
              type: integer
              example: 1
            equipamento_id:
              type: integer
              example: 1
            tipo_recurso:
              type: string
              example: "Porta Ethernet"
            valor_recurso:
              type: string
              example: "Eth0/1"
            message:
              type: string
              example: "Recurso encontrado"
      400:
        description: Tipo de recurso não especificado
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Tipo de recurso não especificado"
      404:
        description: Nenhum recurso disponível
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            message:
              type: string
              example: "Nenhum recurso disponível encontrado"
      500:
        description: Erro interno
        schema:
          type: object
          properties:
            sucesso:
              type: boolean
              example: false
            error:
              type: string
              example: "Erro interno na alocação inteligente"
    """
    try:
        request_data = request.get_json()

        if not request_data or 'tipo_recurso' not in request_data:
            return jsonify({
                "sucesso": False,
                "error": "Tipo de recurso não especificado"
            }), 400
        
        tipo_recurso = request_data['tipo_recurso']
        equipamento_id = request_data.get('equipamento_id')

        resultado = alocacao_inteligente(tipo_recurso, equipamento_id)

        if not resultado.get('success'):
            return jsonify(resultado), 404
        
        gerar_log(
            resultado.get('equipamento_id'),
            'Resource Allocated',
            f'Recurso {resultado.get("recurso_id")} alocado inteligentemente'
        )

        return jsonify(resultado)
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": "Erro interno na alocação inteligente"
        }), 500