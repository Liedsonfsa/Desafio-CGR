from flask import jsonify
from models.logs import get

def getLogs():
    logs = get()

    return jsonify(logs)
