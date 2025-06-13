from flask import Flask
from flasgger import Swagger
from controllers.equipamentos import buscar_todos_equipamentos, buscar_equipamento_por_ID, alterar_status_equipamento, simular_falha
from controllers.logs import logs
from controllers.recursos import buscar_recursos_por_id, alocar_recurso, desalocar_recurso, alocar_inteligentemente
from service.analisar_gargalos import analisar_gargalos

app = Flask(__name__)

app.config['SWAGGER'] = {
    'title': 'API de Gerenciamento de Equipamentos',
    'version': '1.0',
    'description': 'API para gerenciar recursos de rede',
    'uiversion': 3
}
swagger = Swagger(app)

app.add_url_rule('/equipamentos', view_func=buscar_todos_equipamentos, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>', 'buscarEquipamentoPorID', buscar_equipamento_por_ID, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>/status', 'pegarStatusDoEquipamentoPorID', alterar_status_equipamento, methods=['PUT'])
app.add_url_rule('/logs', view_func=logs, methods=['GET'])
app.add_url_rule('/equipamentos/<int:equipamentoId>/recursos', 'buscarRecursosDeUmEquipamentoPorID', buscar_equipamento_por_ID, methods=['GET'])
app.add_url_rule('/recursos/alocar', 'alocarRecurso', alocar_recurso, methods=['POST'])
app.add_url_rule('/recursos/desalocar', 'desalocarRecurso', desalocar_recurso, methods=['POST'])
app.add_url_rule('/recursos/melhor-recurso', 'alocarInteligentemente', alocar_inteligentemente, methods=['GET'])
app.add_url_rule('/equipamentos/<int:equipamento_id>/simular-falha', 'simularFalha', simular_falha, methods=['POST'])
app.add_url_rule('/analisar-gargalos/<int:equipamento_id>', 'analisar-gargalos', analisar_gargalos, methods=['GET'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)