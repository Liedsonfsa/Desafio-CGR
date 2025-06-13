from flask import jsonify
from models.logs import pegar_logs

def logs():
    try:
        logs = pegar_logs()

        if not logs:
            return jsonify({
                "sucesso": False,
                "message": "Nenhum log encontrado",
                "logs": []
            }), 404

        return jsonify({
            "sucesso": True,
            "message": "Logs recuperados com sucesso",
            "logs": logs
        })
    except Exception as e:
        return jsonify({
            "sucesso": False,
            "message": "Erro interno ao buscar logs",
            "error": str(e)
        }), 500
