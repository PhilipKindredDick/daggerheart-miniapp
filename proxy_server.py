from flask import Flask, request, jsonify
import requests
import json
import random
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Убираем flask_cors полностью и делаем вручную
@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# Тест endpoint для проверки CORS
@app.route('/api/test', methods=['GET', 'POST', 'OPTIONS'])
def test():
    return jsonify({"status": "OK", "message": "CORS работает!"})

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"


@app.route('/api/gm_action', methods=['POST', 'OPTIONS'])
def gm_action():
    # Явно обрабатываем OPTIONS
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    try:
        data = request.json
        action = data.get('action', '')
        character = data.get('character', {})
        game_state = data.get('game_state', {})

        # Формируем промпт для DeepSeek
        system_prompt = """Ты — ИИ гейм-мастер для Daggerheart. 

ОБЯЗАТЕЛЬНО отвечай ТОЛЬКО валидным JSON без дополнительного текста:
{
    "scene_description": "Описание сцены 2-4 предложения",
    "action_suggestions": ["Действие 1", "Действие 2", "Действие 3"],
    "requires_roll": null,
    "location": "Название локации",
    "atmosphere": "Настроение сцены"
}

НЕ добавляй никакого текста до или после JSON. Только чистый JSON."""

        user_prompt = f"""
Персонаж: {character.get('name', 'Неизвестный')}, {character.get('ancestry', '')}, {character.get('class', '')}
Текущая сцена: {game_state.get('scene', 'Начало приключения')}
Действие игрока: {action}

Ответь ТОЛЬКО JSON."""

        # Заглушка для тестирования CORS
        test_response = {
            "scene_description": "Тестовая сцена для проверки связи с ГМ. Ваш персонаж стоит в начале приключения.",
            "action_suggestions": ["Осмотреться вокруг", "Поговорить с НПС", "Пойти вперед"],
            "requires_roll": None,
            "location": "Тестовая локация",
            "atmosphere": "спокойная"
        }

        response = jsonify({"success": True, "data": test_response})
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

    except Exception as e:
        response = jsonify({"success": False, "error": str(e)})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/api/roll_dice', methods=['POST'])
def roll_dice():
    data = request.json
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

@app.route('/api/test_deepseek', methods=['GET'])
def test_deepseek():
    try:
        response = requests.post(DEEPSEEK_URL,
            headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [{"role": "user", "content": "test"}], "max_tokens": 10},
            timeout=10
        )
        return jsonify({"status": response.status_code, "response": response.text})
    except Exception as e:
        return jsonify({"error": str(e)})

print("Текущая директория:", os.getcwd())
print("Файл .env существует:", os.path.exists('.env'))

load_dotenv()

print("Переменная загружена:", os.getenv('DEEPSEEK_API_KEY'))

@app.route('/api/endpoints', methods=['GET'])
def list_endpoints():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append(str(rule))
    return jsonify({"endpoints": routes})

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY не найден в переменных окружения")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)