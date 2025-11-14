from django.shortcuts import render
from django.http import JsonResponse


def home(request):
    """
    Rota principal da API, retorna uma mensagem de boas-vindas
    e a versão da API.
    """
    return JsonResponse({
        'mensagem': "Bem vindo ao Geovanni's Pizza - Django Version",
        'versao': '1.0'
    })
