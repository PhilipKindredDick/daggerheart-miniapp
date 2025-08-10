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


@app.route('/api/gm_action', methods=['POST'])
def gm_action():
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

        # Запрос к DeepSeek
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 600,
            "temperature": 0.7
        }

        response = requests.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=30)

        if response.status_code == 200:
            ai_response = response.json()
            gm_text = ai_response['choices'][0]['message']['content'].strip()

            # Убираем возможные markdown блоки
            if gm_text.startswith('```json'):
                gm_text = gm_text[7:]
            if gm_text.startswith('```'):
                gm_text = gm_text[3:]
            if gm_text.endswith('```'):
                gm_text = gm_text[:-3]

            gm_text = gm_text.strip()

            # Парсим JSON ответ ИИ
            try:
                gm_data = json.loads(gm_text)

                # Исправляем trait если нужно
                if gm_data.get('requires_roll') and 'trait' in gm_data['requires_roll']:
                    trait = gm_data['requires_roll']['trait']
                    # Конвертируем dexterity в agility и другие
                    trait_mapping = {
                        'dexterity': 'agility',
                        'intelligence': 'knowledge',
                        'charisma': 'presence',
                        'wisdom': 'instinct'
                    }
                    if trait in trait_mapping:
                        gm_data['requires_roll']['trait'] = trait_mapping[trait]

                return jsonify({"success": True, "data": gm_data})

            except json.JSONDecodeError as e:
                print(f"JSON parse error: {e}")
                print(f"Raw response: {gm_text}")
                # Fallback
                return jsonify({
                    "success": True,
                    "data": {
                        "scene_description": gm_text,
                        "action_suggestions": ["Продолжить", "Осмотреться", "Поговорить"],
                        "requires_roll": None,
                        "location": "Неизвестная локация",
                        "atmosphere": "загадочная"
                    }
                })
        else:
            return jsonify({"success": False, "error": f"DeepSeek API error: {response.status_code}"})

    except Exception as e:
        print(f"Error in gm_action: {e}")
        return jsonify({"success": False, "error": str(e)})

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

DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')

if not DEEPSEEK_API_KEY:
    raise ValueError("DEEPSEEK_API_KEY не найден в переменных окружения")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)