from flask import jsonify, request
from models.recursos import buscar_recursos_por_id, verificarStatus, alocar_recurso, desalocar_recurso, alocacao_inteligente
from models.logs import gerar_log

def buscar_recursos_equipamento(equipamento_id: int):
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
    try:
        request_data = request.get_json()

        if not request_data or 'equipamento_id' not in request_data or 'tipo_recurso' not in request_data:
            return jsonify({
                "sucesso": False,
                "error": "Dados incompletos no request"
        }), 400

        equipamento_id = request_data['equipamento_id']
        tipo_recurso = request_data['tipo_recurso']

        if not verificarStatus(equipamento_id, tipo_recurso):
            return jsonify({
                "sucesso": False,
                "error": "Recurso não disponível para alocação"
            }), 409

        if not alocar_recurso(equipamento_id, tipo_recurso):
            return jsonify({
                "sucesso": False,
                "error": "Falha ao alocar recurso"
            }), 500
        
        gerar_log(equipamento_id, 'Resource Allocated', f'{tipo_recurso} alocado')
        return jsonify({"sucesso": "recurso alocado com sucesso"})
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "error": "Erro interno ao alocar recurso"
        }), 500

def desalocar_recurso():
    try:
        recurso_id = request.args.get('recurso_id')

        if not recurso_id:
            return jsonify({
                "sucesso": False,
                "error": "ID do recurso não fornecido"
            }), 400

        resposta = desalocar_recurso(int(recurso_id))

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