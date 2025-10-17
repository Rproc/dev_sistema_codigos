from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    nome = db.Column(db.String(80),
                     nullable=False)
    email = db.Column(db.String(80),
                      unique=True,
                      nullable=False)
    senha = db.Column(db.String(255),
                      nullable=False)
    
    # Ideia é saber quando o usuario foi criado
    criado = db.Column(db.DateTime, 
    default=datetime.now(timezone.utc))

    atualizado = db.Column(db.DateTime,
    default=datetime.now(timezone.utc),
    onupdate=datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Usuario {self.nome}>'
    
    # Converter o Usuario em um Dict (Dicionario)
    def to_dict(self, incluir_senha=False):

        dados = {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'criado': self.criado.isoformat(),
            'atualizado': self.atualizado.isoformat()
        }

        if incluir_senha:
            dados['senha'] = self.senha

        return dados




