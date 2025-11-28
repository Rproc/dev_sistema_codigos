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
    

#------------------------------

# Listar TODOS
usuarios = Usuario.objects.all()
print(usuarios)  # QuerySet [<Usuario...>, <Usuario...>]

# Contar
print(Usuario.objects.count())  # 3


# Buscar UM (por ID)
usuario = Usuario.objects.get(id=1)
print(usuario.nome)  # Raphamel


# Buscar UM (por email)
usuario = Usuario.objects.get(email='rapha@senai.br')


# Filtrar VÁRIOS
usuarios_raphamel = Usuario.objects.filter(nome='Raphamel')
print(usuarios_raphamel)


# Buscar ou None (não dá erro se não existir)
usuario = Usuario.objects.filter(email='naoexiste@email.com').first()
print(usuario)  # None


# Ordenar
usuarios = Usuario.objects.order_by('-criado')  # Mais recente primeiro
usuarios = Usuario.objects.order_by('nome')     # Ordem alfabética



# ----------------------------------------------

# Forma 1: Buscar, modificar, salvar
usuario = Usuario.objects.get(id=1)
usuario.nome = 'Raphamel Atualizado'
usuario.save()


# Forma 2: Update direto (mais eficiente)
Usuario.objects.filter(id=1).update(nome='Raphamel Update 2')


# Atualizar vários de uma vez
Usuario.objects.filter(nome__startswith='R').update(senha='NovaSenha123')


# ----------------------------------------------------
# Excluir 
# Deletar um
usuario = Usuario.objects.get(id=1)
usuario.delete()


# Deletar vários
Usuario.objects.filter(nome='David').delete()


# PERIGO: Deletar TODOS
Usuario.objects.all().delete()  # ⚠️ CUIDADO!