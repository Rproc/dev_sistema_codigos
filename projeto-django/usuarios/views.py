from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET, require_POST
from flask import Response
from usuarios.models import Usuario
import json
from django.db.models import Q

def home(request):
    """
    Rota principal da API, retorna uma mensagem de boas-vindas
    e a versão da API.
    """
    return JsonResponse({
        'mensagem': "Bem vindo ao Geovanni's Pizza - Django Version",
        'versao': '1.0'
    })

@require_http_methods(['GET', 'POST'])
def usuarios_view(request):
    """
    GET  /usuarios/ -> Listar
    POST /usuarios/ -> Criar
    """
    
    if request.method == 'GET':
        # LISTAR
        usuarios = Usuario.objects.all()
        # Filtro por nome
        nome = request.GET.get('nome')
        if nome:
            usuarios = usuarios.filter(nome__icontains=nome)

        # Filtro por email
        email = request.GET.get('email')
        if email:
            usuarios = usuarios.filter(email__icontains=email)
        
		# Busca geral (OR)
        busca = request.GET.get('busca')
        if busca:
            usuarios = usuarios.filter(
                Q(nome__icontains=busca) |
                Q(email__icontains=busca)
            )

        # Ordenação
        ordem = request.GET.get('ordem', '-criado')
        usuarios = usuarios.order_by(ordem)
        
		# --- PAGINAÇÃO MANUAL ---
        pagina = int(request.GET.get('pagina', 1))
        por_pagina = int(request.GET.get('por_pagina', 1))

        total = usuarios.count()
        start = (pagina - 1) * por_pagina
        end = start + por_pagina

        usuarios_paginados = usuarios[start:end]

        total_paginas = (total + por_pagina - 1) // por_pagina  # ceil manual
        
        dados = [
            {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email
            }
            for usuario in usuarios_paginados
        ]
        return JsonResponse(
            {
                'dados': dados, 
                'pagina': pagina,
                'por_pagina': por_pagina,
             	'total': len(dados),
                'total_pages': total_paginas,
                'tem_proxima': pagina < total_paginas,
                'tem_anterior': pagina > 1,
                'filtros':{
                    'nome':nome,
                    'email':email,
                    'ordem':ordem
				}
            }
        )
    
    elif request.method == 'POST':
        # CRIAR
        try:
            dados = json.loads(request.body)
            
            usuario = Usuario.objects.create(
                nome=dados['nome'],
                email=dados['email'],
                senha=dados['senha']
            )
            
            return JsonResponse(
                {
                    'mensagem': 'Usuário criado com sucesso',
                    'usuario': {
                        'id': usuario.id,
                        'nome': usuario.nome,
                        'email': usuario.email
                    }
                },
                status=201
            )
        except KeyError as e:
            return JsonResponse(
                {'erro': f'Campo obrigatório: {e}'},
                status=400
            )
        except Exception as e:
            return JsonResponse(
                {'erro': str(e)},
                status=400
            )


@require_http_methods(['GET', 'PATCH', 'DELETE'])
def detalhes_usuario(request, id):
    """
    GET    /usuarios/<id>/ -> Buscar
    PATCH  /usuarios/<id>/ -> Atualizar
    DELETE /usuarios/<id>/ -> Deletar
    """
    
    try:
        usuario = Usuario.objects.get(id=id)
    except Usuario.DoesNotExist:
        return JsonResponse(
            {'erro': 'Usuário não encontrado'},
            status=404
        )
    
    if request.method == 'GET':
        # BUSCAR
        return JsonResponse({
            'id': usuario.id,
            'nome': usuario.nome,
            'email': usuario.email,
            'criado': usuario.criado.isoformat()
        })
    
    elif request.method == 'PATCH':
        # ATUALIZAR
        dados = json.loads(request.body)
        
        if 'nome' in dados:
            usuario.nome = dados['nome']
        if 'email' in dados:
            usuario.email = dados['email']
        if 'senha' in dados:
            usuario.senha = dados['senha']
        
        usuario.save()
        
        return JsonResponse({
            'mensagem': 'Usuário atualizado',
            'usuario': {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email
            }
        })
    
    elif request.method == 'DELETE':
        # DELETAR
        nome = usuario.nome
        usuario.delete()
        
        return JsonResponse({
            'mensagem': f'Usuário {nome} deletado com sucesso'
        })
    
