from flask import Flask, request, jsonify, make_response
import requests
import json
import random
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Middleware для CORS
@app.before_request
def handle_options():
    if request.method == "OPTIONS":
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add('Access-Control-Allow-Headers', "*")
        response.headers.add('Access-Control-Allow-Methods', "*")
        return response


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

if not DEEPSEEK_API_KEY:
    print("ОШИБКА: DEEPSEEK_API_KEY не найден!")
    exit(1)


@app.route('/api/test', methods=['GET', 'POST'])
def test():
    return jsonify({"status": "OK", "message": "CORS работает!"})


@app.route('/api/gm_action', methods=['POST'])
def gm_action():
    try:
        # Тестовый ответ без API
        test_response = {
            "scene_description": "Тест CORS: Ваш персонаж начинает приключение в таверне.",
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