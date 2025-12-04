from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

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
    def get_permissions(self):
        """
        Define permissões por action
        
        - cadastro e login: público (AllowAny)
        - list e retrieve: público (AllowAny) 
        - update, partial_update, destroy: precisa estar autenticado
        """
        if self.action in ['cadastro', 'login', 'list', 'retrieve']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        
        return [permission() for permission in permission_classes]
    
    # ============================================
    # ACTION: CADASTRO
    # ============================================
    
    @action(detail=False, methods=['post'], url_path='cadastro', serializer_class=CadastroSerializer)
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
    
    @action(detail=False, methods=['post'], url_path='login', serializer_class=LoginSerializer)
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
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",  ← TOKEN DE ACESSO
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  ← TOKEN DE REFRESH
        }
        """
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            # Pegar usuário validado
            usuario = serializer.validated_data['usuario']

            refresh = RefreshToken.for_user(usuario)
            access = refresh.access_token

            return Response({
                'mensagem': 'Login realizado com sucesso',
                'usuario': UsuarioSerializer(usuario).data,
                'access': str(access),  # Token de acesso
                'refresh': str(refresh)                # Token de refresh
            }, status=status.HTTP_200_OK)
        
        return Response({
            'erro': serializer.errors
        }, status=status.HTTP_401_UNAUTHORIZED)

    @action (detail=False, methods=['get'], url_path='perfil', permission_classes=[IsAuthenticated])
    def perfil(self, request):
        """
        GET /perfil/
        Retorna as informações do perfil do usuário autenticado
        
        Resposta (200):
        {
            "id": 1,
            "nome": "João Silva",
            "email": "joao@example.com",
            "criado": "2024-11-17T10:00:00Z"
        }
        """
        user_id = request.auth.payload.get('user_id')
        
        try:
            usuario = Usuario.objects.get(id=user_id)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data)
        except Usuario.DoesNotExist:
            return Response(
                {'erro': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
    @action(detail=False,methods=['post'], url_path='refresh', permission_classes=[AllowAny])
    def refresh_token(self, request):
        """
        POST /usuarios/refresh/
        
        Gera novo access token usando o refresh token
        
        Body:
        {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
        }
        
        Resposta (200):
        {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."  ← Novo token
        }
        """
        
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'erro': 'Refresh token é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            refresh = RefreshToken(refresh_token)
            
            return Response({
                'access': str(refresh.access_token)
            })
        except TokenError:
            return Response(
                {'erro': 'Token inválido ou expirado'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
    def partial_update(self, request, pk=None):
        """
        PATCH /usuarios/<pk>/ 
        Só permite atualizar o próprio perfil
        """
        usuario = self.get_object()
        
        # Verificar se é o próprio usuário
        user_id_from_token = request.auth.payload.get('user_id')
        if usuario.id != user_id_from_token:
            return Response(
                {'erro': 'Você só pode atualizar seu próprio perfil'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CadastroSerializer(
            usuario,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'mensagem': 'Usuário atualizado com sucesso',
                'usuario': UsuarioSerializer(usuario).data
            })
        
        return Response(
            {'erro': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, pk=None):
        """
        DELETE /usuarios/<pk>/
        Só permite deletar o próprio perfil
        """
        usuario = self.get_object()
        
        # Verificar se é o próprio usuário
        user_id_from_token = request.auth.payload.get('user_id')
        if usuario.id != user_id_from_token:
            return Response(
                {'erro': 'Você só pode deletar seu próprio perfil'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        nome = usuario.nome
        usuario.delete()
        
        return Response({
            'mensagem': f'Usuário {nome} deletado com sucesso'
        })
    