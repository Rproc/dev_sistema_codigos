with Session() as session:
    resultado = session.query(Aluno).all()

    for aluno in resultado:
        print(aluno.id, aluno.nome, \
              aluno.idade, aluno.email)