import requests

BASE_URL = "http://127.0.0.1:5000"

payload = {
        "nome": "Carlos Henrique",
        "email": "carlos.henrique@senai.br",
        "senha": "Coquinha0"
    }

p2 = {
        "email": "raphamengo@senai.br",
        "senha": "Flamengo2019"
}
resposta = requests.post(f"{BASE_URL}/login", 
                         json=p2)
print("Status:", resposta.status_code)
print("Resposta:", resposta.json())
                                                                                                                                                                                                                                                                                                   