from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Usuario
from .serializers import (
    UsuarioSerializer,
    CadastroSerializer,
    LoginSerializer
)


class UsuarioViewSet(viewsets.ModelViewSet):
    """
    ViewSet para usuários com cadastro e login
    """
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]  # Tudo público por enquanto
    
    # ============================================
    # ACTION: CADASTRO
    # ============================================
    
    @action(detail=False, methods=['post'], url_path='cadastro')
    def cadastro(self, request):
        """
        POST /usuarios/cadastro/
        
        Cadastra um novo usuário.
        
        Body:
        {
            "nome": "João Silva",
            "email": "joao@example.com",
            "senha": "senha12345678"
        }
        
        Resposta (201):
        {
            "mensagem": "Usuário cadastrado com sucesso",
            "usuario": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao@example.com",
                "criado": "2024-11-17T10:00:00Z"
            }
        }
        """
        serializer = CadastroSerializer(data=request.data)
        
        if serializer.is_valid():
            # Criar usuário (senha será hasheada automaticamente)
            usuario = serializer.save()
            
            return Response({
                'mensagem': 'Usuário cadastrado com sucesso',
                'usuario': UsuarioSerializer(usuario).data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'erro': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # ============================================
    # ACTION: LOGIN
    # ============================================
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """
        POST /usuarios/login/
        
        Faz login de um usuário.
        
        Body:
        {
            "email": "joao@example.com",
            "senha": "senha12345678"
        }
        
        Resposta (200):
        {
            "mensagem": "Login realizado com sucesso",
            "usuario": {
                "id": 1,
                "nome": "João Silva",
                "email": "joao@example.com",
                "criado": "2024-11-17T10:00:00Z"
            }
        }
        """
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            # Pegar usuário validado
            usuario = serializer.validated_data['usuario']
            
            return Response({
                'mensagem': 'Login realizado com sucesso',
                'usuario': UsuarioSerializer(usuario).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            'erro': serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)
