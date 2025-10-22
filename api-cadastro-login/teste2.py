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
    RESET = '\033[0m'

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
            {Cores.RESET} - {nome_teste}')
        # se foi um sucesso, soma 1
        testes_sucesso += 1

    else:
        print(f'{Cores.VERMELHO}Xi Babou!\
            {Cores.RESET} - {nome_teste}')
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


def teste_login():
    nome_teste = 'Teste: Login'
    qual_teste(nome_teste)
    # Como que fazemos um teste de Login?
    # Pelo menos 1 usuário cadastrado
    # Saber email e senha

    # Passo 1 -> Criar um usuario para o teste
    usuario_teste = {
        'nome': 'Usuario Teste',
        'email': 'usuario_teste@senai.br',
        'senha': 'usuario@123'
    }

    # Passo 2 -> Inserir o usuario
    requests.post(f'{API_URL}/usuarios',
                json=usuario_teste)
    
    # Teste 1 -> Login com sucesso
    try:
        resposta = requests.post(f'{API_URL}/login',
                json={
                    'email': usuario_teste['email'],
                    'senha': usuario_teste['senha']
                },
                headers={
                    'Content-Type':'application/json'
                })
        
        if resposta.status_code == 200:
            dados = resposta.json()
            existe_nome = 'usuario' in dados
            existe_token = 'token' in dados
            print_teste('Teste com credenciais \
                válidas', 
                existe_nome and existe_token,
                f'Token: {dados.get('token')}'
            )
        else:
            print_teste('Teste com credenciais \
                válidas', 
                False,
                f'Status: {resposta.status_code}'
            )
    
    except Exception as e:
        print_teste('Teste com credenciais \
                válidas', 
                False,
                f'Erro: {str(e)}'
            )
        
    # Teste 2 -> Login com email inexistente
    try:
        resposta = requests.post(f'{API_URL}/login',
            json={
                'email':'naoexiste@senai.br',
                'senha':'usuario@123'
            },
            headers={
                'Content-Type':'application/json'
            })
        if resposta.status_code == 401:
            print_teste('Email não existente', True,
                        'API recusou corretamente')
        else:
            print_teste('Email não existente', False,
                        f'Status: {resposta.status_code}')
    
    except Exception as e:
        print_teste('Email não existente', False, 
                    f'Erro:{str(e)}')


def teste_criar():
    nome_teste = 'Teste: Criação de Usuário'
    qual_teste(nome_teste)

    # teste 1 -> Criar um usuario com sucesso
    try:
        novo_usuario={
            'nome': 'Presidente (Luane)',
            'email': 
            'presidente@primeiro_mandado.com',
            'senha': '171deNovaIguaçu'
        }
        resposta = requests.post(f'{API_URL}/usuarios',
                json=novo_usuario, 
                headers={
                    'Content-Type':'application/json'
                })
        if resposta.status_code == 201:
            dados = resposta.json()
            print_teste('Criar um usuário válido', True,
            f'ID Usuario:{dados.get('usuario').get('id')}')
        
        else:
            print_teste('Criar um usuário válido', False,
            f'Status: {resposta.status_code}')
    
    except Exception as e:
        print_teste('Criar um usuário válido', False,
        f'Erro: {str(e)}')

    # teste 2 -> Sem informação -> Corpo do JSON Vazio
    try:
        outro_usuario = {}
        resposta =  requests.post(f'{API_URL}/usuarios',
                    json=outro_usuario,
                    headers={
                        'Content-Type':'application/json'
                    })
        if resposta.status_code == 400:
            print_teste('Rejeitar corpo vazio', True,
                    'API validou corretamente')
        
        else:
            print_teste('Rejeitar corpo vazio', False,
                f'Status:{resposta.status_code}')
    
    except Exception as e:
        print_teste('Rejeitar corpo vazio', False,
                f'Erro: {str(e)}')

def executar_testes():
    teste_home()
    teste_login()
    teste_criar()

    # resumo do testes
                    

if __name__ == '__main__':
    executar_testes()

