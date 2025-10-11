from flask import Flask
# importando a Class Flask do modulo flask

# criar uma instancia do Flask = objeto
app = Flask(__name__)
# __name__ é o nome do modulo atual -> navegação

# quando acessar ao servidor, chame essa função
@app.route('/')
def hello_world():
    return 'Hello, World'
# flask ele converte string em um resposta HTTP

# executar o servidor
if __name__ == '__main__':
    app.run(debug=True)
# debug -> servidor no modo de desenvolvimento
# ativa o reload automatico e mostra
# os erros de forma detalhada
