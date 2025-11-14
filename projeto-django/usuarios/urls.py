from django.urls import path
from . import views

urlpatterns = [
    # primeiro parametro -> rota
    # segundo parametro -> view
    # O parâmetro "name" é usado para fornecer um identificador exclusivo para esse padrão de URL,
    # que pode ser usado para pesquisas reversas de URL.
    path('', views.home, name='home'),
]
