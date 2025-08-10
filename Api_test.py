import requests

url = "https://api.deepseek.com/v1/chat/completions"
api_key = "sk-078082efd18d4fcfab12318843b36c58"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

data = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "user", "content": "Привет! Ответь одним словом."}
    ],
    "temperature": 0.5
}

response = requests.post(url, json=data, headers=headers)
print(response.json())