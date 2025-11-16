from django.urls import path
from . import views

urlpatterns = [
    # primeiro parametro -> rota
    # segundo parametro -> view
    # O parâmetro "name" é usado para fornecer um identificador exclusivo para esse padrão de URL,
    # que pode ser usado para pesquisas reversas de URL.
    path('', views.home, name='home'),
	path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
	path('usuarios/<int:id>/', views.buscar_usuario, name='buscar_usuario'),
	path('usuarios/', views.listar_usuarios_com_filtros, name='listar_usuarios_com_filtros'),
]
