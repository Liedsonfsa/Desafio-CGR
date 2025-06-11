from flask import jsonify, request
from models.equipamentos import buscar, buscarPorID, alterarStatusPorID
from models.logs import generateLog

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
