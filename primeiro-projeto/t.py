usuarios = [
    {'id': 1, 'nome': 'David', 'email': 'davidvarao@senai.br'},
    {'id': 2, 'nome': 'Geovanni', 'email': 'pizza35reais@senai.br'}
]


# u = None
# for usuario in usuarios:
#     if usuario['id'] == id:
#         u = usuario
id = 3
# reescrever para Pythones
u = [usuario for usuario in usuarios
     if usuario['id']==id]

print(u)
