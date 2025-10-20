import requests
import json
from datetime import datetime

# localhost -> 127.0.0.1 - "Hospedeiro Local"
API_URL = 'http://localhost:5000'

class Cores:
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    SEPARADOR = '\033[0m'

# Variaveis de Controle para ver
# se passou no teste
testes_sucesso = 0
testes_falhas = 0

# qual teste nesse momento
def qual_teste(nome):
    print(f'\n{Cores.AZUL}{'='*60}')
    print(nome)
    print(f'{Cores.AZUL}{'='*60}\n')

# resultado dos testes
def print_teste(nome_teste, sucesso, 
                detalhes=''):
    # para falar que estou usando as variaveis
    # criadas acima
    global testes_sucesso, testes_falhas

    # se foi bem sucedido
    if sucesso:
        print(f'{Cores.VERDE}Congratulações \
            {Cores.SEPARADOR} - {nome_teste}')
        # se foi um sucesso, soma 1
        testes_sucesso += 1

    else:
        print(f'{Cores.VERMELHO}Xi Babou!\
            {Cores.SEPARADOR} - {nome_teste}')
        testes_falhas += 1

    if detalhes:
        print(f'Detalhes: {detalhes}')

# Quais dessas rotas deve testar primeiro:
# home, listar_usuario, criar_usuario, login,
# deletar_usuario, atualizar_usuario

# primeiro teste -> API está online
def teste_home():
    qual_teste('Verificando se a API está online')
    try:
        resposta = requests.get(f'{API_URL}/')
        # sucesso
        if resposta.status_code == 200:
            print_teste('API está online', 
                        True, 
            f'Status:{resposta.status_code}')
            return True
        # falha
        else:
            print_teste('API está online',
                        False,
                    f'Status inesperado:  \
                    {resposta.status_code}')
            return False
    # exceção exclusiva do requests
    except requests.exceptions.ConnectionError:
        print_teste('API está online', False,
        'Não foi possível conectar. \
        Deu erro no engano')
        return False


teste_home()   
                    


