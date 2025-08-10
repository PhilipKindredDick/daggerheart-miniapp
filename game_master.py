import asyncio
import json
from openai import OpenAI
from typing import Dict, List, Optional
import random

class DaggerheartGM:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key="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",
            base_url="https://api.deepseek.com"
        )
        self.game_state = {
            "scene": "",
            "location": "",
            "npcs": [],
            "current_challenge": None,
            "player_character": None,
            "game_log": []
        }
        
    async def initialize_game(self, character_data: Dict):
        """Инициализация игры с персонажем"""
        self.game_state["player_character"] = character_data
        
        # Генерируем начальную сцену
        response = await self._call_deepseek([
            {
                "role": "system", 
                "content": self._get_system_prompt()
            },
            {
                "role": "user",
                "content": f"Начни новую игру для персонажа: {character_data['name']}, {character_data['ancestry']}, {character_data['class']}. Создай начальную сцену."
            }
        ])
        
        return self._parse_gm_response(response)
    
    async def process_player_action(self, action: str) -> Dict:
        """Обработка действия игрока"""
        # Добавляем действие в лог
        self.game_state["game_log"].append({
            "type": "player_action",
            "content": action,
            "timestamp": "now"
        })
        
        # Определяем нужна ли проверка
        needs_roll = await self._check_if_roll_needed(action)
        
        if needs_roll:
            return await self._handle_skill_check(action, needs_roll)
        else:
            return await self._continue_narrative(action)
    
    async def _call_deepseek(self, messages: List[Dict]) -> str:
        """Вызов DeepSeek API"""
        try:
            response = self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Ошибка ИИ: {str(e)}"
    
    def _get_system_prompt(self) -> str:
        return """
        Ты — доброжелательный, гибкий, но требовательный гейм-мастер для Daggerheart.
        
        Цели: 
        - Поддерживать темп игры
        - Предлагать содержательные выборы
        - Уважать принципы "линии и вето"
        - Быть честным с бросками и правилами
        
        НИКОГДА не выдумывай результаты бросков — всегда используй системные функции.
        
        Формат ответа (JSON):
        {
            "scene_description": "Короткое описание сцены (2-4 предложения)",
            "action_suggestions": ["Вариант 1", "Вариант 2", "Вариант 3"],
            "requires_roll": null или {"trait": "strength", "difficulty": 12, "reason": "описание"},
            "location": "Название локации",
            "gm_notes": "Внутренние заметки ГМ"
        }
        
        Всегда отвечай только в этом JSON формате.
        """
    
    def roll_dice(self, trait_modifier: int = 0) -> Dict:
        """Бросок кубиков дуальности"""
        hope_roll = random.randint(1, 12)
        fear_roll = random.randint(1, 12)
        
        result = {
            "hope_dice": hope_roll,
            "fear_dice": fear_roll,
            "modifier": trait_modifier,
            "total": max(hope_roll, fear_roll) + trait_modifier,
            "is_critical": hope_roll == fear_roll,
            "dominant_die": "hope" if hope_roll > fear_roll else "fear" if fear_roll > hope_roll else "critical"
        }
        
        return result
    
    async def _check_if_roll_needed(self, action: str) -> Optional[Dict]:
        """Определяет нужна ли проверка для действия"""
        response = await self._call_deepseek([
            {
                "role": "system",
                "content": "Определи, нужна ли проверка характеристики для действия игрока. Ответь JSON: {\"needs_roll\": true/false, \"trait\": \"strength/agility/etc\", \"difficulty\": 12, \"reason\": \"почему\"}"
            },
            {
                "role": "user", 
                "content": f"Действие игрока: {action}"
            }
        ])
        
        try:
            return json.loads(response)
        except:
            return None

# Веб-сервер Flask для связи с фронтендом
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

gm = DaggerheartGM("your_deepseek_api_key")

@app.route('/api/start_game', methods=['POST'])
async def start_game():
    character_data = request.json
    result = await gm.initialize_game(character_data)
    return jsonify(result)

@app.route('/api/player_action', methods=['POST'])
async def player_action():
    action = request.json['action']
    result = await gm.process_player_action(action)
    return jsonify(result)

@app.route('/api/roll_dice', methods=['POST'])
def roll_dice():
    data = request.json
    trait_mod = data.get('trait_modifier', 0)
    result = gm.roll_dice(trait_mod)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)