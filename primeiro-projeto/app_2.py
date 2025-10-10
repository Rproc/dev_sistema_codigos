from flask import Flask, jsonify, request
# importando a Class Flask do modulo flask

# criar uma instancia do Flask = objeto
app = Flask(__name__)
# __name__ é o nome do modulo atual -> navegação
    
usuarios = {
    1: {'id': 1, 'nome': 'João', 'email': 'joao@email.com'},
    2: {'id': 2, 'nome': 'Maria', 'email': 'maria@email.com'}
}
# Definir Rotas (Endpoints)
# quando acessar ao servidor, chame essa função

# Rota com parâmetro numérico
@app.route('/usuario/<int:id>', methods=['GET'])
def buscar_usuario(id):
    # Passo 2: Validar tipo do parâmetro
    if not isinstance(id, int):
        return jsonify({'erro': 'ID deve ser um número'}), 400
    
    # Passo 3: Buscar no banco
    usuario = usuarios.get(id)
    
    # Passo 4: Validar se existe
    if not usuario:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    
    # Passo 5: Retornar sucesso
    return jsonify(usuario), 200

@app.route('/usuario', methods=['POST'])
def criar_usuario():
    # Passo 1: Verificar se há dados no corpo
    if not request.is_json:
        return jsonify({'erro': 'Content-Type deve ser application/json'}), 400
    
    dados = request.get_json()
    
    # Passo 2: Validar se os campos obrigatórios existem
    if not dados:
        return jsonify({'erro': 'Corpo vazio'}), 400
    
    if 'nome' not in dados:
        return jsonify({'erro': 'Campo "nome" é obrigatório'}), 400
    
    if 'email' not in dados:
        return jsonify({'erro': 'Campo "email" é obrigatório'}), 400
    
    # Passo 3: Validar tipos dos dados
    if not isinstance(dados['nome'], str):
        return jsonify({'erro': 'Campo "nome" deve ser texto'}), 400
    
    if not isinstance(dados['email'], str):
        return jsonify({'erro': 'Campo "email" deve ser texto'}), 400
    
    # Passo 4: Validar formato dos dados
    if len(dados['nome']) < 3:
        return jsonify({'erro': 'Campo "nome" deve ter no mínimo 3 caracteres'}), 400
    
    if len(dados['nome']) > 100:
        return jsonify({'erro': 'Campo "nome" deve ter no máximo 100 caracteres'}), 400
    
    if '@' not in dados['email'] or '.' not in dados['email']:
        return jsonify({'erro': 'Email inválido'}), 400
    
    # Passo 5: Validar regras de negócio
    email_existe = any(u['email'] == dados['email'] for u in usuarios.values())
    if email_existe:
        return jsonify({'erro': 'Email já cadastrado'}), 409

    # CORREÇÃO 2: gera novo ID corretamente
    novo_id = max(usuarios.keys()) + 1

    novo_usuario = {
        'id': novo_id,
        'nome': dados['nome'].strip(),
        'email': dados['email'].strip()
    }

    # CORREÇÃO 3: adiciona novo usuário ao dicionário
    usuarios[novo_id] = novo_usuario
    
    # Passo 8: Retornar com status 201
    return jsonify(novo_usuario), 201

# executar o servidor
if __name__ == '__main__':
    app.run(debug=True)
# debug -> servidor no modo de desenvolvimento
# ativa o reload automatico e mostra
# os erros de forma detalhada
