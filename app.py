from flask import Flask
from routes.equipamentos import buscarEquipamentos, buscarEquipamentoPorID, pegarStatusDoEquipamentoPorID
from routes.logs import getLogs

app = Flask(__name__)

app.add_url_rule('/equipamentos', 'buscarEquipamentos', buscarEquipamentos, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>', 'buscarEquipamentoPorID', buscarEquipamentoPorID, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>/status', 'pegarStatusDoEquipamentoPorID', pegarStatusDoEquipamentoPorID, methods=['GET'])
app.add_url_rule('/logs', 'logs', getLogs, methods=['GET'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)