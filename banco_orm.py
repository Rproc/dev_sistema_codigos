from sqlalchemy import create_engine, \
Column, Integer, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, \
sessionmaker, relationship

# method factory (fabrica de classes)
Base = declarative_base()

# criar classe "real"(vai ser a tabela pelo ORM)
class Aluno(Base):
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, \
                autoincrement=True)
    nome = Column(String(62), nullable=False)
    idade = Column(Integer, nullable=False)
    email = Column(String(62), unique=True, \
                   nullable=False)
    
    # back_populates -> referencia reciproca
    # em outras palavras -> quando vc associa Aluno à
    # AlunoDisciplina, AlunoDisciplona é associada a Aluno
    disciplinas = relationship('AlunoDisciplina', 
                               back_populates='aluno')
    
    # metodo magico (printar um objeto)
    def __repr__(self):
        return f"<Aluno(id={self.id}, \
        nome='{self.nome}',\
        idade={self.idade}, \
        email='{self.email}')>"
    
#  ------------------------------------------------

class Disciplina(Base):
    __tablename__ = 'disciplinas'

    id = Column(Integer, primary_key=True, 
                autoincrement=True)
    nome = Column(String(62), nullable=False,
                  unique=True)
    carga_horaria = Column(Integer, nullable=False)

    # associa Disciplina a AlunoDisciplina e vice-versa
    # meio que a ideia de chave estrangeira
    alunos = relationship('AlunoDisciplina', 
                          back_populates='disciplina')

    def __repr__(self):
        return f"<Disciplina(id={self.id}, \
        nome='{self.nome}', \
        carga_horaria={self.carga_horaria})>"

# -------------------------------------------------

class AlunoDisciplina(Base):
    __tablename__ = 'aluno_disciplina'

    id = Column(Integer, primary_key=True, 
                autoincrement=True)
    id_aluno_fk = Column(Integer, ForeignKey('alunos.id'), 
                         nullable=False)
    id_disciplina_fk = Column(Integer,
                                ForeignKey('disciplinas.id'),
                                nullable=False)

    aluno = relationship('Aluno', 
                         back_populates='disciplinas')
    disciplina = relationship('Disciplina',
                        back_populates='alunos')
    


# criar engine (cria conexão com o BD)
engine = create_engine("sqlite:///tecdev_py.db",\
                       echo=False, future=True)

# criar a sessão (isso conecta o engine ao ORM)
Session = sessionmaker(bind=engine,future=True)

# criar as tabelas
Base.metadata.create_all(engine)

with Session() as session:
    # primeiro passo -> Criar alunos
    raphamel = Aluno(nome='Raphamel', idade=24,
                     email='raphamel@senai.br')
    silvio = Aluno(nome='Silvio', idade=25,
                   email='silviogaladaglobo@senai.br')
    presidente = Aluno(nome='Presidente', idade=18,
                       email='presidente@senai.br')
    eriquison = Aluno(nome='Erick', idade=39,
                      email='erickazeite@senai.br')
    
    # segundo passo -> criar disciplinas
    alg = Disciplina(nome='Algoritmo', carga_horaria=180)
    dev = Disciplina(nome='Desenvolvimento de Sistemas',
                     carga_horaria=180)
    
    session.add_all([raphamel, silvio, presidente,
                     eriquison, alg, dev])
    session.commit()

    # Fazer conexão entre Aluno e Disciplina
    cone = [
        AlunoDisciplina(aluno=raphamel, disciplina=alg),
        AlunoDisciplina(aluno=presidente, disciplina=alg),
        AlunoDisciplina(aluno=eriquison, disciplina=dev),
        AlunoDisciplina(aluno=silvio, disciplina=alg),
        AlunoDisciplina(aluno=silvio, disciplina=dev)
    ]
    session.add_all(cone)
    session.commit()

    # consulta 1
    print('Disciplinas cursadas pelo Silvio')
    for vinculo in silvio.disciplinas:
        print(vinculo.disciplina.nome)

    # consulta 2
    print(20*'-')
    print('Todos alunos em Dev de Sistemas')
    for vinculo in dev.alunos:
        print(f'{vinculo.aluno.nome}')






