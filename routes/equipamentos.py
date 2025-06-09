from flask import jsonify
import sqlite3 as sql

def buscarEquipamentos():
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos'

    cursor.execute(query)

    equipamentos = cursor.fetchall()

    return jsonify(equipamentos)

def buscarEquipamentoPorID(id: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT * FROM equipamentos WHERE id = ?'

    cursor.execute(query, (id,))

    equipamento = cursor.fetchone()

    return jsonify(equipamento)

def pegarStatusDoEquipamentoPorID(id: int):
    conn = sql.connect('equipamentos.db')
    cursor = conn.cursor()

    query = 'SELECT status FROM equipamentos WHERE id = ?'

    cursor.execute(query, (id,))

    equipamento = cursor.fetchone()

    return jsonify(equipamento)