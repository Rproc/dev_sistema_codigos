from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from usuarios.models import Usuario
from usuarios.serializers import UsuarioSerializer

class UsuarioListAPIView(APIView):
    """
    GET  /usuarios/ - Listar todos
    POST /usuarios/ - Criar novo
    """
    
    def get(self, request):
        """Listar usuários"""
        usuarios = Usuario.objects.all()
        
        # Serializar (many=True para lista)
        serializer = UsuarioSerializer(usuarios, many=True)
        
        # Response automático
        return Response({
            'dados': serializer.data,
            'total': len(serializer.data)
        })
    
    def post(self, request):
        """Criar usuário"""
        # Desserializar (JSON → Python)
        serializer = UsuarioSerializer(data=request.data)
        
        # Validar
        if serializer.is_valid():
            # Salvar no banco
            usuario = serializer.save()
            
            return Response({
                'mensagem': 'Usuário criado com sucesso',
                'usuario': UsuarioSerializer(usuario).data
            }, status=status.HTTP_201_CREATED)
        
        # Se inválido, retornar erros
        return Response(
            {'erro': serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
    

class UsuarioDetailAPIView(APIView):
    """
    GET    /usuarios/<id>/ - Buscar
    PATCH  /usuarios/<id>/ - Atualizar
    DELETE /usuarios/<id>/ - Deletar
    """
    
    def get_object(self, id):
        """Helper para buscar usuário ou retornar 404"""
        return get_object_or_404(Usuario, id=id)
    
    def get(self, request, id):
        """Buscar usuário específico"""
        usuario = self.get_object(id)
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)
    
    def patch(self, request, id):
        """Atualizar parcialmente"""
        usuario = self.get_object(id)
        
        # partial=True = permite atualizar apenas alguns campos
        serializer = UsuarioSerializer(
            usuario,
            data=request.data,
            partial=True
        )
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'mensagem': 'Usuário atualizado',
                'usuario': serializer.data
            })
        
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def delete(self, request, id):
        """Deletar usuário"""
        usuario = self.get_object(id)
        nome = usuario.nome
        usuario.delete()
        
        return Response({
            'mensagem': f'Usuário {nome} deletado com sucesso'
        }, status=status.HTTP_200_OK)
    