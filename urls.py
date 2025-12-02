# Importa o router do DRF
# O router é responsável por gerar automaticamente todas as rotas REST
from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Importa o ViewSet que será usado para gerar as rotas
from usuarios import views


# Cria uma instância do router
# DefaultRouter já gera também a rota para a interface de navegação do DRF
router = DefaultRouter()


# Registra o ViewSet no router
# Primeiro argumento: prefixo da rota → /usuarios/
# Segundo: a classe do ViewSet que contém as ações (list, retrieve, create...)
# basename: nome interno usado pelo DRF (bom para evitar conflitos)
router.register(
    r'usuarios',       # gera /usuarios/ e /usuarios/<pk>/
    views.UsuarioViewSet,    # ViewSet que controla essas rotas
    basename='usuarios'
)


# urlpatterns gerado automaticamente
# Ele cria todas as rotas sem precisar escrever path() manual
urlpatterns = router.urls
