from flask import Flask, jsonify
from routes.equipamentos import buscarEquipamentos, buscarEquipamentoPorID, pegarStatusDoEquipamentoPorID

app = Flask(__name__)

app.add_url_rule('/equipamentos', 'buscarEquipamentos', buscarEquipamentos, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>', 'buscarEquipamentoPorID', buscarEquipamentoPorID, methods=['GET'])
app.add_url_rule('/equipamentos/<int:id>/status', 'pegarStatusDoEquipamentoPorID', pegarStatusDoEquipamentoPorID, methods=['GET'])


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)