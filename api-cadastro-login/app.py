from flask import Flask, request, jsonify

# cria um objeto flask, que vai ser o app
app = Flask(__name__)

# JSON aceitar caracteres especiais
app.config['JSON_AS_ASCII']=False
# se der errado, descomente o debaixo
# app.json.ensure.ascii = False
# usuario(id, nome, email, senha)
usuarios = [
    {'id': 1, 'nome': 'Raphamel', 
     'email':'raphamengo@senai.br', 
     'senha':'Flamengo2019'},
    {'id': 2, 'nome': 'David', 
     'email':'davidvarao@senai.br',
     'senha':'Varao123'},
    {'id': 3, 'nome': 'Geovanni',
     'email':'geo@vanni.br', 
     'senha':'PizzaioloTricolor'}
]

# pq não estamos usando BD
# Ideia de autoincrement
proximo_id = 4

def validar_usuario(dados):
    # validar dados vindo das requisições
    # 3 retornos: 
    # 1 -> se são validos (True)/False
    # 2 -> Qual foi o erro
    # 3 -> Dados Validados
    # Existem dados no JSON?
    if not dados:
        return False, "Corpo da requisição \
        não pode ser vazio", None

    # se existe o campo nome no JSON
    if 'nome' not in dados:
        return False, \
        "Campo 'nome' é obrigatorio", None
    # ja que o campo existe, iremos pegar o 
    # valor associado a ele
    nome = dados.get('nome', '').strip()

    # tenho o nome, o que eu quero validar?
    if not nome:
        return False, \
    "Campo 'nome' não pode estar vazio", None

    # tamanho minimo do nome
    if len(nome) < 3:
        return False, "Campo 'nome' deve ter \
            no minimo 3 caracteres", None

    # ------------------------------------
    # Se existe o campo EMAIL no JSON
    if 'email' not in dados:
        return False, \
    "Campo 'email' é obrigatório", None

    email = dados.get('email', '').strip().lower()

    if not email:
        return False, "Campo 'email' não \
        pode estar vazio", None
    
    # Certeza -> Campo Email existe e o 
    # email existe
    email_existente = [user for user in usuarios if email == user['email']]

    # verificar se há algum usuario com esse email
    if len(email_existente) > 0:
        return False, "Este email já \
            está cadastrado", None
    
    #  ------------------------------------
    if 'senha' not in dados:
        return False, "Campo 'senha'\
              é Obrigatorio", None
    
    # senha ja existe
    senha = dados.get('senha', '').strip()

    if not senha:
        return False, "Campo 'senha' não pode \
            estar vazio", None
    
    if len(senha) < 8 and len(senha) > 50:
        return False, "Campo 'senha' com \
            tamanho inválido", None 
    
    dados_validados = {
        'nome': nome,
        'email': email,
        'senha': senha
    }
    return True, None, dados_validados


     

# Rota padrão - Index - Landpage
@app.route('/')
def home():
    return jsonify({
        'msg':"Bem vindo ao Geovanni's Pizza"})

# Rota GET - Listar Usuario
app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    # recuperar os usuarios (sem senha)
    usuarios_sem_senha = []

    for usuario in usuarios:
        user = usuario.copy()
        user.pop('senha', None)
        usuarios_sem_senha.append(user)

    return jsonify({
        'dados': usuarios_sem_senha,
        'total': len(usuarios)
    }), 200

# POST -> Criar Usuarios
@app.route('/usuarios', methods=['POST'])
def criar_usuario():

    global proximo_id

    valido, erro, dados_validados = \
    validar_usuario(request.get_json())





# iniciar o servidor -> porta padrão 5000
if __name__ == '__main__':
    app.run(debug=True)