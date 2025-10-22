import requests
import json
from datetime import datetime

# Configuração
API_URL = 'http://localhost:5000'

# Cores para output no terminal


class Cores:
    VERDE = '\033[92m'
    VERMELHO = '\033[91m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    RESET = '\033[0m'


# Contadores de testes
testes_sucesso = 0
testes_falhas = 0


def qual_teste(nome):
    print(f'\n{Cores.AZUL}{'='*60}')
    print(nome)
    print(f'{Cores.AZUL}{'='*60}\n')


def print_teste(nome_teste, sucesso,
                detalhes=''):
    # para falar que estou usando as variaveis
    # criadas acima
    global testes_sucesso, testes_falhas

    # se foi bem sucedido
    if sucesso:
        print(f'{Cores.VERDE}Congratulações {Cores.RESET} - {nome_teste}')
        # se foi um sucesso, soma 1
        testes_sucesso += 1

    else:
        print(f'{Cores.VERMELHO}Xi Babou! {Cores.RESET} - {nome_teste}')
        testes_falhas += 1

    if detalhes:
        print(f'Detalhes: {detalhes}')


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

# Teste de listar


def teste_listar_usuarios():
    """GET /usuarios - Listar todos os usuários"""
    qual_teste("Teste: Listar Usuários")

    # Teste 1: Listar usuários com sucesso
    try:
        resposta = requests.get(f'{API_URL}/usuarios')

        if resposta.status_code == 200:
            dados = resposta.json()

            # Verifica estrutura da resposta
            if 'dados' in dados and 'total' in dados:
                print_teste(
                    "Listar usuários - estrutura correta",
                    True,
                    f"Total de usuários: {dados['total']}"
                )
            else:
                print_teste(
                    "Listar usuários - estrutura correta",
                    False,
                    "Resposta não contém 'dados' e 'total'"
                )

            # Verifica se usuários não têm senha
            if dados['dados']:
                primeiro_usuario = dados['dados'][0]
                tem_senha = 'senha' in primeiro_usuario
                print_teste(
                    "Usuários sem campo senha na listagem",
                    not tem_senha,
                    "Senha não está sendo retornada" if not tem_senha else "ERRO: Senha está sendo exposta!"
                )
        else:
            print_teste("Listar usuários", False,
                        f"Status code: {resposta.status_code}")

    except Exception as e:
        print_teste("Listar usuários", False, f"Erro: {str(e)}")


# Teste de Criar
def teste_criar_usuario():
    """POST /usuarios - Criar novo usuário"""
    qual_teste("Teste: Criar Usuário")

    # Teste 1: Criar usuário com sucesso
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    novo_usuario = {
        'nome': 'Presidente (Luane)',
        'email':
        'presidente@primeiro_mandado.com',
        'senha': '171deNovaIguaçu'
    }

    try:
        resposta = requests.post(
            f'{API_URL}/usuarios',
            json=novo_usuario,
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 201:
            dados = resposta.json()
            print_teste(
                "Criar usuário válido",
                True,
                f"ID: {dados.get('usuario', {}).get('id')}"
            )
        else:
            print_teste("Criar usuário válido", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Criar usuário válido", False, f"Erro: {str(e)}")

    # Teste 2: Criar usuário com email duplicado
    try:
        resposta = requests.post(
            f'{API_URL}/usuarios',
            json=novo_usuario,  # Mesmo email
            headers={'Content-Type': 'application/json'}
        )

        # Deve retornar erro (400)
        if resposta.status_code == 400:
            dados = resposta.json()
            print_teste(
                "Rejeitar email duplicado",
                'email' in dados.get('erro', '').lower(),
                "API rejeitou corretamente"
            )
        else:
            print_teste("Rejeitar email duplicado", False,
                        "Deveria retornar status 400")

    except Exception as e:
        print_teste("Rejeitar email duplicado", False, f"Erro: {str(e)}")

    # Teste 3: Criar usuário com nome curto (< 3 caracteres)
    try:
        resposta = requests.post(
            f'{API_URL}/usuarios',
            json={
                'nome': 'AB',  # Nome muito curto
                'email': f'curto{timestamp}@email.com',
                'senha': 'senha12345'
            },
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar nome curto", True,
                        "API validou corretamente")
        else:
            print_teste("Rejeitar nome curto", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar nome curto", False, f"Erro: {str(e)}")

    # Teste 4: Criar usuário com senha curta (< 8 caracteres)
    try:
        resposta = requests.post(
            f'{API_URL}/usuarios',
            json={
                'nome': 'Usuario Teste',
                'email': f'senhacurta{timestamp}@email.com',
                'senha': '123'  # Senha muito curta
            },
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar senha curta", True,
                        "API validou corretamente")
        else:
            print_teste("Rejeitar senha curta", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar senha curta", False, f"Erro: {str(e)}")

    # Teste 5: Criar usuário com email inválido
    try:
        resposta = requests.post(
            f'{API_URL}/usuarios',
            json={
                'nome': 'Usuario Teste',
                'email': 'emailinvalido',  # Sem @ e .
                'senha': 'senha12345'
            },
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar email inválido", True,
                        "API validou corretamente")
        else:
            print_teste("Rejeitar email inválido", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar email inválido", False, f"Erro: {str(e)}")

    # Teste 6: Criar usuário sem campos obrigatórios
    try:
        resposta = requests.post(
            f'{API_URL}/usuarios',
            json={'nome': 'Apenas Nome'},  # Faltam email e senha
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar dados incompletos",
                        True, "API validou corretamente")
        else:
            print_teste("Rejeitar dados incompletos", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar dados incompletos", False, f"Erro: {str(e)}")

    # Teste 7: Criar usuário com corpo vazio
    try:
        resposta = requests.post(
            f'{API_URL}/usuarios',
            json={},
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar corpo vazio", True,
                        "API validou corretamente")
        else:
            print_teste("Rejeitar corpo vazio", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar corpo vazio", False, f"Erro: {str(e)}")


# Teste de Login
def teste_login():
    """POST /login - Realizar login"""
    qual_teste("Teste: Login")

    # Primeiro cria um usuário para testar login
    usuario_teste = {
        'nome': 'Usuario Login',
        'email': f'login@email.com',
        'senha': 'senhaLogin123'
    }

    requests.post(f'{API_URL}/usuarios', json=usuario_teste)

    # Teste 1: Login com sucesso
    try:
        resposta = requests.post(
            f'{API_URL}/login',
            json={
                'email': usuario_teste['email'],
                'senha': usuario_teste['senha']
            },
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 200:
            dados = resposta.json()
            existe_token = 'token' in dados
            existe_nome = 'usuario' in dados
            print_teste(
                "Login com credenciais válidas",
                existe_nome and existe_token,
                f"Token: {dados.get('token', 'N/A')}"
            )
        else:
            print_teste("Login com credenciais válidas", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Login com credenciais válidas",
                    False, f"Erro: {str(e)}")

    # Teste 2: Login com senha errada
    try:
        resposta = requests.post(
            f'{API_URL}/login',
            json={
                'email': usuario_teste['email'],
                'senha': 'senhaErrada'
            },
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 401:
            print_teste("Rejeitar senha incorreta", True,
                        "API rejeitou corretamente")
        else:
            print_teste("Rejeitar senha incorreta", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar senha incorreta", False, f"Erro: {str(e)}")

    # Teste 3: Login com email inexistente
    try:
        resposta = requests.post(
            f'{API_URL}/login',
            json={
                'email': 'naoexiste@email.com',
                'senha': 'qualquersenha'
            },
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 401:
            print_teste("Rejeitar email inexistente",
                        True, "API rejeitou corretamente")
        else:
            print_teste("Rejeitar email inexistente", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar email inexistente", False, f"Erro: {str(e)}")

    # Teste 4: Login sem campos obrigatórios
    try:
        resposta = requests.post(
            f'{API_URL}/login',
            json={'email': usuario_teste['email']},  # Falta senha
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar login incompleto",
                        True, "API validou corretamente")
        else:
            print_teste("Rejeitar login incompleto", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar login incompleto", False, f"Erro: {str(e)}")


# Teste de Atualização
def teste_atualizar_usuario():
    """PATCH /usuarios/<id> - Atualizar usuário"""
    qual_teste("TESTES: Atualizar Usuário")

    # Cria um usuário para testar
    usuario_teste = {
        'nome': 'Usuario Original',
        'email': f'atualizar@email.com',
        'senha': 'senhaOriginal123'
    }

    resposta_criacao = requests.post(f'{API_URL}/usuarios', json=usuario_teste)
    id_usuario = resposta_criacao.json().get('usuario', {}).get('id')

    # Teste 1: Atualizar nome com sucesso
    try:
        resposta = requests.patch(
            f'{API_URL}/usuarios/{id_usuario}',
            json={'nome': 'Nome Atualizado'},
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 200:
            dados = resposta.json()
            nome_atualizado = dados.get('usuario', {}).get('nome')
            print_teste(
                "Atualizar nome",
                nome_atualizado == 'Nome Atualizado',
                f"Novo nome: {nome_atualizado}"
            )
        else:
            print_teste("Atualizar nome", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Atualizar nome", False, f"Erro: {str(e)}")

    # Teste 2: Atualizar com nome curto
    try:
        resposta = requests.patch(
            f'{API_URL}/usuarios/{id_usuario}',
            json={'nome': 'AB'},
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar atualização com nome curto",
                        True, "API validou corretamente")
        else:
            print_teste("Rejeitar atualização com nome curto",
                        False, f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar atualização com nome curto",
                    False, f"Erro: {str(e)}")

    # Teste 3: Atualizar senha
    try:
        resposta = requests.patch(
            f'{API_URL}/usuarios/{id_usuario}',
            json={'senha': 'novaSenha12345'},
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 200:
            print_teste("Atualizar senha", True,
                        "Senha atualizada com sucesso")
        else:
            print_teste("Atualizar senha", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Atualizar senha", False, f"Erro: {str(e)}")

    # Teste 4: Atualizar com senha igual à anterior
    try:
        resposta = requests.patch(
            f'{API_URL}/usuarios/{id_usuario}',
            json={'senha': 'novaSenha12345'},  # Mesma senha
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar senha igual à anterior",
                        True, "API validou corretamente")
        else:
            print_teste("Rejeitar senha igual à anterior",
                        False, f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar senha igual à anterior",
                    False, f"Erro: {str(e)}")

    # Teste 5: Atualizar usuário inexistente
    try:
        resposta = requests.patch(
            f'{API_URL}/usuarios/99999',
            json={'nome': 'Teste'},
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 404:
            print_teste("Atualizar usuário inexistente",
                        True, "API retornou 404 corretamente")
        else:
            print_teste("Atualizar usuário inexistente", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Atualizar usuário inexistente", False, f"Erro: {str(e)}")

    # Teste 6: Atualizar com corpo vazio
    try:
        resposta = requests.patch(
            f'{API_URL}/usuarios/{id_usuario}',
            json={},
            headers={'Content-Type': 'application/json'}
        )

        if resposta.status_code == 400:
            print_teste("Rejeitar atualização com corpo vazio",
                        True, "API validou corretamente")
        else:
            print_teste("Rejeitar atualização com corpo vazio",
                        False, f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Rejeitar atualização com corpo vazio",
                    False, f"Erro: {str(e)}")


# Teste de Delete
def teste_deletar_usuario():
    """DELETE /usuarios/<id> - Deletar usuário"""
    qual_teste("TESTES: Deletar Usuário")

    # Cria um usuário para deletar
    usuario_teste = {
        'nome': 'Usuario Para Deletar',
        'email': f'deletar@email.com',
        'senha': 'senha12345'
    }

    resposta_criacao = requests.post(f'{API_URL}/usuarios', json=usuario_teste)
    id_usuario = resposta_criacao.json().get('usuario', {}).get('id')

    # Teste 1: Deletar usuário existente
    try:
        resposta = requests.delete(f'{API_URL}/usuarios/{id_usuario}')

        if resposta.status_code == 200:
            print_teste("Deletar usuário existente", True,
                        f"ID deletado: {id_usuario}")
        else:
            print_teste("Deletar usuário existente", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Deletar usuário existente", False, f"Erro: {str(e)}")

    # Teste 2: Deletar usuário inexistente
    try:
        resposta = requests.delete(f'{API_URL}/usuarios/99999')

        if resposta.status_code == 404:
            print_teste("Deletar usuário inexistente", True,
                        "API retornou 404 corretamente")
        else:
            print_teste("Deletar usuário inexistente", False,
                        f"Status: {resposta.status_code}")

    except Exception as e:
        print_teste("Deletar usuário inexistente", False, f"Erro: {str(e)}")

# ========================================
# FUNÇÃO PRINCIPAL
# ========================================


def executar_todos_testes():
    """Executa todos os testes"""
    print(f"\n{Cores.AMARELO}{'='*60}")
    print("INICIANDO TESTES DA API - PIZZARIA")
    print(f"{'='*60}{Cores.RESET}")
    print(f"URL da API: {API_URL}")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    # Verifica se API está online
    if not teste_home():
        print(
            f"\n{Cores.VERMELHO}Erro: API não está acessível. Certifique-se de que está rodando.{Cores.RESET}")
        return

    # Executa todos os testes
    teste_listar_usuarios()
    teste_criar_usuario()
    teste_login()
    teste_atualizar_usuario()
    teste_deletar_usuario()

    # Resultado final
    qual_teste("Resumo dos testes")
    total_testes = testes_sucesso + testes_falhas
    percentual = (testes_sucesso / total_testes *
                  100) if total_testes > 0 else 0

    print(f"Total de testes: {total_testes}")
    print(f"{Cores.VERDE}Passaram: {testes_sucesso}{Cores.RESET}")
    print(f"{Cores.VERMELHO}Falharam: {testes_falhas}{Cores.RESET}")
    print(f"Taxa de sucesso: {percentual:.1f}%")

    if testes_falhas == 0:
        print(f"\n{Cores.VERDE}{'='*60}")
        print("Todas as Congratulações Possiveis")
        print(f"{'='*60}{Cores.RESET}\n")
    else:
        print(f"\n{Cores.AMARELO}{'='*60}")
        print(
            f"{testes_falhas} teste(s) falharam. Verifique os detalhes acima.")
        print(f"{'='*60}{Cores.RESET}\n")


if __name__ == '__main__':
    executar_todos_testes()
