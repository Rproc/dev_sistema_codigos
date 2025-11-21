from rest_framework import serializers
from usuarios.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Usuario
    Equivalente ao to_dict() do Flask, mas mais poderoso!
    """
    
    
    class Meta:
        model = Usuario  # Qual model serializar
        fields = ['id', 'nome', 'email', 'criado', 'atualizado']
        # Ou usar '__all__' para todos os campos
        # fields = '__all__' 
        # exclude = ['senha'] # todos os campos, exceto a senha
        
        # Campos somente leitura (não podem ser modificados)
        read_only_fields = ['id', 'criado', 'atualizado']