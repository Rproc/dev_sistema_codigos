import os
import sys
import django

# Caminho base do projeto (um nível acima de /usuarios/)
BASE_DIR = os.path.dirname(
	os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Apontar para o settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 
					  'docelar.settings')

# Inicializar Django
django.setup()

from usuarios.models import Usuario
# primeira parte do crud: Create (criar)

# create -> cria e salva
usuario1 = Usuario.objects.create(
	nome='Bruno',
	email='bomberman@senai.br',
	senha='321explodiu'
	)

usuario2 = Usuario(
	nome='Juan Frontend',
	email='padding@senai.br',
	senha='css3html5'
)
# salvar no banco
usuario2.save()

print(usuario1.nome)

# se já existir um usuario com o mesmo email?

usuario3, criado = \
Usuario.objects.get_or_create(
	email='saude@senai.br',
	defaults={
		'nome':'Silvio',
		'senha':'atchin'
	}
)
if criado:
	print(f'Criou: {usuario3}')
else:
	print(f'Já existia: {usuario3}')

# -------------------------------------
# a parte de ler (read) - select - query

# listar todos
usuarios = Usuario.objects.all()

# buscar um individuo
usuario4 = Usuario.objects.get(
	email='saude@senai.br')
# silvio

usuario5 = Usuario.objects.get(id=1)
# bruno

# maneira mais "certa" de buscar
# pq retorna None se não encontrar (evita erros)
usuario6 = Usuario.objects.filter(
	nome='Juan Frontend').first()
# saida: Usuario ou None

lista_usuarios = Usuario.objects.order_by(
	'-criado')
# lista de todos os usuarios ja ordernada em 
# ordem decrescente pela data de criação

# -----------------------------------------
# atualizar (update)
# forma 1
usuario_alter = Usuario.objects.get(id=1)
usuario_alter.nome='Hulk magrelo'
usuario_alter.save()

# forma 2 -> usar update
Usuario.objects.filter(
	email='padding@senai.br').update(
		nome='Juan Fullstack'
	)

# -----------------------------------------

# delete (deletar)
usuario_del = Usuario.objects.get(id=1)
usuario_del.delete()

# forma mais rapida
Usuario.objects.filter(nome='Silvio').delete()

# users = Usuario.objects.filter(nome='Silvio')
# for user in users:
# 	# verifica cada usuario com nome silvio
# 	if user == "o que eu quero":
# 		user.delete()

# não faça isso:
# Usuario.objects.all().delete()
