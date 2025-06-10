from flask import Flask
from routes.equipamentos import buscarEquipamentos, buscarEquipamentoPorID, pegarStatusDoEquipamentoPorID
from routes.logs import getLogs
from routes.recursos import buscarRecursosDeUmEquipamentoPorID, alocarRecurso, desalocarRecurso

app = Flask(__name__)

app.add_url_rule('/equipamentos', 'buscarEquipamentos', buscarEquipamentos, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>', 'buscarEquipamentoPorID', buscarEquipamentoPorID, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>/status', 'pegarStatusDoEquipamentoPorID', pegarStatusDoEquipamentoPorID, methods=['PUT'])
app.add_url_rule('/logs', 'logs', getLogs, methods=['GET'])
app.add_url_rule('/equipamentos/<int:equipamentoId>/recursos', 'buscarRecursosDeUmEquipamentoPorID', buscarRecursosDeUmEquipamentoPorID, methods=['GET'])
app.add_url_rule('/recursos/alocar', 'alocarRecurso', alocarRecurso, methods=['POST'])
app.add_url_rule('/recursos/desalocar', 'desalocarRecurso', desalocarRecurso, methods=['POST'])



if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)