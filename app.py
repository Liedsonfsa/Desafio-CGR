from flask import Flask, jsonify
import sqlite3 as sql

app = Flask(__name__)

@app.route('/equipamentos', methods=['GET'])
def buscarEquipamentos():
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos'

    cursor.execute(query)

    equipamentos = cursor.fetchall()

    return jsonify(equipamentos)

@app.route('/equipamentos/<int:id>', methods=['GET'])
def buscarEquipamentoPorID(id):
    return jsonify({'response': id})

@app.route('/equipamentos/<int:id>/status', methods=['GET'])
def buscarStatusDoEquipamentoPorID(id):
    return jsonify({'response': id})


app.run(host='127.0.0.1', debug=True, port=5000)