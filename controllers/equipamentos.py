from flask import jsonify, request
from models.equipamentos import buscar_equipamentos, buscar_equipamento, atualizar_status, buscar_recursos
from models.logs import gerar_log
from models.recursos import setar_status_falha
from random import sample, choice

def buscar_todos_equipamentos():
    try:
        equipamentos = buscar_equipamentos()

        if equipamentos is None or equipamentos == []:
            return jsonify({"error": "Equipamento não encontrado"}), 404
        else:
            return jsonify(equipamentos)
    except Exception as e:
        return jsonify({"error": "Erro interno ao buscar equipamentos"}), 500

def buscar_equipamento_por_ID(id: int):
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
