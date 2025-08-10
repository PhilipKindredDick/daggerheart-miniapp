from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import random

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = "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"  # Замените на ваш ключ
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
        
СТРОГО отвечай только в JSON формате:
{
    "scene_description": "Описание сцены 2-4 предложения",
    "action_suggestions": ["Действие 1", "Действие 2", "Действие 3"],
    "requires_roll": {"trait": "strength", "difficulty": 12, "reason": "почему"} или null,
    "location": "Название локации",
    "atmosphere": "Настроение сцены"
}

Никогда не делай броски сам - только запрашивай их у системы."""

        user_prompt = f"""
Персонаж: {character.get('name', 'Неизвестный')}, {character.get('ancestry', '')}, {character.get('class', '')}
Текущая сцена: {game_state.get('scene', 'Начало приключения')}
Действие игрока: {action}

Ответь как ГМ в формате JSON."""

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
            gm_text = ai_response['choices'][0]['message']['content']
            
            # Парсим JSON ответ ИИ
            try:
                gm_data = json.loads(gm_text)
                return jsonify({"success": True, "data": gm_data})
            except json.JSONDecodeError:
                # Если ИИ ответил не JSON, оборачиваем в структуру
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)