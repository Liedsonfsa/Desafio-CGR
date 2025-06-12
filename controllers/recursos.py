from flask import jsonify, request
from models.recursos import buscarRecursosPorID, verificarStatus, alocar, desalocar, alocacaoInteligente
from models.logs import generateLog

def buscarRecursosDeUmEquipamentoPorID(equipamentoId: int):
    recursos = buscarRecursosPorID(equipamentoId)

    if recursos is None or recursos == []:
        return jsonify({"error": "Recurso não encontrado"}), 404
    else:
        return jsonify(recursos)

def alocarRecurso():
    request_data = request.get_json()

    equipamento_id = request_data['equipamento_id']
    tipo_recurso = request_data['tipo_recurso']

    existe = verificarStatus(equipamento_id, tipo_recurso)

    if existe :
        alocar(equipamento_id, tipo_recurso)
        generateLog(equipamento_id, 'Resource Allocated', f'{tipo_recurso} alocado')
        return jsonify({"sucesso": "recurso alocado com sucesso"})
    else:
        return jsonify({"error": "Este recurso já está alocado"}), 401

def desalocarRecurso():
    recurso_id = request.args.get('recurso_id')

    response = desalocar(recurso_id['recurso_id'])
    generateLog(recurso_id, 'Resource Deallocated', 'Recurso desalocado')

    return jsonify(response)

def alocarInteligentemente():

    tipo_recurso = request.get_json('tipo_recurso')
    equipamento_id = request.get_json('equipamento_id')

    response = alocacaoInteligente(str(tipo_recurso['tipo_recurso']), equipamento_id)

    return jsonify(response)