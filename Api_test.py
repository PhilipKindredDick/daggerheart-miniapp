import requests

url = "https://api.deepseek.com/v1/chat/completions"
api_key = "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"

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