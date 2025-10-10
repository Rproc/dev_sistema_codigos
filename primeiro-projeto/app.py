from flask import Flask, jsonify, request
# importando a Class Flask do modulo flask

# criar uma instancia do Flask = objeto
app = Flask(__name__)
# __name__ é o nome do modulo atual -> navegação

# Essa linha permite usar caracteres especiais
# no JSON
app.config['JSON_AS_ASCII'] = False
# se esse de cima não pegar, use esse abaixo
# app.json.ensure_ascii = False
usuarios = [
    {'id': 1, 'nome': 'David', 'email': 'davidvarao@senai.br'},
    {'id': 2, 'nome': 'Geovanni', 'email': 'pizza35reais@senai.br'}
]

# Definir Rotas (Endpoints)
# quando acessar ao servidor, chame essa função
@app.route('/')
def home():
    return 'Welcome to the mundo das APIs'

# Sempre faça uma função/rota de verificação
# do status da API
@app.route('/status')
def status():
    return jsonify({
        'status':'online',
        'mensagem':'API funcionando corretamente'
    })

# Rota com GET -> Listar todos os usuarios
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    return jsonify(usuarios), 200

@app.route('/usuario/<int:id>', methods=['GET'])
def buscar_usuario(id):
    # Poderia ser reescrito assim
    # u = None
    # for usuario in usuarios:
    #     if usuario['id'] == id:
    #         u = usuario
    # compreensão de listas
    u = [usuario for usuario in usuarios if usuario['id']==id]
    
    if u == []:
        return jsonify({
            'erro': "Dados inválidos"
        }), 404
    else:
        return jsonify(u), 200

# POST -> Ideia de Criação
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    # pegar dados do frontend/requisição
    dados = request.get_json()

    # verificar se há algo no JSON
    if not dados:
        return jsonify({
            'erro':'Não há Dados'
        }), 400
    
    # Pegar um campo do JSON
    nome = dados.get('nome', '').strip()

    # Isso não ve se esta vazio, 
    # verifica se existe
    if not nome:
        return jsonify({
            'erro':'Não há nome'
        }), 400
    
    # Verificar se tem algo escrito
    if len(nome) < 1:
        return jsonify({
            'erro':'Nome Inválido'
        }), 400

    # lower -> tudo em minuscula
    email = dados.get('email', '').strip().lower()

    if not email:
        return jsonify({
            'erro':'Não há email'
        }), 400
    
    email_existente = [usuario for usuario in usuarios 
            if usuario['email'] == email]
    
    if email_existente == []:
        id = len(usuarios) + 1
        novo_usuario = {
            'id':id,
            'nome': nome,
            'email':email
        }
        usuarios.append(novo_usuario)
        return jsonify({
            'status':201,
            'mensagem': 'Novo usuário criado'
        })
    else:
        return jsonify({
            'status':400,
            'mensagem': 'Email já existente'
        })

# executar o servidor
if __name__ == '__main__':
    app.run(debug=True)
# debug -> servidor no modo de desenvolvimento
# ativa o reload automatico e mostra
# os erros de forma detalhada
