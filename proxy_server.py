from flask import Flask, request, jsonify
import requests
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


# CORS middleware по аналогии с Express.js
@app.before_request
def handle_cors():
    if request.method == "OPTIONS":
        response = jsonify()
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return response


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response


@app.route('/api/test', methods=['GET', 'POST'])
def test():
    return jsonify({"status": "OK", "message": "CORS работает!"})


@app.route('/api/gm_action', methods=['POST'])
def gm_action():
    try:
        test_response = {
            "scene_description": "Тест CORS исправлен: Ваш персонаж в таверне готов к приключениям!",
            "action_suggestions": ["Заказать эль", "Поговорить с барменом", "Осмотреть зал"],
            "requires_roll": None,
            "location": "Таверна",
            "atmosphere": "уютная"
        }
        return jsonify({"success": True, "data": test_response})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/api/roll_dice', methods=['POST'])
def roll_dice():
    data = request.json or {}
    trait_modifier = data.get('trait_modifier', 0)

    hope_roll = random.randint(1, 12)
    fear_roll = random.randint(1, 12)
    total = max(hope_roll, fear_roll) + trait_modifier

    result = {
        "hope_dice": hope_roll,
        "fear_dice": fear_roll,
        "modifier": trait_modifier,
        "total": total,
        "is_critical": hope_roll == fear_roll,
        "dominant_die": "hope" if hope_roll > fear_roll else "fear" if fear_roll > hope_roll else "critical"
    }
    return jsonify({"success": True, "data": result})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)