# CURL

import requests

BASE_URL = "http://127.0.0.1:5000"

payload = {
        "nome": "Carlos Silva",
        "email": "carlos.silva@email.com"
    }
resposta = requests.post(f"{BASE_URL}/usuarios", json=payload)
print("Status:", resposta.status_code)
print("Resposta:", resposta.json())
