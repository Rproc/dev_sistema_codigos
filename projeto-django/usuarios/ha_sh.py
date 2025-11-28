from django.contrib.auth.hashers import make_password, check_password

# Teste 1: Criar hash
hash1 = make_password("senha123")
print(f"Hash: {hash1}")

# Teste 2: Verificar senha correta
correto = check_password("senha123", hash1)
print(f"Senha correta? {correto}")  # True

# Teste 3: Verificar senha errada
errado = check_password("senha456", hash1)
print(f"Senha errada? {errado}")  # False

# Teste 4: Mesmo senha, hashes diferentes (por causa do salt)
hash2 = make_password("senha123")
print(f"Hash1: {hash1}")
print(f"Hash2: {hash2}")
print(f"São iguais? {hash1 == hash2}")  # False!
# Mas ambos validam a mesma senha!