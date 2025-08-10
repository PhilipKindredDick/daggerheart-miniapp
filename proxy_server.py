from flask import Flask, request, jsonify
import json
import random
import os

app = Flask(__name__)


# Самый простой CORS
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/api/gm_action', methods=['POST', 'OPTIONS'])
def gm_action():
    if request.method == 'OPTIONS':
        return '', 200

    return jsonify({
        "success": True,
        "data": {
            "scene_description": "CORS тест успешен! Персонаж готов к приключению.",
            "action_suggestions": ["Начать", "Исследовать", "Отдохнуть"],
            "requires_roll": None,
            "location": "Стартовая локация",
            "atmosphere": "готовность"
        }
    })


@app.route('/api/roll_dice', methods=['POST', 'OPTIONS'])
def roll_dice():
    if request.method == 'OPTIONS':
        return '', 200

    hope_roll = random.randint(1, 12)
    fear_roll = random.randint(1, 12)

    return jsonify({
        "success": True,
        "data": {
            "hope_dice": hope_roll,
            "fear_dice": fear_roll,
            "modifier": 0,
            "total": max(hope_roll, fear_roll),
            "is_critical": hope_roll == fear_roll,
            "dominant_die": "hope" if hope_roll > fear_roll else "fear"
        }
    })


@app.route('/api/test')
def test():
    return jsonify({"status": "OK"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)