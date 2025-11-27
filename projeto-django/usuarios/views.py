from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para CRUD de usuários
    
    Automaticamente fornece:
    - list()    GET    /usuarios/
    - create()  POST   /usuarios/
    - retrieve() GET   /usuarios/<id>/
    - update()  PUT    /usuarios/<id>/
    - partial_update() PATCH /usuarios/<id>/
    - destroy() DELETE /usuarios/<id>/
    """
    
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def get_queryset(self):
        '''
        Permite customizar o queryset retornado
        GET /usuarios/?nome=melquisedeque&email=gmail
        '''
        
        queryset = Usuario.objects.all()
        
        # Filtrar por nome
        nome = self.request.query_params.get('nome')
        if nome:
            queryset = queryset.filter(nome__icontains=nome)
        
        # Filtrar por email
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__icontains=email)
        
        # Ordenar
        ordem = self.request.query_params.get('ordem', '-criado')
        queryset = queryset.order_by(ordem)
        
        return queryset
