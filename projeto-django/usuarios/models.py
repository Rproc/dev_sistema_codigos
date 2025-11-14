from django.db import models

class Usuario(models.Model):
    """
    Model para representar um usuário do sistema
    """
    
    # Campos do model
    nome = models.CharField(
        max_length=80,
        verbose_name='Nome',  # Nome bonito para o Admin
        help_text='Nome completo do usuário',
        null=False
    )
    
    email = models.EmailField(
        unique=True,
        verbose_name='Email',
        help_text='Email único do usuário',
		null=False
    )
    
    senha = models.CharField(
        max_length=255,
        verbose_name='Senha',
        help_text='Senha do usuário',
		null=False
    )
    
    criado = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    atualizado = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        db_table = 'usuarios'  # Nome da tabela no banco
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-criado']  # Ordenar por mais recente
    
    def __str__(self):
        """
        Como o objeto aparece quando impresso
        """
        return f'{self.nome} ({self.email})'
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'