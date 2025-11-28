from django.db import models
from django.contrib.auth.hashers import make_password, check_password
# Create your models here.

class Usuario(models.Model):
    
    nome = models.CharField(max_length=80,
                    verbose_name='Nome',
                    help_text='Nome completo do usuário',
                    null=False)
    email = models.EmailField(unique=True, 
                    verbose_name='E-mail',
                    help_text='E-mail do usuário',
                    null=False)
    senha = models.CharField(max_length=255,
                    verbose_name='Senha',
                    help_text='Senha do usuário',
                    null=False)
    criado = models.DateTimeField(auto_now_add=True,
                    verbose_name='Criado em')
    atualizado = models.DateTimeField(auto_now=True,
                    verbose_name='Atualizado em')
    
    class Meta:
        # nome da tabela
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nome'] #ordena por nome (ordem alfabetica)
        # se fosse por data de criação
        # ordering = ['-criado'] 
        # ordem do mais recente (decrescente)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'
    
    def __str__(self):
        return f'{self.nome} ({self.email})'

    def verificar_senha(self, senha_texto):
        """
        Verifica se a senha fornecida está correta
        
        Args:
            senha_texto (str): Senha em texto puro
            
        Returns:
            bool: True se correta, False se incorreta
        """
        return check_password(senha_texto, self.senha)


    def save(self, *args, **kwargs):
        """
        Sobrescreve o método save para hashear a senha automaticamente
        
        IMPORTANTE: Este método é chamado sempre que criamos
        ou atualizamos um usuário!
        """
        # args e kwargs são argumentos posicionais e nomeados - Aceita qualquer argumento
        # Verifica se a senha precisa ser hasheada
        # Senhas hasheadas começam com o algoritmo (pbkdf2_sha256$)
        if self.senha and not self.senha.startswith('pbkdf2_sha256$'):
            self.senha = make_password(self.senha)
        
        super().save(*args, **kwargs)









