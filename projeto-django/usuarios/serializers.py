from rest_framework import serializers
from .models import Usuario


# ============================================
# SERIALIZER DE CADASTRO
# ============================================

class CadastroSerializer(serializers.ModelSerializer):
    """
    Serializer para cadastro de novos usuários
    """
    senha = serializers.CharField(
        write_only=True,  # Não retorna senha na resposta
        min_length=8,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha']
    
    def validate_nome(self, value):
        """Validar nome"""
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Nome deve ter no mínimo 3 caracteres")
        return value.strip()
    
    def validate_email(self, value):
        """Validar email"""
        email = value.strip().lower()
        
        # Verificar se já existe
        if Usuario.objects.filter(email=email).exists():
            raise serializers.ValidationError("Este email já está cadastrado")
        
        return email
    
    def validate_senha(self, value):
        """Validar senha"""
        if len(value) < 8:
            raise serializers.ValidationError("Senha deve ter no mínimo 8 caracteres")
        return value
    
    def create(self, validated_data):
        """Criar usuário (senha será hasheada pelo model)"""
        return Usuario.objects.create(**validated_data)


# ============================================
# SERIALIZER DE LOGIN
# ============================================

class LoginSerializer(serializers.Serializer):
    """
    Serializer para login (não vinculado a model)
    """
    email = serializers.EmailField(required=True)
    senha = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    
    def validate_email(self, value):
        """Normalizar email"""
        return value.strip().lower()
    
    def validate(self, data):
        """
        Validar credenciais
        """
        email = data.get('email')
        senha = data.get('senha')
        
        # Buscar usuário
        try:
            usuario = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError("Email ou senha inválidos")
        
        # Verificar senha (usando método do model)
        if not usuario.verificar_senha(senha):
            raise serializers.ValidationError("Email ou senha inválidos")
        
        # Adicionar usuário aos dados validados
        data['usuario'] = usuario
        return data


# ============================================
# SERIALIZER DE USUÁRIO (para respostas)
# ============================================

class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para retornar dados do usuário
    (SEM senha!)
    """
    class Meta:
        model = Usuario
        fields = ['id', 'nome', 'email', 'criado']
        read_only_fields = ['id', 'criado']
