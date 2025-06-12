from flask import jsonify, request
from models.equipamentos import buscar, buscarPorID, alterarStatusPorID, buscarRecursos
from models.logs import generateLog
from models.recursos import setarStatusDeFalha
from random import sample, choice

def buscarEquipamentos():
    equipamentos = buscar()

    if equipamentos is None or equipamentos == []:
        return jsonify({"error": "Equipamento não encontrado"}), 404
    else:
        return jsonify(equipamentos)

def buscarEquipamentoPorID(id: int):
    equipamento = buscarPorID(id)

    if equipamento is None or equipamento == []:
        return jsonify({"error": "Recurso não encontrado"}), 404
    else:
        return jsonify(equipamento)

def alterarStatusDoEquipamento(id: int):
    request_datas = request.get_json()

    new_status = request_datas['status']
    description = request_datas['descricao']

    alterarStatusPorID(id, new_status)

    generateLog(id, 'Status Change', description)

    return jsonify(
        {
            "equipamento_id": id,
            "novo_status": new_status, 
            "tipo_evento": 'Status Change',
            "descricao": description
        }
    )

def simularFalha(equipamento_id: int):
    recursos = buscarRecursos(equipamento_id)

    num_falhas = max(1, round(len(recursos) * 0.3))
    recursos_afetados = sample(recursos, num_falhas)

    falhas_possiveis = ['Indisponível', 'Com Problema']

    for recurso_id, valor_recurso in recursos_afetados:
        novo_status = choice(falhas_possiveis)

        setarStatusDeFalha(novo_status, recurso_id)

        descricao = f"Recurso {valor_recurso} marcado como {novo_status} (simulação)"

        generateLog(equipamento_id, 'Failure', descricao)
    
    return jsonify({
        "success": True,
        "message": f"Simulação de falha concluída. {num_falhas} recursos afetados.",
        "equipamento_id": equipamento_id,
        "recursos_afetados": len(recursos_afetados)
    }), 200
