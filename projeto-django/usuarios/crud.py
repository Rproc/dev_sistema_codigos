# Forma 1: create()
from usuarios.models import Usuario

usuario1 = Usuario.objects.create(
    nome='Raphamel',
    email='rapha@senai.br',
    senha='Flamengo123'
)

print(usuario1)  # Raphamel (rapha@senai.br)
print(usuario1.id)  # 1


# Forma 2: Instanciar e save()
usuario2 = Usuario(
    nome='David',
    email='david@senai.br',
    senha='Varao123'
)
usuario2.save()  # Só aqui que salva no banco!


# Forma 3: get_or_create()
usuario3, criado = Usuario.objects.get_or_create(
    email='geo@vanni.br',
    defaults={
        'nome': 'Geovanni',
        'senha': 'Pizza123'
    }
)

if criado:
    print(f'Criou: {usuario3}')
else:
    print(f'Já existia: {usuario3}')