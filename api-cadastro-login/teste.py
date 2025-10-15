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



# resposta = requests.post(f"{BASE_URL}/login", 
#                          json=p2)
# print("Status:", resposta.status_code)
# print("Resposta:", resposta.json())


# ------------------------
# deletar
# resposta = requests.delete(f"{BASE_URL}/usuarios/1")
# print("Status:", resposta.status_code)
# print("Resposta:", resposta.json())

resposta = requests.get(f"{BASE_URL}/usuarios")
print("Status:", resposta.status_code)
print("Resposta:", resposta.json())

resposta = requests.patch(f"{BASE_URL}/usuarios/1",
        json={'email': 'raphaelflu@senai.br'})
print("Status:", resposta.status_code)
print("Resposta:", resposta.json())