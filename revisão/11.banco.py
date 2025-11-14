from sqlalchemy import create_engine, Column, \
    Integer, String, DECIMAL, Date, ForeignKey
from sqlalchemy.orm import declarative_base, \
    relationship, sessionmaker
from datetime import date

Base = declarative_base()

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    pedidos = relationship("Pedido", 
                           back_populates="cliente")

    def __repr__(self):
        return f"<Cliente(nome='{self.nome}', email='{self.email}')>"


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    preco = Column(DECIMAL(10, 2), nullable=False)

    itens = relationship("PedidoItem", 
                         back_populates="produto")

    def __repr__(self):
        return f"<Produto(nome='{self.nome}', preco={self.preco})>"


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, 
                        ForeignKey("clientes.id"), 
                        nullable=False)
    data = Column(Date, nullable=False)

    cliente = relationship("Cliente", 
                           back_populates="pedidos")
    itens = relationship("PedidoItem", 
                         back_populates="pedido")

    def __repr__(self):
        return f"<Pedido(id={self.id}, cliente='{self.cliente.nome}', data={self.data})>"


class PedidoItem(Base):
    __tablename__ = 'pedido_itens'

    id = Column(Integer, primary_key=True, 
                autoincrement=True)
    pedido_id = Column(Integer, ForeignKey('pedidos.id'),
                       nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'),
                        nullable=False)
    quantidade = Column(Integer, nullable=False)

    pedido = relationship("Pedido",
                          back_populates='itens')
    produto = relationship("Produto",
                           back_populates='itens')
    
    def __repr__(self):
        return f"<PedidoItem(\
    nome_produto='{self.produto.nome}',\
    quantidade={self.quantidade})>"


engine = create_engine(
    'mysql+pymysql://root:alunolab@localhost:3303/loja_virtual',
    echo=False, future=True)

Session = sessionmaker(bind=engine, future=True)

# with Session() as session:
#     # insert clientes
#     anderson = Cliente(nome='Anderson', 
#                        email='andinho@senai.br')
#     elon_musk = Cliente(nome='Elon Musk',
#                         email='coquinha_zero@senai.br')
#     # insert produtos
#     p1 = Produto(nome='Coca Zero 2L', preco=13.00)
#     p2 = Produto(nome='Metanol', preco=15.00)
#     p3 = Produto(nome='Pão com Mortadela', preco=2.50)
#     p4 = Produto(nome='Brigadeiro', preco=5.00)

#     session.add_all([anderson, elon_musk, p1, p2, p3, p4])
#     session.commit()

#     # criar pedidos
#     pedido1 = Pedido(cliente=elon_musk, 
#                      data=date.today())
#     item1 = PedidoItem(pedido=pedido1, produto=p1,
#                        quantidade=5)
#     item2 = PedidoItem(pedido=pedido1, produto=p3,
#                        quantidade=4)
    
#     session.add(pedido1)
#     session.commit()

# consulta
with Session() as session:
    elon = session.query(Cliente).filter_by(nome='Elon Musk').first()

    for pedido in elon.pedidos:
        print(f'Pedido {pedido.id} em {pedido.data}')
        for item in pedido.itens:
            print(f'{item.produto.nome} - R$ {item.produto.preco} - {item.quantidade} unidade')