from django.urls import path
from usuarios import views

urlpatterns = [
    # APIViews (class-based)
    path(
        'usuarios/',
        views.UsuarioListAPIView.as_view(), 
        name='usuario-lista'
    ),
    path(
        'usuarios/<int:id>/',
        views.UsuarioDetailAPIView.as_view(),
        name='usuario-detalhe'
    ),
]