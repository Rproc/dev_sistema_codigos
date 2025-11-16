from django.shortcuts import render
from django.http import JsonResponse
from usuarios.models import Usuario


def home(request):
    """
    Rota principal da API, retorna uma mensagem de boas-vindas
    e a versão da API.
    """
    return JsonResponse({
        'mensagem': "Bem vindo ao Geovanni's Pizza - Django Version",
        'versao': '1.0'
    })

def listar_usuarios(request):
    """
    GET /usuarios/
    Lista todos os usuários
    
    Equivalente Flask:
    @app.route('/usuarios', methods=['GET'])
    def listar_usuarios():
        usuarios = Usuario.query.all()
        return jsonify([u.to_dict() for u in usuarios])
    """
    
    # Buscar todos os usuários
    usuarios = Usuario.objects.all()
    
    # Converter para lista de dicionários
    dados = []
    for usuario in usuarios:
        dados.append({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'criado': usuario.criado.isoformat()
        })
    # Usando pythonês 
    # dados = [
    #     {
    #         'id': u.id,
    #         'nome': u.nome,
    #         'email': u.email,
    #         'criado': u.criado.isoformat()
    #     }
    #     for u in usuarios
    # ]
    
    # Retornar JSON
    return JsonResponse({
        'dados': dados,
        'total': len(dados)
    })

# usuarios/views.py

def buscar_usuario(request, id):
    """
    GET /usuarios/1/
    Busca um usuário específico por ID
    
    No Flask:
    @app.route('/usuarios/<int:id>')
	def buscar_usuario(id):
    	usuario = Usuario.query.get(id)
    """
    
    try:
        usuario = Usuario.objects.get(id=id)
        
        dados = {
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'criado': usuario.criado.isoformat(),
            'atualizado': usuario.atualizado.isoformat()
        }
        
        return JsonResponse(dados)
        
    except Usuario.DoesNotExist:
        return JsonResponse(
            {'erro': 'Usuário não encontrado'},
            status=404
        )
    
# usuarios/views.py

def listar_usuarios_com_filtros(request):
    """
    GET /usuarios/?nome=joao&email=joao@email.com
    Lista usuários com filtros opcionais
    """
    
    # Começar com todos
    usuarios = Usuario.objects.all()
    
    # Filtrar por nome (se fornecido)
    nome = request.GET.get('nome')  # ← GET (maiúsculo!)
    if nome:
        # __icontains = contem (case insensitive [não diferencia maiúsculas/minúsculas])
        usuarios = usuarios.filter(nome__icontains=nome)
    
    # Filtrar por email (se fornecido)
    email = request.GET.get('email')
    if email:
        usuarios = usuarios.filter(email__icontains=email)
    
    # Ordenar
    ordem = request.GET.get('ordem', '-criado')  # Default: mais recente
    usuarios = usuarios.order_by(ordem)
    
    # Converter para lista
    dados = [
        {
            'id': u.id,
            'nome': u.nome,
            'email': u.email,
        }
        for u in usuarios
    ]
    
    return JsonResponse({
        'dados': dados,
        'total': len(dados),
        'filtros': {
            'nome': nome,
            'email': email,
            'ordem': ordem
        }
    })