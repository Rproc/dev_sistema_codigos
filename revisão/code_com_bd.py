from sqlalchemy import create_engine, text

# Criação e conexão com o banco
engine = create_engine("sqlite:///teste4.db", echo = True, future = True)

# criar tabela
with engine.connect() as conn:
    conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS alunos(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome VARCHAR(50) NOT NULL,
                        idade INTEGER NOT NULL,
                        email VARCHAR(50) UNIQUE NOT NULL
                      )
                      """))
    conn.commit()

# inserir alunos
with engine.connect() as conn:
    conn.execute(text("INSERT INTO alunos (nome, idade, email) " \
                    "VALUES (:nome, :idade, :email)"),
                    [ {"nome":"David", "idade":21, 
                       "email":"davidvarao@senai.br"},
                       {"nome":"Geovanni", "idade":23,
                        "email":"geovannicuricica@senai.br"},
                        {"nome":"Silvio", "idade":25,
                         "email":"silviogaladaglobo@senai.br"}
                    ]
                )
    conn.commit()

# consulta 1
with engine.connect() as conn:
    resultado = conn.execute(text("SELECT * FROM alunos"))
    for dado in resultado:
        print(dado.id, dado.nome, dado.idade, dado.email)


# e2 = create_engine("mysql+pymysql://
# user:senha@localhost:3306/pizzaria")