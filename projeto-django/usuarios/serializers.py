from rest_framework import serializers
from usuarios.models import Usuario


class UsuarioSerializer(serializers.ModelSerializer):
    """
    Serializer para o model Usuario
    Equivalente ao to_dict() do Flask, mas mais poderoso!
    """
    senha = serializers.CharField(
    write_only=True,  # Não aparece na saída
    min_length=8,
    max_length=50
    )
    senha_confirmacao = serializers.CharField(write_only=True)

    # Campo calculado (SerializerMethodField)
    nome_completo = serializers.SerializerMethodField()

    class Meta:
        model = Usuario  # Qual model serializar
        fields = ['id', 'nome', 'email', 'criado', 'atualizado', 'senha', 'nome_completo', 'senha_confirmacao']
        # Ou usar '__all__' para todos os campos
        # fields = '__all__' 
        # exclude = ['senha'] # todos os campos, exceto a senha

    # Campos somente leitura (não podem ser modificados)
    read_only_fields = ['id', 'criado', 'atualizado']

    def get_nome_completo(self, obj):
        """
        Método para obter o nome completo do usuário.
        Exemplo de campo calculado.
        deve começar com get_<nome_do_campo>
        """
        return f"{obj.nome} ({obj.email})"
    
    def validate_nome(self, value):
        """
        Valida o campo 'nome'
        Método DEVE se chamar validate_<nome_do_campo>
        """
        if len(value) < 3:
            raise serializers.ValidationError(
            "Nome deve ter no mínimo 3 caracteres"
        )

        # Sempre retornar o valor (possivelmente modificado)
        return value.strip()

    def validate_email(self, value):
        """Valida email"""
        email = value.lower().strip()

        # Verificar se já existe
        if Usuario.objects.filter(email=email).exists():
            raise serializers.ValidationError(
            "Este email já está cadastrado"
        )
        return email

    def validate_senha(self, value):
        """Valida senha"""
        if len(value) < 8:
            raise serializers.ValidationError(
            "Senha deve ter no mínimo 8 caracteres"
        )

        if value.isdigit():
            raise serializers.ValidationError(
            "Senha não pode ser apenas números"
        )
        return value
    
    def validate(self, data):
        """
        Validação a nível de objeto (múltiplos campos)
        Chamado APÓS validate_<campo> individuais
        """
        senha = data.get('senha')
        senha_confirmacao = data.get('senha_confirmacao')

        if senha != senha_confirmacao:
            raise serializers.ValidationError({
                'senha_confirmacao': 'As senhas não conferem'
            })

        # Remover senha_confirmacao (não está no model)
        data.pop('senha_confirmacao')
        return data