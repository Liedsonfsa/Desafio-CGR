from flask import Flask
from controllers.equipamentos import buscarEquipamentos, buscarEquipamentoPorID, alterarStatusDoEquipamento, simularFalha
from controllers.logs import getLogs
from controllers.recursos import buscarRecursosDeUmEquipamentoPorID, alocarRecurso, desalocarRecurso, alocarInteligentemente
from service.analisar_gargalos import analisar_gargalos

app = Flask(__name__)

app.add_url_rule('/equipamentos', 'buscarEquipamentos', buscarEquipamentos, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>', 'buscarEquipamentoPorID', buscarEquipamentoPorID, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>/status', 'pegarStatusDoEquipamentoPorID', alterarStatusDoEquipamento, methods=['PUT'])
app.add_url_rule('/logs', 'logs', getLogs, methods=['GET'])
app.add_url_rule('/equipamentos/<int:equipamentoId>/recursos', 'buscarRecursosDeUmEquipamentoPorID', buscarRecursosDeUmEquipamentoPorID, methods=['GET'])
app.add_url_rule('/recursos/alocar', 'alocarRecurso', alocarRecurso, methods=['POST'])
app.add_url_rule('/recursos/desalocar', 'desalocarRecurso', desalocarRecurso, methods=['POST'])
app.add_url_rule('/recursos/melhor-recurso', 'alocarInteligentemente', alocarInteligentemente, methods=['GET'])
app.add_url_rule('/equipamentos/<int:equipamento_id>/simular-falha', 'simularFalha', simularFalha, methods=['POST'])
app.add_url_rule('/analisar-gargalos/<int:equipamento_id>', 'analisar-gargalos', analisar_gargalos, methods=['GET'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)