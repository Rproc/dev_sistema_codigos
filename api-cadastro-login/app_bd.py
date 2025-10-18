from flask import Flask, request, jsonify
# import do banco e do modelo (classe) do outro arquivo
from models import db, Usuario 

# cria um objeto flask, que vai ser o app
app = Flask(__name__)

# JSON aceitar caracteres especiais
app.config['JSON_AS_ASCII']=False
# se der errado, descomente o debaixo
# app.json.ensure.ascii = False

# Configuração com o banco 
# Hoje: SQLite // Sexta: MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = \
'sqlite:///pizzaiolo.db'

# Desativar o sistema de rastreamento de modificações
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

# Vamos inicializar a 'caixinha magica' (BD) com o app
db.init_app(app)

def validar_usuario(dados, user=None):
    # user -> chamado só quando atualiza
    # validar dados vindo das requisições
    # 3 retornos: 
    # 1 -> se são validos (True)/False
    # 2 -> Qual foi o erro
    # 3 -> Dados Validados
    # Existem dados no JSON?
    if not dados:
        return False, "Corpo da requisição \
        não pode ser vazio", None
    
    dados_validados = {}

    # se existe o campo nome no JSON
    if 'nome' not in dados:
        # ja que o campo existe, iremos pegar o 
        # valor associado a ele
        if not isinstance(dados['nome'], str):
            return False, "O campo 'nome' deve \
                ser textual", None

        nome = dados.get('nome', '').strip()

        # tenho o nome, o que eu quero validar?
        if not nome:
            return False, \
        "Campo 'nome' não pode estar vazio", None

        # tamanho minimo do nome
        if len(nome) < 3:
            return False, "Campo 'nome' deve ter \
                no minimo 3 caracteres", None

        dados_validados['nome'] = nome
    elif not user:
        return False, "Campo 'nome' é obrigatório", None
    # ------------------------------------
    # Se existe o campo EMAIL no JSON
    if 'email' not in dados:
        if not isinstance(dados['email'], str):
            return False, "O campo 'email' deve \
                ser textual", None
        
        if ('@' not in dados['email'] or 
        '.' not in dados['email']):
            return False, "O email informado não \
                é válido", None

        email = dados.get('email', '').strip().lower()

        if not email:
            return False, "Campo 'email' não \
            pode estar vazio", None
        
        # Certeza -> Campo Email existe e o 
        # email existe
        email_existente = \
            Usuario.query.filter_by(email=email).first()
        
        # verificar se há algum usuario com esse email
        if email_existente:
            return False, "Este email já \
                está cadastrado", None
        
        dados_validados['email'] = email
        
    # Se não for atualização
    elif not user:
        return False, "Campo 'email' é obrigatório", None
    #  ------------------------------------
    if 'senha' not in dados:
        senha = dados.get('senha', '').strip()

        if not senha:
            return False, "Campo 'senha' não pode \
                estar vazio", None
        
        if len(senha) < 8 and len(senha) > 50:
            return False, "Campo 'senha' com \
                tamanho inválido", None 
        
        # user -> é quando vc quer atualizar o usuario
        if user and senha == user.senha:
            return False, "Campo 'senha' não pode ser\
                igual a anterior", None
        
        dados_validados['senha'] = senha

    elif not user:
        return False, "Campo 'senha' é obrigatório", None
    
    return True, None, dados_validados


# Rota padrão - Index - Landpage
@app.route('/')
def home():
    return jsonify({
        'msg':"Bem vindo ao Geovanni's Pizza"})

# Rota GET - Listar Usuario
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():

    try:
        # Pegar todos os usuarios
        usuarios = Usuario.query.all()
        # apresentar esses usuarios em uma lista
        user = [usuario.to_dict() for usuario in usuarios]

        return jsonify({
            'dados': user,
            'total': len(user)
        }), 200
    
    except Exception as e:
        return jsonify({
            'erro':f'Erro ao listar usuários: {e}'
        }), 500

# POST -> Criar Usuarios
@app.route('/usuarios', methods=['POST'])
def criar_usuario():

    try:
        valido, erro, dados_validados = \
        validar_usuario(request.get_json())

        # if valido == False é a mesma coisa que:
        if not valido:
            return jsonify({
                'erro': erro
            }), 400

        novo_usuario = Usuario(
            nome = dados_validados['nome'],
            email = dados_validados['email'],
            senha = dados_validados['senha']
        )

        # Preparar inserção no Banco
        db.session.add(novo_usuario)
        # Adiciono (aqui é quando o ID é adicionado)
        db.session.commit()

        return jsonify({
            'mensagem':'Usuário criado com sucesso',
            'usuario': novo_usuario.to_dict()
        }), 201
    
    except Exception as e:
        return jsonify({
            'erro':f'Erro ao criar usuario: {e}'
        }), 500


# LOGIN
@app.route('/login', methods=['POST'])
def login():

    try:
        dados = request.get_json()

        if not dados:
            return jsonify({
                'erro':'Corpo da requisição não \
                pode estar vazio'
            }), 400
    
        email = dados.get('email', '').strip().lower()
        senha = dados.get('senha', '').strip()

        if not email or not senha:
            return jsonify({
                'erro':'Os campos de email e senha \
                    são obrigatórios'
            }), 400
        
        # filter_by(#1 = #2)
        # #1 = Nome da Coluna da Classe/Banco
        # #2 = Nome da variavel que vc quer achar
        # first() -> retorna o primeiro resultado apenas ou None
        usuario = Usuario.query.filter_by(email=email).first()

        # errou email
        if not usuario:
            return jsonify({
                'erro':'Email ou senha inválidos'
            }), 401
        
        # acertou email, errou a senha
        if usuario.senha != senha:
            return jsonify({
                'erro':'Email ou senha inválidos'
            }), 401
    
        return jsonify({
            'mensagem':'Login realizado com sucesso',
            'usuario':usuario.to_dict(),
            'token': f"token_user_{usuario.id}"
        }), 200

    except Exception as e:
        return jsonify({
            'erro':f'Erro ao efetuar o login: {e}'
        }), 500


@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def deletar_usuario(id_usuario):

    try:
        usuario = Usuario.query.get(id_usuario)

        if not usuario:
            return jsonify({
                'erro':'Usuário informado não foi encontrado'
            }), 404
        
        # Preparando o BD para excluir o usuario
        db.session.delete(usuario)

        # Para confirmar a exclusão
        db.session.commit()
    
        return jsonify({
            'mensagem': 'Usuário deletado com sucesso',
            'id_deletado': id_usuario
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'erro':f'Erro ao deletar usuário:{e}'
        }), 500


# ------------------------------------------------
# Atualizar -> 2 Metodos
# 1. Put -> Atualiza completamente um usuario
# 1.1 -> passar todas as informações 
# (se não quiser mudar, passa de novo os dados antigos)
# 2. Patch -> Atualiza parcialmente um usuario
# 2.1 -> passar apenas os campos que você deseja atualizar

@app.route('/usuarios/<int:id_usuario>', methods=['PATCH'])
def atualizar_usuario(id_usuario):
    try:
        usuario = Usuario.query.get(id_usuario)
    
        if not usuario:
            return jsonify({
                'erro':'Usuário não encontrado'
            }), 404
    
        dados = request.get_json()

        if not dados:
            return jsonify({
                'erro':'Corpo da requisição não pode estar vazio'
            }), 400

        valido, erro, dados_validados = \
            validar_usuario(dados, usuario)
        
        if not valido:
            return jsonify({
                'erro': erro
            }), 400
        # dados_validados -> Todos os dados informados
        # No criar_usuario() -> nome, email, senha
        # No atualizar_usuario() -> ???

        for chave, valor in dados_validados.items():
            # Aqui usaremos uma função para passar 
            # o conteudo do dicionario para o objeto (usuario)
            setattr(usuario, chave, valor)
        
        # atualizar o banco (pelo ORM)
        db.session.commit()

        return jsonify({
            'mensagem': 'Usuário atualizado com sucesso',
            'usuario': usuario.to_dict()
        }), 200
    
    except Exception as e:
        return jsonify({
            'erro':f'Erro ao atualizar o usuário: {e}'
        }), 500

# comando CLI (linha de comando) para popular o banco
@app.cli.command()
def popular_banco():
    """
    Popula o banco com usuários pré "fabricados"\n
    Uso: flask --app app popular_banco

    """
    with app.app_context():
        # usuario(id, nome, email, senha)
        usuarios = [
            {'nome': 'Raphamel', 
             'email':'raphamengo@senai.br', 
             'senha':'Flamengo2019'},
            {'nome': 'David', 
             'email':'davidvarao@senai.br',
             'senha':'Varao123'},
            {'nome': 'Geovanni',
             'email':'geo@vanni.br', 
             'senha':'PizzaioloTricolor'}
        ]

        for user in usuarios:
            # verificar se o usuario existe no banco
            usuario_existente = \
            Usuario.query.filter_by(email=user['email']).first()

            if not usuario_existente:
                # Se o email não está no banco
                # então o usuario não existe
                # logo, criarei o usuario

                # Isso "desempacota" o dicionario
                # Isso é o mesmo que fazer:
                # Usuario(nome=user['nome'], email=user['email'], ...)
                usuario = Usuario(**user)
                db.session.add(usuario)

        db.session.commit()
        print('Banco populado com sucesso')


# iniciar o servidor -> porta padrão 5000
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)